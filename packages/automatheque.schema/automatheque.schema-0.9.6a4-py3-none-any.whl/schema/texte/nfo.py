# -*- coding: utf-8 -*-
import os
from jinja2 import Template

from automatheque.lib import Renommable

TEMPLATE_SHOW = """<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<tvshow>
    <title>{{ serie }}</title>
    <showtitle>{{ serie }}</showtitle>
    <displayseason>{{ saison|default(-1, true) }}</displayseason>
    <displayepisode>{{ episode|default(-1, true) }}</displayepisode>
    <plot>{{ description }}</plot>
</tvshow>
"""
TEMPLATE_EPISODE = """<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<episodedetails>
    <title>{{ titre }}</title>
    <plot>{{ description|safe }}</plot>
    <aired>{{ date_diffusion }}</aired>
    <season>{{ saison|default(1, true) }}</season>
    <episode>{{ episode }}</episode>
</episodedetails>
"""


class FichierNfo(Renommable):
    # TODO autre option faire un NFOGenerateur et passer les param sans les
    # mettre dans l'objet
    def __init__(self, source=None, template=None, dest=None):
        """Initialisation.

        :param source: objet ou dict source
        :param template Template: objet jinja2.Template
        """
        self.ext = 'nfo'
        self.source_dict = self.filename = self.rendu_final = None

        self.template = template
        self.source = source
        self.dest = dest

        # Pré-traitement du template et de la source :
        self.initialise()

        if self.template and self.source:
            self.rendu_final = self._genere_nfo()

    def initialise(self):
        """."""
        if not self.template:
            self.template = self._choisir_template()
        try:
            # On utilise _liste_champs_dispo si possible
            self.source_dict = self.source._liste_champs_dispo()
            self.source_dict['ext'] = self.ext
        except Exception:
            self.source_dict = self.source

    def _liste_champs_dispo(self):
        return self.source_dict

    def _gabarits_par_defaut(self):
        if not isinstance(self.source, Renommable):
            raise TypeError(
                "La source doit être Renommable pour que FichierNfo le soit")
        return self.source._gabarits_par_defaut()

    def _choisir_template(self, source=None):
        from automatheque.modele.video import Episode, Serie, Film
        source = self.source if not source else source
        if isinstance(source, Episode):
            template = TEMPLATE_EPISODE
        if isinstance(source, Serie):
            template = TEMPLATE_SHOW
        if isinstance(source, dict):
            print('[W] pas de template auto defini pour les dictionnaires')
        return Template(template)

    def _genere_nfo(self):
        return self.genere_nfo(source_dict=self.source_dict,
                               template=self.template)

    def ecrit_fichier(self, rep_cible):
        filename = self.dest if self.dest else 'tvshow.nfo'
        self.filename = os.path.join(rep_cible, filename)

        with open(self.filename, 'w') as f:
            f.write(self.rendu_final)

        # alors self._liste_champs_dispo est correct pour le FichierNfo :
        if isinstance(self.source, Renommable) and not self.dest:
            self.renomme(rep_cible)

    @classmethod
    def genere_nfo(cls, source_dict, template):
        # Pour le champ "description" on peut éventuellement utiliser
        # html.unescape() dans les libs par défaut.
        return template.render(**source_dict)
