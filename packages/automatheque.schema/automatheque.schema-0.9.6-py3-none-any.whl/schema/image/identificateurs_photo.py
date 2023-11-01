#!/usr/bin/python3
"""Identificateurs pour la classe :class:`Photo`."""
import re  # pour les flags
from datetime import datetime

# import Automatheque
from automatheque.lib.decomposeur import Identificateur, Identificateurs


def assigne_tags(obj, infos):
    """Fonction appelée quand l'identificateur remonte des informations.

    Ici on veut que l'identificateur capture la chaîne suivante :
    {tag1: valeur1}{tag2: valeur2, valeur3}
    à partir de la chaîne d'origine :
    {{tag1: valeur1}{tag2: valeur2, valeur3}}

    Il nous reste donc à capturer chaque groupe "{tag:valeurs}" avant de
    l'assigner à l'objet :class:`Photo`.

    :param infos:  Résultat du findall de la chaîne de l'identificateur, pour
                   PATRON_IDENTIFICATION_TAGS le résultat est une chaîne,
                   pas une liste
    """
    patron_tags = re.compile(r"(?:\{(.*?):([^}]*)\}\s*)")
    res = patron_tags.findall(infos)
    for nom_tag, valeur in res:
        # Traitement particulier pour les dates que l'on doit transformer
        # en objet datetime:
        if nom_tag.startswith('date'):
            try:
                valeur = datetime.strptime(valeur, "%Y%m%d %H%M%S")
            except Exception:
                # TODO on pourrait tester d'autres formats de date ou utiliser
                # dateutils ou dateparser ou autre
                pass
        setattr(obj.tags, nom_tag, valeur)


class PhotoIdentificateurs(Identificateurs):
    """Identificateurs proposés par défaut pour les photos.

    On cree une classe spécifique qu'on passera au decomposeur, pour pouvoir
    utiliser des identificateurs différents en fonction de ce que l'on cherche.

    1. Le premier format attendu est le suivant :
    {{album: salut, ça va}{titre: hello}} => album=salut, titre=hello
    """

    PATRON_IDENTIFICATION_TAGS = Identificateur(
        r"(?<=\{)((?:\{[^:]*:[^}]*\})*)(?=\s*\})",
        drapeaux=re.IGNORECASE,
        appel_source=lambda o, valeur: o._prepare_decomposition(valeur),
        appel_en_retour=lambda o, m: assigne_tags(o, m))
    # TODO :
    PATRON_IDENTIFICATION_GOURMAND = Identificateur(
        r"(.*)",
        drapeaux=re.IGNORECASE,
        appel_en_retour=lambda o, m: assigne_tags(o, [m], 0))
    # TODO on pourrait
    # chercher à avoir un identificateur qui fasse :
    # {annee} - {evenement} ou {album} ??

    def __init__(self):
        """Remplissage des identificateurs."""
        super(PhotoIdentificateurs, self).__init__()
        self.identificateurs.append(self.PATRON_IDENTIFICATION_TAGS)
        #self.identificateurs.append(self.PATRON_IDENTIFICATION_GOURMAND)
