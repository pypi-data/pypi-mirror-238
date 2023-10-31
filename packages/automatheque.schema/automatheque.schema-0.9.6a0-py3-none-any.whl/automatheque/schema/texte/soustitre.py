# -*- coding: utf-8 -*-
"""Classe pour gérer les sous-titres d'un élément video.

L'idée est de prendre un fichier sous-titre, de le remplir comme si
c'était une vidéo puis de se servir des données décomposées pour
renommer le fichier.

Processus :
* décomposition : décompose le fichier comme une vidéo (avec videomate)
* si *.srt alors new SousTitre(filename, video)
* décomposition spécifique au sous titre pour détecter langue
* renommage : proposer une valeur 'video_file' et 'video_file_rep',
              enlever l'extension sur le video_file et utiliser qqch comme :
                "{video_file_no_ext}/lang.ext" ou "{video_file_no_ext}.lang.ext"
"""
import attr
import os

from automatheque.lib.renommeur import Gabarit, Gabarits, Renommable, Renommeur
from automatheque.lib.decomposeur import Decomposable
from automatheque.plugins.decomposition.decomposeurs_soustitre import (
    SousTitreDecomposeursPlugin,
)


@attr.s
class SousTitre(Decomposable, Renommable):

    filename = attr.ib()  # Nécessaire pour Renommable
    # TODO : la vidéo doit déjà être décomposée !
    video = attr.ib()
    basename = attr.ib(init=False)  # Nécessaire pour Decomposable
    # TODO ici on n'hérite pas de Renommable pour changer mais on doit quand même
    # l'utiliser plus loin, donc il faudrait peut-être trouver un moyen de passer
    # le filename en paramètre de Renommable ? ou exiger que les classes qui héritent
    # de l'interface aient certaines propriétés ??
    ext = attr.ib(init=False)
    langue = attr.ib(init=False)
    ordre = attr.ib(init=False, default=0)

    def __attrs_post_init__(self):
        (debut, fin) = os.path.split(self.filename)
        self.basename = fin or os.path.basename(debut)
        # self.ext = os.path.splitext(self.basename)[1][1:]

        self.basename, self.ext = os.path.splitext(self.basename)
        self.ext = self.ext[1:]  # Enlève le "."

    def _liste_champs_dispo(self):
        """
        Surcharge de la fonction de Renommable.

        liste des champs disponibles pour le parsing.
        TODO : on peut meme gérer plusieurs langues !
        """
        video_infos = self.recup_video_infos()
        champs = {
            "langue": self.langue,
            "ext": self.ext,
            "ordre": self.ordre,
            "video_type": self.video.__class__.__name__,
            "video": self.video.filename,
            # TODO pb pour les chemins, il faut peut-être le décomposer
            # et le recomposer ??
            "video_parent": video_infos["video_parent"],
            "video_sans_ext": video_infos["video_sans_ext"],
        }
        return {
            # key: enleve_caracteres_invalides(value) for (key, value) in champs.items()
            key: value
            for (key, value) in champs.items()
        }

    @classmethod
    def _gabarits_par_defaut(cls):
        """Surcharge de la fonction de Renommable.

        Renvoie une instance de Gabarits.
        """
        gabarits = Gabarits()
        defaut = [
            {
                "squelette": "{video_parent}/Subs/{video_sans_ext}/{ordre}_{langue}.{ext}",  # noqa
                "condition": "len('{langue}') > 1 and int({ordre}) and '{video_type}' == 'Episode'",  # noqa
                "ordre": 1,
            },
            {
                "squelette": "{video_parent}/Subs/{ordre}_{langue}.{ext}",
                "condition": "len('{langue}') > 1 and int({ordre})",
                "ordre": 1,
            },
            {
                "squelette": "{video_parent}/{video_sans_ext}.{langue}.{ext}",
                "condition": "len('{langue}') > 1",
                "ordre": 2,
            },
            {
                "squelette": "{video_parent}/{video_sans_ext}.{ext}",
                "condition": "",
                "ordre": 2,
            },
        ]
        for elem in defaut:
            g = Gabarit()
            for k, v in elem.items():
                setattr(g, k, v)
            gabarits.append(g)
        return gabarits

    @classmethod
    def _decomposeurs_par_defaut(cls):
        """Surcharge de la fonction de Decomposable.

        Renvoie une instance de Decomposeurs ou le chemin vers la classe.
        """
        p = SousTitreDecomposeursPlugin()
        return p.decomposeurs

    # def renomme(self, v_rep_cible, debug=False, force=False, copier=False):
    #    """Appelle le renommage de Renommeur.
    #
    #    Args:
    #        v_rep_cible ([type]): TODO passer un Path ?
    #        debug (bool, optional): [description]. Defaults to False.
    #        force (bool, optional): [description]. Defaults to False.
    #        copier (bool, optional): [description]. Defaults to False.
    #    """
    #    renommable = Renommable(self)
    #    renommable.renomme(v_rep_cible, debug, force, copier)

    def recup_video_infos(self):
        renommeur = Renommeur(self.video)
        renommeur._remplir_gabarits()
        video = renommeur._construire_nouveau_nom()
        video_chemin_sans_ext = os.path.splitext(video)[0]
        (video_parent, video_basename) = os.path.split(video_chemin_sans_ext)
        return {
            "video_parent": video_parent,
            "video_sans_ext": video_basename,
        }
