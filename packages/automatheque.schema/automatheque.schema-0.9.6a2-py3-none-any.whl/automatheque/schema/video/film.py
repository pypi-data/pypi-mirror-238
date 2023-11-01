#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re

from automatheque.plugin import PluginAutomatheque, FILM_EST_VISIONNE, FILM_INFOS
from automatheque.plugins.decomposition.decomposeurs_film import FilmDecomposeursPlugin
from automatheque.lib import Gabarit, Gabarits, Renommable, Decomposable
from automatheque.log import recup_logger
from automatheque.util import enleve_caracteres_invalides

LOGGER = recup_logger(__name__)


class Film(Renommable, Decomposable):
    """Classe qui représente un Film.

    Elle est décomposable et renommable automatiquement par la lib.
    Par défaut la configuration pour le renommage doit se trouver dans une
    section intitulée "renommage_film".
    """

    RENOMMEUR_CONFIG_SECTION = "renommage_film"

    def __init__(self, filename):
        """Initialisation du film à partir de son nom de fichier.

        Si on le souhaite on pourra ajouter ici une recherche sur imdb.
        :param filename: Nom du fichier

        TODO : basename devrait être autocalculée à chque fois et renvoyer un Path
        """
        # Fichier :
        self.filename = filename  # chemin complet
        (debut, fin) = os.path.split(self.filename)
        self.basename = fin or os.path.basename(debut)
        self.ext = os.path.splitext(self.basename)[1][1:]
        # Entité :
        self.titre = ""
        self.annee = 0
        self._est_visionne = None
        self._ids = {}  # TODO mettre un namedtuple

    def __setattr__(self, attribut, valeur):
        if attribut == "titre" and valeur:
            valeur = self._normalise_titre(valeur)
        object.__setattr__(self, attribut, valeur)

    def __str__(self):
        try:
            return "film: {}, année: {:04d}, ext: {}".format(
                self.titre, self.annee or 0, self.ext
            )
        except Exception as e:
            return self.basename

    @property
    def est_visionne(self):
        if self._est_visionne is not None:
            return self._est_visionne
        for p in PluginAutomatheque.plugins_par_capacite(FILM_EST_VISIONNE):
            try:
                self._est_visionne = p.est_visionne(self)
            except Exception as e:
                LOGGER.debug(e)
                continue
            else:
                LOGGER.debug("visionné {}: plugin {}".format(self._est_visionne, p.cle))
                return self._est_visionne

    @property
    def ids(self):
        if not self._ids:
            self._charger_infos()
        return self._ids

    def _normalise_titre(self, titre=None):
        """Normalise et renvoie le titre."""
        if not titre:
            titre = self.titre
        from automatheque.modele.video import videoNormaliseur

        titre = videoNormaliseur.normalise(titre, "nettoyage")
        titre = videoNormaliseur.normalise(titre, "film")
        return titre.title().strip()  # TODO peut on le mettre dans normaliseur ?

    def _normalise_basename_ou_valeur(self, valeur=None):
        """Normalise le basename et le stocke dans le titre."""
        from automatheque.modele.video import videoNormaliseur

        if not valeur:
            valeur = self.basename
            # On retire l'extension :
            valeur = os.path.splitext(valeur)[0]
        res = videoNormaliseur.normalise(valeur, "release")
        return videoNormaliseur.normalise(res, "film")

    @classmethod
    def _decomposeurs_par_defaut(cls):
        """Surcharge de la fonction de Decomposable.

        Renvoie une instance de Identificateurs ou le chemin vers la classe.

        return (
            "automatheque.modele.video.identificateurs_film.FilmIdentificateurs"
        )  # noqa
        """
        p = FilmDecomposeursPlugin()
        return p.decomposeurs

    @classmethod
    def _gabarits_par_defaut(cls):
        """Surcharge de la fonction de Renommable.

        Renvoie une instance de Gabarits.
        """
        gabarits = Gabarits()
        defaut = [
            {
                "squelette": "{film} ({annee})/{film} ({annee}).{ext}",
                "condition": "{annee} >= 1850",
                "ordre": 1,
            },
            {"squelette": "{film}/{film}.{ext}", "condition": "", "ordre": 1},
        ]
        for elem in defaut:  # TODO faire une fonction de gabarit ajout_dict ?
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
        champs = {"film": self.titre, "annee": self.annee, "ext": self.ext}
        return {
            key: enleve_caracteres_invalides(value) for (key, value) in champs.items()
        }

    def _prepare_decomposition(self, valeur=None):
        return self._normalise_basename_ou_valeur(valeur)

    def _charger_infos(self):
        for p in PluginAutomatheque.plugins_par_capacite(FILM_INFOS):
            try:
                p.recup_film_infos(self)
            except Exception:
                continue
            else:
                break
