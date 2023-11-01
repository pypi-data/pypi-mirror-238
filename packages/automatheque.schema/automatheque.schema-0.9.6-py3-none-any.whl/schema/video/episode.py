#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from .serie import Serie
from automatheque.lib import Gabarit, Gabarits, Renommable, Decomposable
from automatheque.plugin import PluginAutomatheque, EPISODE_EST_VISIONNE, EPISODE_INFOS
from automatheque.plugins.decomposition.decomposeurs_serie import (
    SerieSaisonDecomposeursPlugin,
)
from automatheque.util import enleve_caracteres_invalides


# TODO creer EpisodeFile ?
# TODO composition instead of inheritance ! Renommable doit être une interface, pas un héritage
class Episode(Renommable, Decomposable):
    """Classe qui représente un ou plusieurs épisode de série tv."""

    def __init__(self, filename):
        """Initialisation de l'épisode à partir de son nom de fichier.

        On utilise un set() pour gérer les numéros d'épisode puisqu'il permet
        de stocker sans doublon :
        https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset

        :param filename: Nom du fichier
        """
        # Fichier :
        self.filename = filename  # chemin complet
        (debut, fin) = os.path.split(self.filename)
        self.basename = fin or os.path.basename(debut)
        self.ext = os.path.splitext(self.basename)[1][1:]
        # Entité :
        self.serie = Serie()
        self.saison = None
        self._est_visionne = None
        self._tvdbid = None
        self._ids = {}  # TODO mettre un namedtuple
        # liste des numéros d'épisode, suivant que le fichier contient un ou
        # plusieurs épisodes
        self.episode = set([])
        self.titre = ""  # si on a l'occasion d'avoir le titre de l'episode
        self.qualite = ""
        self.description = ""
        self.date_diffusion = ""

    def __setattr__(self, attribut, valeur):
        if attribut == "serie":
            if not isinstance(valeur, Serie):
                raise ValueError(Serie)
            # Quand on ajoute un objet Serie, on ajoute l'episode dans sa liste
            valeur.episodes.append(self)
            if hasattr(self, "serie") and isinstance(self.serie, Serie):
                try:
                    self.serie.episodes.remove(self)
                except ValueError:  # Erreur : list.remove(x): x not in list
                    pass
        object.__setattr__(self, attribut, valeur)

    def __str__(self):
        try:
            return "serie: {}, saison: {:02d}, episodes: {}, ext: {}".format(
                self.serie.titre,
                self.saison,
                "-".join(str(x) for x in sorted(self.episode)),
                self.ext,
            )
        except Exception as e:
            return self.basename

    @property
    def est_visionne(self):
        if self._est_visionne is not None:
            return self._est_visionne
        for p in PluginAutomatheque.plugins_par_capacite(EPISODE_EST_VISIONNE):
            try:
                self._est_visionne = p.est_visionne(self)
            except Exception:
                continue
            else:
                # TODO DEBUG logger
                print(self._est_visionne, p.cle)
                return self._est_visionne

    @property
    def tvdbid(self):
        if not self._tvdbid:
            self._charger_infos()
            try:
                self.tvdbid = self._ids["tvdb"]
            except Exception:
                pass
        return self._tvdbid

    @tvdbid.setter
    def tvdbid(self, value):
        self._tvdbid = value

    @property
    def ids(self):
        if not self._ids:
            self._charger_infos()
        return self._ids

    @classmethod
    def _normalise(cls, nomfichier):
        """
        TODO :
        Creer une classe de normalisation en fonction de ce que l'on souhaite
        faire : normaliser les parentheses, les espaces etc.
        cf : filebot/normalization et filebot/ReleaseInfo pour le nettoyage
        """
        # On retire l'extension :
        res = os.path.splitext(nomfichier)[0]
        # premier schéma de nommage:
        # sauf si le nom de la série contient un ., mais c'est rare
        # res = re.sub(r'[\s,._-]', ' ', nomfichier)
        # res = re.sub(r'Onelinkmoviez.com', '', res)
        # Les lignes ci dessous seront gérées dans le fichier de patrons
        # res=re.sub(r'(season[ ]*|saison[ ]*)', 'S', res, flags=re.IGNORECASE)
        # res = re.sub(r'episode[ ]*', 'E', res, flags=re.IGNORECASE)
        from automatheque.modele.video import videoNormaliseur

        res = videoNormaliseur.normalise(res, "episode")
        res = videoNormaliseur.normalise(res, "saison")
        res = videoNormaliseur.normalise(res, "release")

        return res

    @classmethod
    def _decomposeurs_par_defaut(cls):
        """Surcharge de la fonction de Decomposable.

        Renvoie une instance de Decomposeurs ou le chemin vers la classe.
        """
        p = SerieSaisonDecomposeursPlugin()
        return p.decomposeurs

    @classmethod
    def _gabarits_par_defaut(cls):
        """Surcharge de la fonction de Renommable.

        Renvoie une instance de Gabarits.
        """
        gabarits = Gabarits()
        defaut = [
            {
                "squelette": "{serie}/{serie} - Saison {saison:02d}/{serie} S{saison:02d}E{episodes[0]:02d}-{episodes[1]:02d}.{ext}",  # noqa
                "condition": "len({episodes}) == 2",
                "ordre": 1,
            },
            {
                "squelette": "{serie}/{serie} - Saison {saison:02d}/{serie} S{saison:02d}E{episode:02d} - {titre}.{ext}",  # noqa
                "condition": '"' + "{titre}" + '"',
                "ordre": 1,
            },
            {
                "squelette": "{serie}/{serie} - Saison {saison:02d}/{serie} S{saison:02d}E{episode:02d}.{ext}",  # noqa
                "condition": "",
                "ordre": 1,
            },
        ]
        for elem in defaut:
            g = Gabarit()
            for k, v in elem.items():
                setattr(g, k, v)
            gabarits.append(g)
        return gabarits

    def _liste_champs_dispo(self):
        """
        Surcharge de la fonction de Renommable.

        liste des champs disponibles pour le parsing.
        TODO : on peut meme gérer plusieurs langues !
        """
        champs = {
            "serie": self.serie.titre,
            "saison": self.saison,
            "episode": next(iter(self.episode)) if len(self.episode) == 1 else "multi",
            "episodes": sorted(self.episode) if len(self.episode) > 1 else [],
            "titre": self.titre,
            "ext": self.ext,
            "description": self.description,
            "date_diffusion": self.date_diffusion,
        }
        return {
            key: enleve_caracteres_invalides(value) for (key, value) in champs.items()
        }

    def _prepare_decomposition(self, valeur=None):
        if not valeur:
            valeur = self.basename
        nomfichier = self._normalise(valeur)

        return nomfichier

    def _charger_infos(self):
        for p in PluginAutomatheque.plugins_par_capacite(EPISODE_INFOS):
            try:
                p.recup_infos(self)
            except Exception:
                continue
            else:
                break
