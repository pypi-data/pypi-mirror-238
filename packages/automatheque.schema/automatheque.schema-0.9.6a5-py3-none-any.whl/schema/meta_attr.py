#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Module pour gérer les meta attributs des fichiers passés par automatheque.

Si possible on écrit certaines informations dans les attributs étendus des
fichiers.
'''
from pathlib import PurePath
from xattr import xattr
from collections import defaultdict


class MetaAttr(object):
    """
    Classe qui sert à récupérer ou sauvegarder des meta attributs.

    La sauvegarde des attributs se fait pour l'instant uniquement dans
    Renommeur.renomme().

    TODO : décider si on l'initialise avec le fichier que l'on veut traiter,
    et si on charge d'office les infos meta dans l'objet, ou si on se contente
    d'appeler les classmethod dessus.

    TODO : on pourrait aussi étendre __getattr__ pour transformer les fonctions
    "sauvegardeXXXXX" en appel à _sauvegarde(cle, valeur) automatiquement ?
    Pour l'instant je préfère limiter moi même les fonctions autorisées.
    """

    XATTR_MODELE_CLASSE_CLE = 'user.automatheque.modele.classe'
    XATTR_FICHIER_ORIG_CLE = 'user.automatheque.fichier_orig'

    # TODO le veut on ?
    XATTR_FILEBOT_FILENAME_KEY = "net.filebot.filename"
    XATTR_FILEBOT_METADATA_KEY = "net.filebot.metadata"

    # TODO soit on stocke la classe soit l'objet serialisé ...
    # TODO on peut utiliser un registre des Media, cf dans MediaDetecteur.
    # Reste qu'on veut peut-être sérialiser l'objet.. (mais c'est un peu
    # intrusif) => le modele depuis le registre c'est peut-être le mieux,
    # il faudrait une fonction qui charge tous les média (en fonction de
    # charger_tags, charge_id3 etc.)
    XATTR_MODELE_CLASSE_VALEURS = defaultdict(str, (
        ('Episode', 'video.Episode'),
        ('Film', 'video.Film'),
        ('Chanson', 'audio.Chanson')
    ))

    @staticmethod
    def _recupereXattr(fichier, cle):
        # TODO le decode fonctionne pour python2 ?
        return xattr(fichier).get(cle).decode('utf-8')  # , namespace=xattr.NS_USER)

    @staticmethod
    def _sauvegardeXattr(fichier, cle, valeur):
        xattr(fichier).set(cle, valeur.encode('utf-8'))  # , namespace=xattr.NS_USER)

    @staticmethod
    def sauvegardeModeleClasse(fichier, classe):
        """Sauvegarde le modèle Automatheque utilisé dans les xattrs."""
        if MetaAttr.XATTR_MODELE_CLASSE_VALEURS[classe]:
            MetaAttr._sauvegardeXattr(
                fichier,
                MetaAttr.XATTR_MODELE_CLASSE_CLE,
                MetaAttr.XATTR_MODELE_CLASSE_VALEURS[classe])

    @staticmethod
    def recupereModeleClasse(fichier):
        """Renvoie une instance du modèle stocké dans les xattrs."""
        # TODO renommer recupereModeleInstance
        modele = MetaAttr._recupereXattr(
            fichier, MetaAttr.XATTR_MODELE_CLASSE_CLE)
        from pydoc import locate
        classe = locate('automatheque.modele.{}'.format(modele))
        return classe(fichier)

    @staticmethod
    def sauvegardeFichierOrig(fichier, fichier_orig):
        """Sauvegarde le nom du fichier d'origine dans les xattr."""
        if isinstance(fichier_orig, PurePath):
            fichier_orig = str(fichier_orig.resolve())
        MetaAttr._sauvegardeXattr(
            fichier, MetaAttr.XATTR_FICHIER_ORIG_CLE, fichier_orig)

    @staticmethod
    def recupereFichierOrig(fichier):
        MetaAttr._recupereXattr(fichier, MetaAttr.XATTR_FICHIER_ORIG_CLE)

    @staticmethod
    def sauvegardeMetaAttr(obj, fichier_orig):
        MetaAttr.sauvegardeModeleClasse(obj.filename, obj.__class__.__name__)
        MetaAttr.sauvegardeFichierOrig(obj.filename, fichier_orig)
