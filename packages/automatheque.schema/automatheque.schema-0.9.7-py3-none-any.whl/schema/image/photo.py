# -*- coding: utf-8 -*-
"""Module pour gérer les Photos.

.. moduleauthor:: marrco <marrco@wohecha.fr>
"""
import os
import re
import imghdr
import attr


from .tags import ExifTags

from automatheque.lib import Decomposable, Gabarit, Gabarits, Renommable
from automatheque.log import recup_logger
from automatheque.modele.base import Media
from automatheque.modele.calendrier.evenement import Evenement
from automatheque.util import enleve_caracteres_invalides

LOGGER = recup_logger(__name__)


@attr.s
class Photo(Media, Renommable, Decomposable):
    """A photo object.

    :param str filename: The fully qualified path to the photo file
    """

    # Extensions valides pour les photos TODO que ça ??
    extensions = ("arw", "cr2", "dng", "gif", "jpeg", "jpg", "nef", "rw2")

    # ATTENTION il ne faut pas modifier le filename en cours de route
    # sinon les tags n'ont plus la bonne valeur.
    # TODO corriger ça avec un super__ ou avec une property sur filename qui
    # appelle tags.source.
    # filename = attr.ib()
    basename = attr.ib(init=False, default=None)
    tags = attr.ib(
        default=attr.Factory(lambda self: ExifTags(self.source), takes_self=True)
    )
    _charger_tags = attr.ib(default=False)

    def __attrs_post_init__(self):
        """Automatiquement joué après l'initialisation."""
        self.filename = self.source
        if not self.is_valid():
            return None
        (debut, fin) = os.path.split(self.filename)
        self.basename = fin or os.path.basename(debut)
        if self._charger_tags:
            self._charge_tags()

    def is_valid(self):
        """Vérifie si le fichier est valide.

        Récupéré de https://github.com/jmathai/elodie.
        TODO À changer plus tard.

        :returns: bool
        """
        source = self.filename

        # Tout d'abord on vérifie que c'est bien une image :
        if imghdr.what(source) is None:
            return False

        return os.path.splitext(source)[1][1:].lower() in self.extensions

    def _charge_tags(self):
        """Remplit les metadonnées des tags."""
        self.tags = self.tags._charge_tags()

    # Renommable :
    @classmethod
    def _gabarits_par_defaut(cls):
        """Surcharge de la fonction de Renommable.

        Renvoie une instance de Gabarits.
        """
        gabarits = Gabarits()
        defaut = [
            {
                "squelette": "{date.year}/{date:%Y-%m}/{date:%Y-%m-%d} {album} @{lieu}/{_nom_fichier}",  # noqa
                "condition": '"{lieu}" and "{album}"',
                "ordre": 2,
            },
            {
                "squelette": "{evenement_obj.date_debut.year}/{evenement_obj.date_debut:%Y-%m}/{_date_ev} {_album}/{_nom_fichier}",  # noqa
                "condition": '"{evenement_obj.date_debut.year}" and "{_date_ev}" and "{_album}"',
                "ordre": 3,
            },  # noqa
            {
                "squelette": "{evenement_obj.date_debut.year}/{evenement_obj.date_debut:%Y-%m}/{_date_ev} {_album} @{ville}/{_nom_fichier}",  # noqa
                "condition": '"{evenement_obj.date_debut.year}" and "{_date_ev}" and "{_album}" and "{ville}"',
                "ordre": 2,
            },  # noqa
            {
                "squelette": "{evenement_obj.date_debut.year}/{evenement_obj.date_debut:%Y-%m}/{_date_ev} {_album} @{ville} {pays}/{_nom_fichier}",  # noqa
                "condition": '"{evenement_obj.date_debut.year}" and "{_date_ev}" and "{_album}" and "{ville}" and "{pays}" != "FR"',
                "ordre": 1,
            },  # noqa
            {
                "squelette": "{date.year}/{date:%Y-%m}/{date:%Y-%m-%d} sans doute screenshots/{_nom_fichier}",  # noqa
                "condition": "{date}",
                "ordre": 5,
            },
        ]
        for elem in defaut:
            g = Gabarit()
            for k, v in elem.items():
                setattr(g, k, v)
            gabarits.append(g)
        return gabarits

    def _liste_champs_dispo(self):
        """Surcharge de la fonction de Renommable.

        liste des champs disponibles pour le parsing.
        TODO : on peut meme gérer plusieurs langues !
        """
        if not self.tags.nom_origine:
            self.tags.nom_origine = self.tags._calc_nom_origine()

        _date_ev = ""
        _album = self.tags.album or ""
        if isinstance(self.tags.evenement, Evenement):
            _date_ev = "{date.year}-{date.month:02d}-{date.day:02d}".format(
                date=self.tags.evenement.date_debut
            )
            if self.tags.evenement._date_fin_diff_court:
                # TODO pouvoir formater aussi ce "date_ev"
                _date_ev = "{date.year}-{date.month:02d}-{date.day:02d} au {diff}".format(
                    date=self.tags.evenement.date_debut,
                    diff="-".join(
                        map(
                            lambda x: "{:02d}".format(x),
                            self.tags.evenement._date_fin_diff_court,
                        )
                    ),
                )
            _album = self.tags.evenement.titre if self.tags.evenement.titre else ""
        else:
            _album = self.tags.evenement if self.tags.evenement else _album

        champs = {
            # fmt: off
            "date": self.tags.date_prise_de_vue if self.tags.date_prise_de_vue else self.tags.date_creation_fichier,
            # fmt: on
            "date_prise_de_vue": self.tags.date_prise_de_vue,
            "date_creation_fichier": self.tags.date_creation_fichier,
            "date_modification_fichier": self.tags.date_modification_fichier,
            "fabriquant_appareil": self.tags.fabriquant_appareil,
            "modele_appareil": self.tags.modele_appareil,
            "latitude": self.tags.latitude,
            "longitude": self.tags.longitude,
            "timezone": self.tags.timezone,
            # TODO sert à qqch ? renvoyer un "emplacement ?"
            # 'coordonnees_gps': self.tags.coordonnees_gps,
            "album": self.tags.album,  # TODO utiliser une classe Album
            "auteur": self.tags.auteur,
            # On utilise _obj pour signifier que l'événement est un objet :
            # fmt: off
            "evenement_obj": self.tags.evenement if isinstance(self.tags.evenement, Evenement) else None,
            # fmt: on
            "lieu": self.tags.lieu_quartier,
            "ville": self.tags.ville,
            "province": self.tags.province_etat,
            "pays": self.tags.pays,
            "titre": self.tags.titre,
            "mime_type": self.get_mimetype(),
            "nom_origine": self.tags.nom_origine,
            "nom_court": os.path.splitext(os.path.basename(self.filename))[0],
            "extension": self.extension,
            "chemin_repertoire": os.path.dirname(self.filename),
            # Ici les choix qui semblent les plus judicieux:
            # Ce ne sont que des "str" précalculées.
            # TODO on devrait en faire des objets avec une str par def et sinon
            # des paramètres de formatages en option comme date par ex.
            "_date_ev": _date_ev,
            "_album": "{}".format(_album).strip(),
            # fmt: off
            "_nom_fichier": "{date:%Y%m%d-%H%M%S}_{nom_origine}.{ext}".format(
                date=self.tags.date_prise_de_vue if self.tags.date_prise_de_vue else self.tags.date_creation_fichier,
                nom_origine=re.sub(r"\W+", "-", os.path.splitext(self.tags.nom_origine)[0]),
                ext=self.extension,
            ),
            # fmt: on
            # '_lieu': tags.ville TODO si un jour on a un "nom_personnalisé"
        }

        # On retourne "" à la place de "None" :
        # TODO faire cela de manière systématique sur les "champs_dispo"
        champs = {
            cle: valeur if valeur is not None else ""
            for (cle, valeur) in champs.items()
        }

        # On filtre certains caractères qui ne pourraient pas être utilisés :
        return {
            cle: enleve_caracteres_invalides(valeur) for (cle, valeur) in champs.items()
        }

    @classmethod
    def _identificateurs_par_defaut(cls):
        """Surcharge de la fonction de Decomposable.

        Renvoie une instance de Identificateurs ou le chemin vers la classe.
        """
        # fmt: off
        return ("automatheque.modele.image.identificateurs_photo.PhotoIdentificateurs")  
        # fmt: on

