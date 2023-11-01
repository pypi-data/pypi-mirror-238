#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Module automatheque pour la gestion des tags audio."""
from collections import defaultdict
from datetime import date, datetime
from dateutil.parser import parse as date_parse
import re
from unidecode import unidecode

import attr
import musicbrainzngs  # TODO devrait fonctionner en plugin ou dépendance !
from mediafile import MediaFile, Image

from automatheque.log import recup_logger

LOGGER = recup_logger(__name__)


class TagsDict(dict):
    """Classe qui sert juste à modifier l'affichage du defaultdict des tags.
    
    MediaFile.art est un gros blob qu'il vaut mieux éviter d'afficher.
    """

    def __init__(self):
        for f in list(MediaFile.fields()):
            self[f] = None
        self["images"] = []
        self["genre"] = []

    def __repr__(self):
        def reduit_champs(k, v):
            v = f"{str(v):.15}" if k in ["acoustid_fingerprint", "art"] and v else v
            return v

        return str({k: reduit_champs(k, v) for k, v in self.items()})


@attr.s
class Tags(object):
    # Mapping des tags utilisés dans automatheque et ceux de MediaFile
    # TODO on pourrait essayer de tout basculer vers mediafile mais
    # il faut tout revoir donc ce sera pour plus tard ....
    MAPPING = {
        "musicbrainz_releaseid": "mb_albumid",
        "musicbrainz_recordingid": "mb_trackid",
        "tracknumber": "track",
        "totaltracks": "tracktotal",
        "discnumber": "disc",
        "totaldiscs": "disctotal",
        "releasecountry": "country",
    }

    _mediafile = attr.ib(init=False, repr=False, default=None)
    _tags = attr.ib(init=False, factory=TagsDict)
    compilation = attr.ib(init=False, default=0)
    releasetotaltracks = attr.ib(init=False, default=0)
    # Si on doit mettre une cover ou pas
    cover = attr.ib(init=False, repr=False, cmp=False, default=False)

    def charge_tags(self, filename):
        """Liste des tags gérés par MediaFile :

        title ,
        artist ,
        album ,
        genres ,
        genre = genres.single_field(),

        lyricist ,
        composer ,
        composer_sort ,
        arranger ,

        grouping ,
        track ,
        tracktotal ,
        disc ,
        disctotal ,
        lyrics ,
        comments ,
        bpm ,
        comp ,
        albumartist ,
        albumtype ,
        label ,
        artist_sort ,
        albumartist_sort ,
        asin ,
        catalognum ,
        barcode ,
        disctitle ,
        encoder ,
        script ,
        language ,
        country ,
        albumstatus ,
        media ,
        albumdisambig ,

        # Release date.
        date ,

        year = date.year_field(),
        month = date.month_field(),
        day = date.day_field(),

        # *Original* release date.
        original_date ,

        original_year = original_date.year_field(),
        original_month = original_date.month_field(),
        original_day = original_date.day_field(),

        # Nonstandard metadata.
        artist_credit ,
        albumartist_credit ,

        # Acoustid fields.
        acoustid_fingerprint,
        acoustid_id,

        # ReplayGain fields
        rg_track_gain ,
        rg_album_gain,
        rg_track_peak,
        rg_album_peak,

        # EBU R128 fields.
        r128_track_gain,
        r128_album_gain,

        initial_key,

        # Properties
        def length,
        def samplerate,
        def bitdepth,
        def channels,
        def bitrate,
        def format = A string describing the file format/codec.

        """
        self._mediafile = MediaFile(filename)
        for f in self._mediafile.fields():
            setattr(self, f, getattr(self._mediafile, f))

        return self

    def save(self, filename):
        if not self._mediafile:
            self._mediafile = MediaFile(filename)
        self._mediafile.update({k: v for k, v in self._tags.items() if v})
        self._mediafile.save()

    def ajout_image(self, data, image_type="front"):
        if image_type == "front":
            mediafile_image_type = 3
        im = Image(data, type=mediafile_image_type)
        self.images.append(im)

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            if name == "_tags":
                raise AttributeError  # on ne veut pas de self._tags["_tags"]
            # Mappings depuis "Tags" automatheque déjà utilisés vers _tags mediafile :
            name = Tags.MAPPING[name] if name in Tags.MAPPING else name
            try:
                return self._tags[name]
            except KeyError as e:
                raise AttributeError from e

    def __setattr__(self, name, value):
        """Surcharge de la mise à jour des attributs.

        Pour certains attributs on déclenche une action avant ou après les
        avoir mis à jour.
        """
        if name in [
            "_mediafile",
            "_tags",
            "compilation",
            "cover",
            "releasetotaltracks",
        ]:
            object.__setattr__(self, name, value)
        else:
            if name == "date" and value and not isinstance(value, date):
                raise ValueError(date)
            name = Tags.MAPPING[name] if name in Tags.MAPPING else name
            self._tags[name] = value
        if name in ["date", "year", "month", "day"]:
            self._autocalc_dates(name)

    def __json__(self):
        """Sérialise en json.

        Fonction privée appelée par json.dumps quand on utilise
        :class:`~automatheque.util.nestorjsonencoder.NestorJSONEncoder`
        """
        return self.__dict__

    def _autocalc_dates(self, champ):
        """Détermine le tag originaldate.

        Déclenché automatiquement quand la date est modifiée.
        """
        if self.date and champ == "date":
            self.year = self.date.year
            if not re.findall(r"(18\d\d|19\d\d|20\d\d)", str(self.year)):
                ValueError("date au mauvais format")
            self.month = self.date.month
            self.day = self.date.day

        if not self.original_date and self.date and champ == "date":
            self.original_date = self.date
        if not self.original_year and self.year and champ in ["date", "year"]:
            # donc self.date ou self.year on été setté, donc je peux :
            self.original_year = self.year
        if (
            not self.original_month
            and self.month
            and champ in ["date", "year", "month"]
        ):
            self.original_month = self.month
        if (
            not self.original_day
            and self.day
            and champ in ["date", "year", "month", "day"]
        ):
            self.original_day = self.day


@attr.s
class TagsBak(object):
    """Classe de base pour la gestion des tags audio.

    TODO : se rapprocher de ça : https://picard.musicbrainz.org/docs/mappings/
    Il faudrait plusieurs modules en fonction du système de tags utilisé par
    le fichier, et charger les mappings correspondants pour remplir la
    structure.
    Il faudrait aussi renommer les attributs de Tags pour prendre les mêmes que
    picard !
    """

    # Attribut utilisé uniquement pour l'initialisation depuis un autre objet:
    tags = attr.ib(repr=False, cmp=False, default=None)

    # Attributs :
    # NB: par défaut on donne des valeurs "int" ou "str" aux attributs afin de
    # faciliter l'écriture des tags suivant les formats et aussi le renommage
    # des chansons en "str".
    album = attr.ib(init=False, default="")
    title = attr.ib(init=False, default="")
    artist = attr.ib(init=False, default="")
    albumartist = attr.ib(init=False, default="")
    compilation = attr.ib(init=False, default=0)
    date = attr.ib(init=False, default="")
    originaldate = attr.ib(init=False, repr=False, cmp=False, default="")
    tracknumber = attr.ib(init=False, default=0)
    totaltracks = attr.ib(init=False, default=0)
    discnumber = attr.ib(init=False, default=0)
    totaldiscs = attr.ib(init=False, default=0)
    releasecountry = attr.ib(init=False, default="")
    media = attr.ib(init=False, default="")
    # musicbrainz_albumid dans picard:
    musicbrainz_releaseid = attr.ib(init=False, default="")
    # musicbrainz_trackid dans picard:
    musicbrainz_recordingid = attr.ib(init=False, default="")
    # Spécifique à autotag :
    releasetotaltracks = attr.ib(init=False, default=0)
    # Passer à True si l'on doit intégrer une cover:
    cover = attr.ib(init=False, repr=False, cmp=False, default=False)

    def __attrs_post_init__(self):
        """Fonction exécutée par attrs après l'initialisation."""
        if self.tags is not None:
            for attribut in self.tags.__dict__.keys():
                if attribut == "tags":
                    continue
                try:
                    object.__setattr__(self, attribut, getattr(self.tags, attribut))
                except Exception:
                    pass

    def __setattr__(self, name, value):
        """Surcharge la mise à jour des attributs.

        Pour certains attributs on déclenche une action avant ou après les
        avoir mis à jour.
        """
        object.__setattr__(self, name, value)
        if name == "date":
            self._autocalc_year()

    def __json__(self):
        """Sérialise en json.

        Fonction privée appelée par json.dumps quand on utilise
        :class:`~automatheque.util.nestorjsonencoder.NestorJSONEncoder`
        """
        return self.__dict__

    def _autocalc_year(self):
        """Détermine le tag originaldate.

        Déclenché automatiquement quand la date est modifiée.
        """
        try:
            for v_year in re.findall(r"(18\d\d|19\d\d|20\d\d)", self.date):
                self.originaldate = v_year
                break
        except AttributeError:  # si self.date n'est pas encore initialisée
            pass

    def charge_tags(self, infos):
        """À surcharger par les descendants."""
        raise NotImplementedError("À surcharger par les descendants")

    def format_sauvegarde(self):
        """À Surcharger par les descendants.

        Renvoie un hash avec les tags nommés et formattés correctement pour le
        type de :class:`Tags` manipulé.
        """
        raise NotImplementedError("À surcharger par les descendants")


class Id3Tags(Tags):
    """Sous classe de Tags pour les tags ID3.

    Permet de faire le lien entre les champs ID3 et les champs internes de
    :class:`Tags`.
    """

    LISTE_TAGS = [
        "title",
        "artist",
        "album",
        "albumartist",
        "date",
        "compilation",  # https://help.mp3tag.de/main_tags.html#TCMP
        "releasecountry",
        "discnumber",
        "tracknumber",
        "media",
        "musicbrainz_trackid",
        "musicbrainz_albumid",
    ]

    def charge_tags(self, v_audio):
        """Charge les tags du fichier dans l'objet.

        Lit les id3 du fichier (fournis) et peuple self avec les tags id3
        trouvés.
        """
        for tag in Id3Tags.LISTE_TAGS:
            try:
                setattr(self, tag, unidecode(v_audio[tag][0]))
            except Exception:
                pass
        return self

    def __setattr__(self, name, value):
        """Surcharge de la mise à jour des attributs.

        Pour certains attributs on déclenche une action avant ou après les
        avoir mis à jour.
        """
        # TODO si on veut remplacer par un simili "switch/case" :
        # https://bytebaker.com/2008/11/03/switch-case-statement-in-python/
        if name == "tracknumber":
            value = self._autocalc_tracknumber(value)
        if name == "totaltracks":
            value = self._autocalc_totaltracks(value)
        if name == "discnumber":
            value = self._autocalc_discnumber(value)
        if name == "compilation":
            value = int(value)
        if name == "musicbrainz_albumid":
            name = "musicbrainz_releaseid"
        if name == "musicbrainz_trackid":
            name = "musicbrainz_recordingid"
        Tags.__setattr__(self, name, value)

    def _autocalc_tracknumber(self, tracknumber):
        """Formatte le tracknumber pour ID3.

        Fonction spécifique aux tags ID3 qui stockent le tracknumber sous la
        forme tracknumber/totaltracks (ex: "1/12")
        """
        try:
            # On initialise avec la valeur par défaut si elle existe
            res = self.tracknumber
        except Exception:
            res = None
        # Recherche des tracknumber et totaltracks sous la forme 1/10
        try:
            for (v_tracknumber, v_totaltracks) in re.findall(
                r"(\d+)/(\d+)", tracknumber
            ):
                res = int(v_tracknumber)
                # retourne dans __setattr__
                self.totaltracks = int(v_totaltracks)
                break
        except:
            pass

        # si non trouve : variantes
        if not res:
            try:
                res = int(tracknumber)
            except:
                res = tracknumber

        return res

    def _autocalc_totaltracks(self, totaltracks):
        """Remplit totaltracks en fonction des informations présentes.

        On ne le remplit pas s'il a déjà été rempli par _autocalc_tracknumber.
        """
        try:
            res = self.totaltracks  # On initialise avec la valeur par défaut
        except Exception:
            res = None

        if not res:
            try:
                res = int(totaltracks)
            except Exception:
                pass

        return res

    def _autocalc_discnumber(self, discnumber):
        """Formatte le discnumber pour ID3.

        Fonction spécifique aux tags ID3 qui stockent le discnumber sous la
        forme discnumber/totaldiscs (ex: "1/2")
        """
        try:
            # On initialise avec la valeur par défaut si elle existe
            res = self.discnumber
        except AttributeError:
            res = None
        # Recherche des discnumber et totaldiscs sous la forme 1/2
        try:
            for (v_discnumber, v_totaldiscs) in re.findall(r"(\d+)/(\d+)", discnumber):
                res = int(v_discnumber)
                # retourne dans __setattr__
                self.totaldiscs = int(v_totaldiscs)
                break
        except Exception:
            pass

        # si non trouve : variantes
        if not res:
            try:
                res = int(discnumber)
            except Exception:
                res = discnumber

        return res

    def format_sauvegarde(self):
        """Renvoie un hash avec les valeurs mappées au format id3.

        TODO creer une sous classe TagsID3 et faire le __setattr__ avec le mapping
        et le getattr aussi , avec une TAGLIST à parcourir qui liste les champs ID3

        Voir là : https://github.com/quodlibet/mutagen/blob/master/mutagen/easyid3.py#L523  # noqa
        """
        res = {
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "albumartist": self.albumartist,
            "compilation": self.compilation,
            "date": self.date,
            "originaldate": self.originaldate,
            "media": self.media,
            "discnumber": "{}/{}".format(self.discnumber, self.totaldiscs),
            "tracknumber": "{}/{}".format(self.tracknumber, self.totaltracks),  # noqa
            "releasecountry": self.releasecountry,
            "musicbrainz_albumid": self.musicbrainz_releaseid,
            "musicbrainz_trackid": self.musicbrainz_recordingid,
        }
        return res


class MusicbrainzTags(Tags):
    """Sous classe de Tags pour les tags récupérés depuis musicbrainz.

    Peut ensuite être donnée directement à Chanson.tags pour les intégrer dans
    le fichier.
    """

    # Liste des noms d'artistes utilisés pour des "compilations":
    LISTE_COMPILATIONS = [
        "Various Artists",
        "[christmas music]",
        "[Disney]",
        "[theatre]",
        "[classical music]",
        "[soundtrack]",
    ]
    ARTISTE_COMPILATION = "Various Artists"
    VIDE = "non present dans la liste des compilations"  # chaîne random !

    def __init__(self, relid, recid, tags=None):
        """Initialisation.

        :param relid: releaseid de musicbrainz
        :param recid: recordingid de musicbrainz
        :param tags: si présent charge les tags donné dans l'objet
                     MusicbrainzTags
        """
        super(MusicbrainzTags, self).__init__()  # deprecated : tags)
        self.musicbrainz_releaseid = relid
        self.musicbrainz_recordingid = recid
        musicbrainzngs.set_useragent(
            "Example music app", "0.1", "http://example.com/music"
        )
        # Stocker les infos récupérées de musicbrainz.com :
        self._cache = {"release": None, "recording": None}

    def charger_tags(self):
        """Charge les tags depuis musicbrainz.com.

        TODO : changer le nom pour "charge_tags", et charger_tags reste
        l'attribut du la classe pour charger à l'initialisation. (cf photos)
        TODO : ou plutot changer le nom pour "récupérer_tags" vu qu'on "fetch"
        depuis internet.
        En fait on mélange des tags "enregistrés" dans le fichier, et des tags
        "scrapés" depuis internet... on pourrait les séparer et faire des
        adaptateurs.
        """
        LOGGER.debug(
            "... Musicbrainz.charger_tags : relid=%s, recid=%s"
            % (self.musicbrainz_releaseid, self.musicbrainz_recordingid)
        )

        try:
            self._cache.update(
                musicbrainzngs.get_recording_by_id(
                    self.musicbrainz_recordingid, includes="artists"
                )
            )
            self._cache.update(
                musicbrainzngs.get_release_by_id(
                    self.musicbrainz_releaseid,
                    includes=["recordings", "artist-credits"],
                )
            )

            # Maintenant que les tags sont téléchargés, on les charge dans
            # l'objet :
            # TODO on pourrait faire un @property sur cache qui charge depuis
            # internet si vide ? mais alors il faut séparer les 2 ?
            # histoire de pouvoir donner directement le dict release et éviter
            # des appels superflus à musicbrainz.
            self.charge_tags(self._cache)

        except Exception as e:
            raise ValueError(f"[E] charger_tags : {e!r}")

    def charge_tags(self, infos):
        """Charge les tags depuis "infos" ou depuis l'objet.

        :param infos: dict {'release': , 'recording': } avec les infos à
                      charger dans l'objet; si on force infos à None alors on
                      utilise les valeurs de self._cache
        """
        if infos is None:
            infos = self._cache
        self._charge_release(infos["release"])
        self._charge_recording(infos["recording"])

    def _charge_release(self, details_rel):
        """Remplit les attributs de Tags à partir des valeurs de la release."""
        # verification du lien entre recording et release
        for v_medium in details_rel["medium-list"]:
            self.releasetotaltracks += int(v_medium["track-count"])
            for v_track in v_medium["track-list"]:
                if v_track["recording"]["id"] == self.musicbrainz_recordingid:
                    # Pour éviter les multiples try/except on utilise .get()
                    self.tracknumber = int(
                        v_track.get("position", self.tracknumber or 0)
                    )
                    self.totaltracks = int(v_medium.get("track-count", 1))
                    self.discnumber = int(v_medium.get("position", 1))
                    self.totaldiscs = int(details_rel.get("medium-count", 1))
                    self.media = v_medium.get("format", self.media)
                    break

        if not self.tracknumber:
            raise ValueError("[E] Aucun tracknumber")

        self.releasecountry = details_rel.get("country", self.releasecountry)
        d = details_rel.get("date", self.date)
        try:
            self.date = datetime.strptime(d, "%Y-%m-%d")
        except ValueError:
            try:
                res = datetime.strptime(d, "%Y-%m")
                self.year, self.month = (res.year, res.month)
            except ValueError:
                res = datetime.strptime(d, "%Y")
                self.year = res.year

        try:
            self.album = details_rel["title"]
        except KeyError:
            raise ValueError("[E] aucun titre d'album trouve")

        try:
            if details_rel["cover-art-archive"]["front"] == "true":
                self.cover = True
        except KeyError:
            pass

        try:
            self.albumartist = details_rel["artist-credit"][0]["artist"][
                "name"
            ]  # TODO ou utiliser artist-credit-phrase en entier ? si elle existe pour la release
        except Exception:
            pass
        if (
            details_rel.get("artist-credit-phrase", MusicbrainzTags.VIDE)
            in MusicbrainzTags.LISTE_COMPILATIONS
        ):
            self.compilation = 1  # Voir pourquoi "1" dans `Tags`
            self.albumartist = MusicbrainzTags.ARTISTE_COMPILATION

    def _charge_recording(self, details_rec):
        """Remplit les attributs de Tags avec les valeurs du "recording"."""
        # TODO vérifier : https://picard.musicbrainz.org/docs/mappings/
        if not self.compilation and not self.albumartist:
            try:
                self.albumartist = details_rec["artist-credit"][0]["artist"]["name"]
            except Exception:
                pass

        self.artist = details_rec.get("artist-credit-phrase", self.artist)
        self.title = details_rec.get("title", self.title)

