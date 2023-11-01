"""Module de base pour les fichiers media.

On réfléchit à avoir une classe Fichier (qui serait Renommable), et une classe
Media (ou MetaDonnées) qui dit qu'on a des meta données inclues dedans.
Il faut notamment pouvoir tester si le filename qu'on passe est du bon format
que ce soit son extension ou son mimetype, voire carrément son contenu en
l'ouvrant (avec mutagen pour audio ou avec imghdr pour images)

.. moduleauthor:: marrco <marrco@wohecha.fr>
"""
import attr
import mimetypes
import os

try:  # Py3k compatibility
    basestring
except NameError:
    basestring = (bytes, str)


@attr.s
class Media(object):
    """Classe de base pour tous les media.

    :param str source: Chemin complet vers le fichier, TODO non mettre dans
        stockage, on pourrait avoir les données dans une base ou dans une url

    par contre garder empreinte pour avoir un uuid unique ou calculé

    garder extension ? si légitime ? ou juste dans stockage ... ?

    TODO commencer par faire juste les modeles sans dépendance, juste les
        structure
    """

    extensions = ()

    source = attr.ib(default=None)
    empreinte = attr.ib(init=False, default=None)

    metadonnees_ou_etiquettes = attr.ib()

    def __attrs_post_init__(self):
        """Initialisation."""
        self.raz_cache()

    @property
    def extension(self):
        """Renvoie l'extension du fichier.

        :returns: string
        """
        source = self.source
        return os.path.splitext(source)[1][1:].lower()

    def get_metadata(self, recharger_cache=False):
        """TODO est-ce qu'on fait ça ?? pour l'instant on l'utilise pas."""
        # TODO on peut remplacer ou l'utiliser pour avoir la liste des
        # metadonnees récupérées et/ou modifiables dans les Tags.
        if not self.is_valid():
            return None

        if isinstance(self.metadata, dict) and recharger_cache is False:
            return self.metadata

        source = self.filename

        self.metadata = {
            "date_taken": self.tags.date_prise_de_vue,
            "camera_make": self.tags.fabriquant_appareil,
            "camera_model": self.tags.modele_appareil,
            "latitude": self.tags.coordonnees("latitude"),
            "longitude": self.tags.get_coordinate("longitude"),
            "album": self.tags.album,
            "title": self.tags.titre,
            "mime_type": self.get_mimetype(),
            "original_name": self.tags.get_original_name(),
            "base_name": os.path.splitext(os.path.basename(source))[0],
            "extension": self.extension,
            "directory_path": os.path.dirname(source),
        }

        return self.metadata

    def get_mimetype(self):
        """TODO faire un lien avec MediaDetecteur."""
        if not self.is_valid():
            return None

        # TODO utiliser media_detecteur
        mimetype = mimetypes.guess_type(self.filename)

        return mimetype[0] if mimetype else None

    def is_valid(self):
        """Fonction générique pour vérifier si c'est un fichier du bon type.

        Compare avec la constante de classe "cls.extensions"

        :returns: bool
        """
        source = self.filename
        return os.path.splitext(source)[1][1:].lower() in self.extensions

    def raz_cache(self):
        """Remet le cache à zéro."""
        # self.metadata = None
        # TODO self.tags.raz_cache()
        # à condition que l'objet "Media" soit pour les objets qui ont des tags
