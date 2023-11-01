# -*- coding: utf-8 -*-
"""Module pour la classe Emplacement qui relie position GPS et adresse.

Le passage de la position GPS à l'adresse et vice versa s'appelle en anglais le
"geocoding" (et "nominatim").
"""
import attr
from math import radians, cos, sqrt


@attr.s
class Emplacement(object):
    """Emplacement et conversion en différents formats."""

    latitude = attr.ib(default=0, converter=float)
    longitude = attr.ib(default=0, converter=float)
    adresse = attr.ib(default='')

    precision = attr.ib(kw_only=True, default='')
    qualite = attr.ib(kw_only=True, default='')
    numero_adresse = attr.ib(kw_only=True, default='')
    rue = attr.ib(kw_only=True, default='')
    ville = attr.ib(kw_only=True, default='')
    etat = attr.ib(kw_only=True, default='')
    pays = attr.ib(kw_only=True, default='')
    code_postal = attr.ib(kw_only=True, default='')

    # Attribut supplémentaire pour stocker un nom personnalisé, par ex :
    # "Maison" ou "Appartement Jihène" etc. que l'on pourra remplir à la main
    # ou à partir des contacts ou autre.
    nom_personnalise = attr.ib(kw_only=True, default='')

    def valide(self):
        """Renvoie si l'emplacement est valide ou non."""
        valide = False
        if (self.latitude and self.longitude) or self.adresse:
            valide = True
        return valide

    @classmethod
    def depuis_decimal(cls, decimal):
        """TODO."""
        return cls()

    @staticmethod
    def decimal_to_dms(decimal):
        """TODO."""
        decimal = float(decimal)
        decimal_abs = abs(decimal)
        minutes, seconds = (decimal_abs * 3600 / 60)
        degrees, minutes = (minutes / 60)
        degrees = degrees
        sign = 1 if decimal >= 0 else -1
        return (degrees, minutes, seconds, sign)

    @staticmethod
    def dms_to_decimal(degrees, minutes, seconds, direction=' '):
        """TODO."""
        sign = 1
        if(direction[0] in 'WSws'):
            sign = -1
        return (
            float(degrees) + (float(minutes) / 60)
            + (float(seconds) / 3600)
        ) * sign

    @staticmethod
    def dms_string(decimal, type='latitude'):
        """TODO."""
        # Example string -> 38 deg 14' 27.82" S
        dms = Emplacement.decimal_to_dms(decimal)
        if type == 'latitude':
            direction = 'N' if decimal >= 0 else 'S'
        elif type == 'longitude':
            direction = 'E' if decimal >= 0 else 'W'
        return '{} deg {}\' {}" {}'.format(dms[0], dms[1], dms[2], direction)

    def distance(self, lat, lon):
        """Renvoie une distance approximative avec une autre paire lat/lon.

        Cette distance n'est valable que pour des points proches.
        Ne pas l'utiliser pour des calculs précis et points éloignés.
        Récupéré de : https://github.com/jmathai/elodie/blob/master/elodie/localstorage.py#L142.  # noqa
        et http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points  # noqa

        :param lat:        latitude du point à mesurer
        :param longitude:  longitude du point à mesurer
        """
        # Conversion degrés "décimaux" en radians
        lon1, lat1, lon2, lat2 = list(map(
            radians,
            [lon, lat, self.longitude, self.latitude]
        ))

        r = 6371000  # radius of the earth in m
        x = (lon2 - lon1) * cos(0.5 * (lat2 + lat1))
        y = lat2 - lat1
        d = r * sqrt(x * x + y * y)
        return d
