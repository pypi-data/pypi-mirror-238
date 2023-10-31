# -*- coding: utf-8 -*-
"""Module qui fournit les classes pour la manipulation des tags photo.

Notamment la classe :class:`ExifTags` pour les tags Exiftool.

Installation de exiftools :
https://www.sno.phy.queensu.ca/~phil/exiftool/install.html

.. moduleauthor:: marrco <marrco@wohecha.fr>
"""
import os
import attr
import re
from datetime import datetime
# Gestion des timezones :
import pytz
import tzlocal

# load modules
from automatheque.log import recup_logger
from automatheque.dependances.exiftool import ExifTool
from automatheque.modele.calendrier import Evenement

LOGGER = recup_logger(__name__)


@attr.s
class BaseTags(object):
    """Classe de base pour les Tags de photo."""

    extensions = ()
    # Attributs par défaut chargés dans les tags.
    # Si un type d'objet n'utilise pas tous les attributs (par ex pour les
    # éventuelles vidéos) alors il ne sera pas remonté.
    # TODO pour l'instant ça ne sert que dans le _pprint()
    ATTRIBUTS_CHARGES = (
        'album', 'evenement', 'auteur', 'date_prise_de_vue',
        'date_creation_fichier', 'date_modification_fichier',
        'latitude', 'longitude', 'timezone', 'pays', 'province_etat', 'ville',
        'lieu_quartier',
        'fabriquant_appareil', 'modele_appareil',
        'nom_origine', 'titre',
        'description', 'evaluation'
    )
    TIMEZONE_SEPARATEUR = "%"

    # Attribut dans le init pour conserver le nom du fichier traité :
    source = attr.ib(repr=False)
    attributs_charges = attr.ib(repr=False, default=attr.Factory(
        lambda self: self.ATTRIBUTS_CHARGES, takes_self=True))

    # Liste des metadonnées :
    album = attr.ib(init=False)
    evenement = attr.ib(init=False)
    auteur = attr.ib(init=False)
    date_prise_de_vue = attr.ib(init=False)
    date_creation_fichier = attr.ib(init=False)
    date_modification_fichier = attr.ib(init=False)
    coordonnees_gps = attr.ib(init=False)
    latitude = attr.ib(init=False)
    longitude = attr.ib(init=False)
    lieu_quartier = attr.ib(init=False)
    ville = attr.ib(init=False)
    province_etat = attr.ib(init=False)
    pays = attr.ib(init=False)
    fabriquant_appareil = attr.ib(init=False)
    modele_appareil = attr.ib(init=False)
    nom_origine = attr.ib(init=False)
    titre = attr.ib(init=False)
    description = attr.ib(init=False)
    evaluation = attr.ib(init=False)

    # Stockage des metadonnées brutes :
    _metadonnees = attr.ib(init=False, repr=False, factory=dict)

    def _pprint(self):
        # Fonction sale en attendant que attr puisse utiliser des callables.
        repr = 'Tags('
        for a in self.attributs_charges:
            repr += '{}={}, '.format(a, getattr(self, a))
        return repr + ')'

    # On utilise toutes ces "property" car les attributs existent et donc on
    # ne passerait pas par __getattr__ en les appelant. Si on veut supprimer
    # les property, alors il faut supprimer les attrib (ou surcharger
    # __getattribute__ mais c'est dangereux) TODO
    @property
    def album(self):
        """Renvoie la valeur de la propriété dans les metadonnées."""
        return self._album

    @property
    def evenement(self):
        """Renvoie la valeur de la propriété dans les metadonnées."""
        return self._evenement

    @property
    def auteur(self):
        """Renvoie la valeur de la propriété dans les metadonnées."""
        return self._auteur

    @property
    def date_prise_de_vue(self):
        """Renvoie la valeur de la propriété dans les metadonnées."""
        return self._date_prise_de_vue

    @property
    def date_creation_fichier(self):
        """Renvoie la date de création du fichier.

        :returns: time object or None for non-photo files or 0 timestamp
        """
        return self._date_creation_fichier

    @property
    def date_modification_fichier(self):
        """Renvoie la date de dernière modification du fichier.

        :returns: time object or None for non-photo files or 0 timestamp
        """
        return self._date_modification_fichier

    @property
    def coordonnees_gps(self):
        """Renvoie la valeur de la propriété dans les metadonnées."""
        return self._coordonnees_gps

    @property
    def latitude(self):
        """Renvoie la valeur de la propriété dans les metadonnées."""
        return self._latitude

    @property
    def longitude(self):
        """Renvoie la valeur de la propriété dans les metadonnées."""
        return self._longitude

    @property
    def timezone(self): return self._timezone

    @property
    def lieu_quartier(self): return self._lieu_quartier

    @property
    def ville(self): return self._ville

    @property
    def province_etat(self): return self._province_etat

    @property
    def pays(self): return self._pays

    @property
    def fabriquant_appareil(self):
        """Renvoie la valeur de la propriété dans les metadonnées."""
        return self._fabriquant_appareil

    @property
    def modele_appareil(self):
        """Renvoie la valeur de la propriété dans les metadonnées."""
        return self._modele_appareil

    @property
    def nom_origine(self):
        """Renvoie la valeur de la propriété dans les metadonnées."""
        return self._nom_origine

    @property
    def titre(self):
        """Renvoie la valeur de la propriété dans les metadonnées."""
        return self._titre

    @property
    def description(self): return self._description

    @property
    def evaluation(self): return self._evaluation

    def raz_cache(self):
        """Remise à zéro du cache des métadonnées."""
        self._metadonnees = None

    def _charge_tags(self):
        """Charge les tags depuis le fichier source.

        À surcharger

        :returns: :class:`Tags`
        """
        self._metadonnees = {}
        return self


@attr.s
class ExifTags(BaseTags):
    """Classe pour les tags manipulés par ExifTool.

    TODO : gérer les tags avec lang-alt : default : -x-default ou -fr (conf)
    on les appelle en ajoutant -fr au tag demandé directement.

    NB: on cherche à utiliser le mot clé "MWG:", voir :
        https://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/MWG.html
        Cela nécessite un traitement spécifique dans les getattr et setattr.
    """

    # En utilisant des attributs précédés d'un underscore on force
    # l'utilisation de __getattr__ qui vient ensuite chercher dans ce dict.
    EXIF_ASSOCIATIONS = {
        '_date_prise_de_vue': ["MWG:DateTimeOriginal"],
        '_date_creation_fichier': ["MWG:CreateDate"],
        '_date_modification_fichier': ["MWG:ModifyDate"],
        '_fabriquant_appareil': ['EXIF:Make', 'QuickTime:Make'],
        '_modele_appareil': ['EXIF:Model', 'QuickTime:Model'],
        '_album': ['XMP-xmpDM:Album', 'XMP:Album'],

        # TODO ajouter "subject" pour pouvoir faire le tag depuis decompose
        '_evenement': ['XMP:Event'],
        # En ajoutant "_struct" au bout du nom, on précise que l'on veut
        # récupérer le résultat sous forme de structure, telle que définie
        # par la norme dans exiftool ou par la configuration spécifique.
        '_evenement_struct': ['XMP:Evenement'],
        # Dans le cas présent :
        # XMP-Automatheque:Evenement Struct
        #    Field Name 	Writable
        #    -----------------------
        #    Etag       string
        #    Url        string
        #    Vevent     string
        # On utilise XMP:Evenement au lieu de XMP-Automatheque car pyexiftool
        # est exécuté par défaut avec "-G". Voir fichiers/exiftool.config.dist.

        '_titre': ['XMP:Title'],
        '_ville': ["MWG:City"],
        '_pays': ["MWG:Country"],
        '_province_etat': ["MWG:State"],
        '_lieu_quartier': ["MWG:Location"],
        '_auteur': ["MWG:Creator"],

        # GPS et timezones :from datetime timezone
        '_latitude': ['EXIF:GPSLatitude'],
        '_longitude': ['EXIF:GPSLongitude'],
        '_latitude_ref': ['EXIF:GPSLatitudeRef'],
        '_longitude_ref': ['EXIF:GPSLongitudeRef'],
        '_timezone': ['XMP:Timezone'],  # Custom tag d'automatheque :
        # Comme on n'est jamais sûr de parser correctement les dates exif/xmp
        # et autres, on préfère les laisser en "localtime" et stocker à part
        # la timezone (par ex: "Europe/Paris") que l'on utilisera pour parser
        # la date, dans XMP-Automatheque:Timezone. Si on ne trouve pas de
        # timezone dans les tags, on utilise la timezone locale.
        # Il existe aussi EXIF:GPSDateStamp et EXIF:GPSTimeStamp, stockée en
        # UTC, mais il faut utiliser GPSDateTime (composite) pour la lire, si
        # elle est présente.

        '_nom_origine': ['XMP:OriginalFileName'],
        '_description': ["MWG:Description"],
        '_evaluation': ["MWG:Rating"],
    }

    # Params supplémentaires lors de l'appel à exiftool
    exiftool_params = [
        '-overwrite_original',
        '-use',
        'MWG'
    ]

    # Spécificité pour la sauvegarde des tags gps :
    utiliser_gps_ref = attr.ib(init=False, default=True)

    def _pprint(self):
        """TODO en attendant que repr affiche les property."""
        r = super(ExifTags, self)._pprint()
        r = r[:-1]
        r += '{}={})'.format('utiliser_gps_ref', self.utiliser_gps_ref)
        return r

    def __getattr__(self, attribut):
        """Appelé quand l'attribut n'est pas trouvé.

        Pour un attribut demandé, renvoie la valeur des metadonnées. Or on n'a
        (exprès) pas créé les attributs commençant par des underscores :
        par ex "_album" n'existe pas, donc il passera par cette fonction.
        """
        # Traitement particulier pour les dates :
        est_date = attribut.startswith('_date')

        if attribut in self.EXIF_ASSOCIATIONS:
            if self._metadonnees is None:
                self._charge_tags()

            for nom_tag in self.EXIF_ASSOCIATIONS[attribut]:
                # Quand on veut lire des tags "MWG:XX" il faut changer leurs
                # noms car ils sont retournés par exiftool comme des
                # "Composite:XX". Pour les écrire en revanche on garde "MWG:".
                nom_tag = re.sub('MWG:', 'Composite:', nom_tag, flags=re.I)
                if nom_tag in self._metadonnees and not est_date:
                    return self._metadonnees[nom_tag]
                elif nom_tag in self._metadonnees and est_date:
                    val = self.recompose_datetime(self._metadonnees[nom_tag],
                                                  nom_tag)
                    if val is None:
                        continue
                    return val

            # Défaut si on n'a rien trouvé :
            if est_date:
                return pytz.utc.localize(
                    datetime.utcfromtimestamp(
                        min(os.path.getmtime(self.source),
                            os.path.getctime(self.source))))
            return None
        raise AttributeError(attribut)

    def __setattr__(self, name, value):
        """Surcharge de la mise à jour des attributs.

        Pour certains attributs on déclenche une action avant ou après les
        avoir mis à jour.
        """
        _name = '_{}'.format(name)  # Ajout de l'underscore pour le test
        if _name not in self.EXIF_ASSOCIATIONS:
            object.__setattr__(self, name, value)
            return
        if name == 'date_prise_de_vue':
            value = self._calc_date_prise_de_vue(value)
        if name == 'nom_origine':
            value = self._calc_nom_origine(value)
        if name == 'timezone':
            value = self._calc_timezone(value)

        tags = {}
        # On met à jour tous les tags que l'on lit pour être sûr de rendre
        # le fichier le plus facilement lisible par ailleurs.
        for nom_tag in self.EXIF_ASSOCIATIONS[_name]:
            tags[nom_tag] = value
            # On ajoute des tags dans certains cas :
            if name in ['latitude', 'longitude']:
                tags = self.__maj_tags_gps(tags, name, value)
            if name == 'evenement':
                if isinstance(value, Evenement):
                    tags[nom_tag] = value.titre
                tags.update(self.__maj_evenement(value))

        status = self.__maj_tags(tags, nom=name)
        self.raz_cache()
        return status

    @property
    def latitude(self):
        """Surcharge de la fonction de BaseTags.

        :returns: float or None if not present in EXIF or a non-photo file
        """
        direction_multiplier = 1.0
        # Cast coordinate to a float due to a bug in exiftool's
        #   -json output format.
        # https://github.com/jmathai/elodie/issues/171
        # http://u88.n24.queensu.ca/exiftool/forum/index.php/topic,7952.0.html  # noqa
        v = float(self._latitude) if self._latitude else None
        # TODO: verify that we need to check ref key
        #   when self.utiliser_gps_ref != True
        if self._latitude_ref == 'S':
            direction_multiplier = -1.0
        return v * direction_multiplier if v else None

    @property
    def longitude(self):
        """Surcharge de la fonction de BaseTags.

        :returns: float or None if not present in EXIF or a non-photo file
        """
        direction_multiplier = 1.0
        # Cast coordinate to a float due to a bug in exiftool's
        #   -json output format.
        # https://github.com/jmathai/elodie/issues/171
        # http://u88.n24.queensu.ca/exiftool/forum/index.php/topic,7952.0.html  # noqa
        v = float(self._longitude) if self._longitude else None
        # TODO: verify that we need to check ref key
        #   when self.utiliser_gps_ref != True
        if self._longitude_ref == 'W':
            direction_multiplier = -1.0
        return v * direction_multiplier if v else None

    @property
    def evenement(self):
        """Renvoie une instance de :class:`Evenement`, une chaîne ou None.

        Événement associé à l'objet taggé. C'est un événement de type
        :class:`~automatheque.modele.calendrier.evenement.Evenement`, qui
        contient le vobject VEvent (cf la norme icalendar).
        S'il n'y pas d'objet stocké, mais qu'il y a quand même une chaîne pour
        l'événement alors cette chaîne est retournée.
        """
        j = self._evenement_struct
        if j:
            return Evenement(
                etag=j['Etag'], url=j['Url'],
                vevent=j['Vevent'].encode('utf-8').decode('unicode_escape'))
        elif self._evenement:
            return self._evenement
        return None

    def __maj_evenement(self, valeur):
        """Un événement est une structure, donc on doit gérer spécifiquement.

        La structure est du format :
        {'etag': valeur.etag, 'url': valeur.url,
         'vevent': valeur.vevent.serialize()}
        en ligne de commande cela ferait :
        -tag="{etag=test2, url=testurl, vevent=test_vevent}"
        """
        tags = {}
        if isinstance(valeur, Evenement):
            for tag in self.EXIF_ASSOCIATIONS['_evenement_struct']:
                # Comme pyexiftool ne gère pas les structures on utilise
                # la fonctionnalité de exiftool qui permet d'accéder aux
                # éléments de la structure en concaténant ses parties (vision
                # "flat") : Evenement[Etag] => EvenementEtag
                # NB: ce n'est pas case-sensitive
                tags[tag + 'etag'] = valeur.etag
                tags[tag + 'url'] = valeur.url
                # Il faut échapper les "\n" dans les tags car ExifTool en mode
                # "-stay_open" les attrape sinon :
                tags[tag + 'vevent'] = (valeur.vevent.serialize()
                                        .encode('unicode_escape')
                                        .decode())
        # Cas où on veut supprimer l'événement:
        if not valeur:
            for tag in self.EXIF_ASSOCIATIONS['_evenement_struct']:
                tags[tag + 'etag'] = ''
                tags[tag + 'url'] = ''
                tags[tag + 'vevent'] = ''

        return tags

    def recompose_datetime(self, valeur, nom_tag=None):
        """Recompose une date à partir des metadonnées.

        TODO : pb si la date de modification du fichier n'est pas sur la
        meme timezone. Ceci dit on ne s'en sert pas .. on pourrait presque
        la supprimer !

        :returns: datetime objet ou None
        """
        _date = None
        timezone = self._timezone
        if timezone:
            try:
                tzinfo = pytz.timezone(timezone)
            except pytz.exceptions.UnknownTimeZoneError:
                LOGGER.warning("pytz erreur pour: {}".format(timezone))
        else:
            tzinfo = tzlocal.get_localzone()
        # TODO il semblerait que EXIFTOOL s'en charge :
        # https://sno.phy.queensu.ca/~phil/exiftool/faq.html#Q5

        # Un peu compliqué mais tous les formats de date ne sont pas stockés
        # avec le même formattage, donc soit on laisse datetime deviner, soit
        # on l'aide. Ce que l'on fait ici.
        # cf https://github.com/jmathai/elodie. <= que de l'exif
        # et https://github.com/photo/frontend/blob/master/src/libraries/models/Photo.php#L500  # noqa
        try:
            if(re.match(r'\d{4}(-|:)\d{2}(-|:)\d{2}', valeur) is not None):
                dt, tm = valeur.split(' ')
                dt_list = re.compile(r'-|:').split(dt)
                # le "." est le séparateur des microsecondes :
                tm_list = re.compile(r'-|:|\.').split(tm)
                try:  # les microsecondes doivent faire 6 caractères : .123456
                    tm_list[3] = tm_list[3].ljust(6, '0')  # donc on complete
                except IndexError:  # on ne fait rien s'il n'y en a pas
                    pass
                dt_list = dt_list + tm_list
                dt_list = map(int, dt_list)
                _date = datetime(*dt_list)
        except Exception:
            LOGGER.warning('impossible de décoder la date {} pour le tag {}'.format(valeur, nom_tag))  # noqa
            pass

        if(_date == 0):
            return None

        return tzinfo.localize(_date)

    def _charge_tags(self):
        """Charge les tags depuis le fichier source.

        Surcharge de :class:`Tags`.

        :returns: :class:`ExifTags`
        """
        metadonnees = {}

        def exec_json(et, args, metadonnees):
            """Factorisation des appels internes."""
            args = self.exiftool_params + args + [self.source]
            m = et.execute_json(*args)[0]
            if m:
                metadonnees.update(m)

        with ExifTool() as et:
            exec_json(et, [], metadonnees)
            # https://stackoverflow.com/a/33048483 concaténer des listes :
            for nom_tag in sum(self.EXIF_ASSOCIATIONS.values(), []):
                args = []
                # Pour charger les tags MWG il faut les réclamer explicitement
                # sinon ils n'apparaissent pas dans exiftool.
                if nom_tag.startswith('MWG:'):
                    args.append('-{}'.format(nom_tag.lower()))
                if args:
                    exec_json(et, args, metadonnees)
            for a in [a for a in self.EXIF_ASSOCIATIONS.keys()
                      if a.endswith('_struct')]:
                args = ['-struct']
                # Pour charger les tags de type "Structure" il faut préciser
                # '-struct' si on ne veut pas qu'exiftool les "déplie".
                for nom_tag in self.EXIF_ASSOCIATIONS[a]:
                    args.append('-{}'.format(nom_tag.lower()))
                if args:
                    exec_json(et, args, metadonnees)

        self._metadonnees = metadonnees
        return self

    def _calc_date_prise_de_vue(self, date_prise_de_vue):
        """Convertit la date de prise de vue en chaîne de caractère.

        C'est nécessaire car exiftool attend un certain format en entrée.
        En meme temps il a l'air assez souple, ptet qu'on pourrait rendre la
        fonction plus générique.
        TODO : https://sno.phy.queensu.ca/~phil/exiftool/faq.html#Q5

        On décide de ne pas stocker le timezone dedans, mais de le laisser
        dans _timezone.
        On pourrait remplir timezone à partir de la date de prise de vue, mais
        pour l'instant on s'en passe. Pour savoir si elle a une timezone :
        `automatheque.util.structures_python.date_est_naive()`

        :param datetime time: objet datetime de la date de prise de vue
        :returns: value
        """
        if(date_prise_de_vue is None):
            return None

        return date_prise_de_vue.strftime('%Y:%m:%d %H:%M:%S')

    def _calc_timezone(self, timezone,
                       separateur=BaseTags.TIMEZONE_SEPARATEUR):
        """Vérifie le format de timezone.

        On fait cela pour autoriser l'utilisation d'un autre caractère spécial
        que "/" pour la timezone, car si on veut le lire depuis un nom de
        fichier ou l'écrire dans un nom de fichier, les "/" ne sont pas
        autorisés. Par défaut on utilise "%" à la place.

        :param str timezone: chaîne de caractères qui représente une timezone
                             ex: Europe/Paris ou Europe%Paris
        :returns: value
        """
        return re.sub(r'{}'.format(separateur), '/', timezone)

    def _calc_nom_origine(self, nom_origine=None):
        """Renvoie le nom d'origine EXIF tag if not already set.

        :returns: True, False, None
        """
        # If EXIF original name tag is set then we return.
        if self.nom_origine is not None:
            return self.nom_origine

        if not nom_origine:
            nom_origine = os.path.basename(self.source)

        return nom_origine

    def __maj_tags_gps(self, tags, type, valeur):
        """Construit un dictionnaire de tags GPS à mettre à jour.

        Cette fonction est nécessaire car il faut parfois mettre à jour les
        tags qui stockent les "réferences" gps (=S/W). (quand les latitudes et
        longitudes sont des valeurs absolues !)
        cf : self.utiliser_gps_ref == True
        """
        if self.utiliser_gps_ref:
            if type == 'latitude' and valeur < 0:
                for tag in self.EXIF_ASSOCIATIONS['_latitude_ref']:
                    tags[tag] = 'S'

            if type == 'longitude' and valeur < 0:
                for tag in self.EXIF_ASSOCIATIONS['_latitude_ref']:
                    tags[tag] = 'W'

        return tags

    def __maj_tags(self, tags, nom=''):
        """Met à jour les tags donnés."""
        # TODO le faire aussi en passant les self._metadonnees
        # par ex dans la fonction : _ecrire_tags_dans_fichier

        # La première fois qu'on met à jour les tags on met à jour aussi le
        # le nom d'origine du fichier s'il n'en a pas.
        if self.nom_origine is None and nom != "nom_origine":
            self.nom_origine = self._calc_nom_origine()

        status = ''
        with ExifTool() as et:
            status = et.set_tags(tags, self.source, *self.exiftool_params)

        return status != ''
