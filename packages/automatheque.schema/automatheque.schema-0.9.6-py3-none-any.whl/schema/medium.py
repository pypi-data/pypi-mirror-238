from pathlib import Path

@attr.s
class Medium():
    """On peut trouver un nom un peu mieux sans doute.

    Il s'agit de la version "physique" (=fichier) des media gérés.
    
    classe abstraite pour s'assurer que le nom_fichier existe

    ATTENTION MAUVAISE idée de faire de l'héritage non ?
    si on veut plusieurs types de fichiers, il faudra plusieurs
    greffons pour gérer l'enregistrement dans différents types.

    TODO renommer en "StockageMedium", et ensuite sous classer par
    type de fichier "StockageCourrielEml(StockageMedium)"

    NB:  on pourrait en faire un de base, qui stocke le contenu
        dans un md, et les metadonnées en frontmatter ? qui prend
        en paramètre les propriétés que l'on veut mettre en frontmatter
        et celles que l'on veut mettre en MD.
    """
    chemin_fichier = attr.ib(validator=lambda x: isinstance(x, Path))

    # RENDRE OBLIGATOIRE SI VIDE !
    EXTENSIONS = []
    MIMETYPE = [] # ??

    def charge(self):
        if self.extension not in self.EXTENSIIONS:
            raise ValueError('Mauvaise extension')
        self._charge()

    def _charge(self):
        raise NotImplementedError()

    def sauvegarde(self):
        raise NotImplementedError()

