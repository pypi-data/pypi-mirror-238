# -*- coding: utf-8 -*-
"""Package destiné à gérer les musiques.
"""
from .tags import Id3Tags, MusicbrainzTags, Tags

from .chanson import Chanson

__all__ = [
    'Chanson',
    'Id3Tags',
    'MusicbrainzTags',
    'Tags'
]
