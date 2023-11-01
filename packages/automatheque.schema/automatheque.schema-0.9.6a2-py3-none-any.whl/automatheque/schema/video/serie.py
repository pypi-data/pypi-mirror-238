# -*- coding: utf-8 -*-
import re

from automatheque.util import enleve_caracteres_invalides


class Serie(object):
    """
    Classe pour représenter les séries tv.
    """

    def __init__(self, titre=""):
        self.titre = titre
        self.episodes = []
        self.description = ""
        self.saisons = []
        self._normalise_titre()
        self.redresse_titre_annee()

    def _normalise_titre(self):
        """
        Pour nettoyer le titre de la série, sans forcément supprimer tous les
        caractères spéciaux. Ou bien si au contraire ! :-)
        """
        suppr_team = re.sub(r"^\[.*?\]", " ", self.titre)
        # S'il reste du texte après avoir supprimé la potentielle "team"
        # alors on estime que c'est le titre, sinon on ne fait rien.
        self.titre = suppr_team if suppr_team else self.titre
        self.titre = re.sub(r"[\s,._-]", " ", self.titre)
        self.titre = self.titre.title().strip()

    def _liste_champs_dispo(self):
        """
        Surcharge de la fonction de Renommable, même si Serie ne l'est pas.

        liste des champs disponibles pour le parsing.
        TODO : on peut meme gérer plusieurs langues !
        """
        champs = {"serie": self.titre, "description": self.description}
        return {
            key: enleve_caracteres_invalides(value) for (key, value) in champs.items()
        }

    def redresse_titre_annee(self):
        """Ecrit l'année du titre sous la forme (YYYY) si elle existe."""
        # Le schema (?<!) permet d'interdire des caractères avant ceux trouvés
        # et le schema (?!) permet d'interdire des caractères après.
        # Ici on cherche une année qui n'est pas déjà entre ().
        schema = re.compile(r"(?<!\d|\()((?:19|20)\d{2})(?!\d|\))")
        try:
            annee = schema.findall(self.titre)[0]
            self.titre = re.sub(schema, "", self.titre).strip()
        except IndexError:
            pass  # aucune année trouvée par le findall
        else:  # si le try est arrivé jusqu'au bout (= nobreak)
            self.titre = "{} ({})".format(self.titre, annee)
