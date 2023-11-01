#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Module automatheque pour la gestion des chansons."""
from pathlib import Path
from unidecode import unidecode

# from enum import Enum
import attr

from mediafile import MediaFile, FileTypeError
import mutagen.id3
import mutagen.easyid3
import musicbrainzngs

# imports automatheque :
from automatheque.lib import Gabarit, Gabarits, Renommable
from automatheque.log import recup_logger
from automatheque.modele.audio import Tags
from automatheque.util import enleve_caracteres_invalides


LOGGER = recup_logger(__name__)


class FormatsChansonSupportes(object):  # Enum):
    """Liste des formats supportés par Chanson.

    Il s'agit de la liste des formats que mutagen peut gérer.
    """

    MP3 = 1
    # TODO ou alors demander à MediaFile ce qu'il arrive à gérer tout simplement?

    # TODO deplacer dans Tags ? ou import MediaFile ici aussi ?

    @classmethod
    def est_supporte(cls, nom_fichier):
        """Renvoie True si supporté, False sinon."""
        try:
            MediaFile(nom_fichier)
            return True
        except FileTypeError:
            return False


@attr.s
class Chanson(Renommable):
    """Classe représentant une chanson.

    TODO on ne considère que les tags ID3, on devrait en gérer +
    """

    filename = attr.ib()
    charger_tags = attr.ib(default=False, repr=False, cmp=False)
    acoustid_id = attr.ib(init=False, default="")
    # TODO : attr pourra donner un callback à repr, on pourra donner cela :
    # lambda x: '{:.10}'.format(x)
    acoustid_fingerprint = attr.ib(init=False, repr=False, default="")
    length = attr.ib(init=False, default="")
    # Utiliser factory au lieu de default sinon on partage la meme instance tag
    tags = attr.ib(init=False, factory=Tags)

    def __attrs_post_init__(self):
        """Methode magique de "attr" lancée après l'initialisation."""
        if self.charger_tags:
            self.charge_tags()

        self.ext = Path(self.filename).suffix[1:]  # on enleve le point

    def __setattr__(self, name, value):
        """Surcharge __setattr__ pour transformer les types de tags à la volée.

        Le but est de passer à Chanson des tags de type Id3Tags. DEPRECATED 
        """
        if name == "tags" and not isinstance(value, Tags):
            raise ValueError("tags doit être de type Tags")

        # Si notre tags est une instance de Tags, alors on peut déjà gérer tous les cas
        # grâce à MediaFile donc plus besoin de caster en Id3Tags
        #        elif name == "tags" and not isinstance(value, Id3Tags):
        #            value = Id3Tags(tags=value)
        object.__setattr__(self, name, value)

    def _ouvre_tags_fichier(self, v_easy=True):
        """Renvoie l'objet tags audio de mutagen pour le fichier manipulé.
        
        DEPRECATED MediaFile
        """
        try:
            if v_easy:
                v_audio = mutagen.easyid3.EasyID3(self.filename)
            else:
                v_audio = mutagen.id3.ID3(self.filename)
        except mutagen.id3.ID3NoHeaderError:  # Si le fichier n'a pas de tags
            v_audio = mutagen.File(self.filename, easy=v_easy)
            try:
                v_audio.add_tags()
            except:  # cela signifie que File n'a pas trouvé le type de fichier
                try:  # dernière chance : on essaie de le trouver nous-mêmes :
                    if ".mp3" in self.filename:
                        v_audio = mutagen.mp3.EasyMP3(self.filename)
                        try:
                            v_audio.add_tags()
                        except mutagen.id3.error:
                            pass
                    else:
                        raise
                except:
                    raise ValueError(
                        "mutagen ne peut pas déterminer le type du fichier"
                    )
        except Exception as e:
            raise ValueError("erreur ouverture du fichier avec mutagen : {}".format(e))

        return v_audio

    @classmethod
    def _gabarits_par_defaut(cls):
        """Surcharge de la fonction de Renommable.

        Renvoie une instance de Gabarits.
        """
        gabarits = Gabarits()
        defaut = [
            {
                "squelette": "{album} - ({date}) - CD{cd:02d}/{album} ({date}) - CD{cd:02d} - {num_piste:02d}. {artistes} - {titre_piste}.{ext}",
                "condition": "{nb_cd} >= 2 and {compilation}",
                "ordre": 1,
            },
            {
                "squelette": "{album} - ({date})/{album} ({date}) - {num_piste:02d}. {artistes} - {titre_piste}.{ext}",
                "condition": "{compilation}",
                "ordre": 1,
            },
            {
                "squelette": "{artiste}/{artiste} - ({date}) {album} - CD{cd:02d}/{album} ({date}) - CD{cd:02d} - {num_piste:02d}. {artistes} - {titre_piste}.{ext}",
                "condition": "{nb_cd} >= 2",
                "ordre": 2,
            },
            {
                "squelette": "{artiste}/{artiste} - ({date}) {album}/{album} ({date}) - {num_piste:02d}. {artistes} - {titre_piste}.{ext}",
                "condition": "",
                "ordre": 3,
            },
        ]
        for elem in defaut:
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
        champs = {
            "artiste": self.tags.albumartist,
            "album": self.tags.album,
            "compilation": self.tags.compilation,
            "date": self.tags.original_year,
            "cd": self.tags.discnumber,
            "nb_cd": self.tags.totaldiscs,
            "num_piste": self.tags.tracknumber,
            "artistes": self.tags.artist,
            "titre_piste": self.tags.title,
            "ext": self.ext,
        }
        return {
            key: enleve_caracteres_invalides(value) for (key, value) in champs.items()
        }

    def charge_tags(self):
        """Charge les tags du fichier dans l'objet.

        Lit les tags du fichier et peuple self.tags avec les tags trouvés.
        """
        # DEPRECATED v_audio = self._ouvre_tags_fichier()

        self.tags.charge_tags(self.filename)  # DEPRECATED : v_audio)

        for tag in ["length", "acoustid_fingerprint", "acoustid_id"]:
            try:
                setattr(self, tag, getattr(self.tags, tag))
            except Exception:
                pass

    def tags_pour_mutagen(self):
        """Génère une liste de tags compréhensible par mutagen.
        
        DEPRECATED avec mediafile
        """
        res = self.tags.format_sauvegarde()
        res.update(
            {
                "length": self.length,
                "acoustid_id": self.acoustid_id,
                "acoustid_fingerprint": self.acoustid_fingerprint,
            }
        )
        return res

    def sauvegarder_tags_dans_fichier(self):
        """Enregistre les Tags de self.tags dans le fichier audio."""

        # gestion des images :
        # TODO utiliser un plugin pour l'image au lieu de musicbrainz direct
        if self.tags.cover and self.tags.musicbrainz_releaseid:
            LOGGER.debug("... integration image")
            self.tags.ajout_image(
                musicbrainzngs.get_image_front(
                    self.tags.musicbrainz_releaseid, size=None
                ),
                "front",
            )

        # self.tags.length: self.length,
        self.tags.acoustid_id = self.acoustid_id
        self.tags.acoustid_fingerprint = self.acoustid_fingerprint

        self.tags.save(self.filename)
        return

        try:
            v_audio = self._ouvre_tags_fichier()
            v_audio.delete()

            for v_id3tag, v_valeur in self.tags_pour_mutagen().items():
                try:
                    v_audio[v_id3tag] = "%s" % (v_valeur)
                except Exception:
                    LOGGER.exception(
                        "[E] Copie tags cible : {} - {}".format(v_id3tag, v_valeur)
                    )
                    raise
            v_audio.save()

            # gestion des images :
            # TODO utiliser un plugin pour l'image au lieu de musicbrainz direct
            if self.tags.cover and self.tags.musicbrainz_releaseid:
                LOGGER.debug("... integration image")
                v_audio = self._ouvre_tags_fichier(v_easy=False)
                v_imgcover = musicbrainzngs.get_image_front(
                    self.tags.musicbrainz_releaseid, size=None
                )
                v_audio.add(
                    mutagen.id3.APIC(
                        encoding=3,
                        mime="image/jpeg",
                        type=3,
                        desc=u"Cover",
                        data=v_imgcover,
                    )
                )
                v_audio.save()
        except Exception as e:
            raise ValueError("[E] sauvegarder_tags_dans_fichier {}".format(e))

