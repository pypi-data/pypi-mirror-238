# -*- coding: utf-8 -*-
"""Package destiné à gérer les vidéos.
"""
from .serie import Serie
from .episode import Episode
from .film import Film

import os

# Automatheque:
from automatheque.lib.normaliseur import Normaliseur
from automatheque.lib.decomposeur import Decomposeurs

__all__ = ["Episode", "Film", "Serie"]


FICHIER_PATRONS_INFOS_VIDEO = os.path.join(
    os.path.dirname(__file__), "patrons_infos_video.yaml"
)  # TODO déplacer dans constantes

# TODO chemin à suivre :
# recuperation d'un fichier
# 1. determiner le type de fichier (MIME ? xattr)
# => modele_detecteur.py // media_detection.py
# 2. si c'est un fichier video utiliser les methodes appropriees
# 3. nettoyer le nom du fichier
# 4. déterminer si c'est un episode ou un film
# => classe Video avec "nettoie" et "normalise" ? mais comment le transformer
# ensuite en objet episode ?
# 5. enregistrer dans xattr ? https://github.com/xattr/xattr

# on peut faire self.__class__ = Episode et self.__init__ ensuite :thinking:
# ou juste :
# try:
#     e = Episode(bb)
#     e.decompose()
# else:
#     return e
# try:
#     f = Film(bb)
#     f.decompose()
#     f.scrappinginternet() ??
# else:
#     return f

# Tout mettre dans un objet Video dont dependent les autres ?
# => pas sur parce que c'est etrange de devoir etre une instance de video pour
# faire ces tests !
# ou on fait les 2 ? à voir ,la question etant comment je sais si je suis
# un film ou un episode : MediaDetection !


def _detecteModeleVideo(fichier):
    """Cherche le modèle de type Video pour le fichier donné.

    .. todo::
       on pourrait l'améliorer en vérifiant par ex le nombre de minutes du
       fichier : entre 0 et 61 : probablement une série, sinon probablement un
       film , à ajouter avec le test de décomposition.

    Utilisé par media_detection.py"""
    # On commence par tester avec les décomposeurs de plus gros poids
    try:
        e = Episode(fichier)
        decomposeurs = Decomposeurs()
        decomposeurs.decomposeurs = [
            d for d in e._decomposeurs_par_defaut() if d.poids > 0
        ]
        e.auto_decompose(decomposeurs=decomposeurs)
    except Exception:
        pass
    else:
        return e
    try:
        f = Film(fichier)
        decomposeurs = Decomposeurs()
        decomposeurs.decomposeurs = [
            d for d in f._decomposeurs_par_defaut() if d.poids > 0
        ]
        f.auto_decompose(decomposeurs=decomposeurs)
    except Exception:
        pass
    else:
        return f

    # Puis on prend les décomposeurs de poids faible,
    # et on termine avec le film, car pas défaut il prend tout !
    try:
        e = Episode(fichier)
        decomposeurs = Decomposeurs()
        decomposeurs.decomposeurs = [
            d for d in e._decomposeurs_par_defaut() if d.poids == 0
        ]
        e.auto_decompose(decomposeurs=decomposeurs)
    except Exception:
        pass
    else:
        return e
    try:
        f = Film(fichier)
        decomposeurs = Decomposeurs()
        decomposeurs.decomposeurs = [
            d for d in f._decomposeurs_par_defaut() if d.poids == 0
        ]
        f.auto_decompose(decomposeurs=decomposeurs)
    except Exception:
        pass
    else:
        return f
    return None


def estEpisode(video):
    return isinstance(video, Episode)


def estFilm(video):
    return isinstance(video, Film)


def estSerie(video):
    return isinstance(video, Serie)


videoNormaliseur = Normaliseur(FICHIER_PATRONS_INFOS_VIDEO)
