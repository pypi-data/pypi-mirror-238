"""Module pour gérer les événements du calendrier."""
from datetime import datetime
from collections import defaultdict

import attr
import vobject
import pytz

from automatheque.util.structures_python import date_en_datetime


@attr.s
class Evenement(object):
    """Représente un événement dans le calendrier.

    Se base principalement sur vobject qui est utilisé par caldav et par
    radicale.
    """

    # Attributs spécifiques à caldav
    etag = attr.ib()
    url = attr.ib()
    # VEVENT
    vevent = attr.ib()  # VOBJECT qui represente l'evenement

    # Propriétés cosmétiques pour visualiser certaines valeurs de vevent plus
    # facilement.
    date_debut = attr.ib(init=False, default=None)
    date_fin = attr.ib(init=False, default=None)
    titre = attr.ib(init=False, default=None)

    def __attrs_post_init__(self):
        """Dé-sérialise le vobject utilisé pour le vevent."""
        if isinstance(self.vevent, str):
            self.vevent = vobject.readOne(self.vevent)

    @property
    def date_debut(self):
        """Renvoie une datetime."""
        return date_en_datetime(self.vevent.dtstart.value)

    @property
    def date_fin(self):
        """Renvoie une datetime."""
        date_fin = None
        if self.vevent.dtend.value:
            date_fin = self.vevent.dtend.value
        elif self.vevent.duration.value:
            # TODO il nous faut un exemple et on calculera la date de fin
            # à partir de la date de début et la durée.
            # Reste le cas des événements récurrents ... :thinking_face:
            raise NotImplementedError
        return date_en_datetime(date_fin)

    @property
    def _date_fin_diff_court(self):
        """Version courte de la date de fin.

        Pas beaucoup d'intérêt on pourrait le gérer avec des règles de
        renommage. Mais cela simplifie le code pour les champs de photo
        précalculés.
        ex: 04-12, si date_debut = 2018-03-14 et date_fin = 2018-04-12
        """
        date_fin_diff_court = []
        if self.date_debut.year != self.date_fin.year:
            date_fin_diff_court.append(self.date_fin.year)
        if self.date_debut.month != self.date_fin.month:
            date_fin_diff_court.append(self.date_fin.month)
        if self.date_debut.day != self.date_fin.day:
            date_fin_diff_court.append(self.date_fin.day)

        return date_fin_diff_court

    @property
    def titre(self):
        """Renvoie une date ou datetime."""
        return self.vevent.summary.value


def json_en_vobject(json):
    """Retourne un vobject à partir du json donné.

    JSON extrait de Google Calendar pour l'instant.
    ex:
    ```
    {'kind': 'calendar#events', 'etag': '"p330ftucghr3ts0g"',
     'summary': 'JAPAN', 'updated': '2018-11-09T10:33:33.960Z',
     'timeZone': 'Asia/Tokyo', 'accessRole': 'writer', 'defaultReminders': [],
     'nextSyncToken': 'CMD--ZCOx94CEMD--ZCOx94CGAQ=',
     'items': [
        {'kind': 'calendar#event', 'etag': '"2687374532000000"',
         'id': 'xxxid', 'status': 'confirmed',
         'htmlLink': 'https://www.google.com/calendar/event?eid=zzzid&ctz=Europe/Brussels',
         'created': '2012-07-30T22:23:22.000Z', 'updated': '2012-07-30T22:27:46.000Z',
         'summary': 'Arrivee Osaka', 'location': 'Osaka', 'colorId': '5',
         'creator': {'email': 'yyyyy@gmail.com', 'displayName': 'Gaelle M'},
         'organizer': {'email': 'xxxid@group.calendar.google.com',
            'displayName': 'JAPAN 2013', 'self': True},
         'start': {'dateTime': '2013-03-17T01:00:00+01:00', 'timeZone': 'Asia/Tokyo'},
         'end': {'dateTime': '2013-03-17T04:00:00+01:00', 'timeZone': 'Asia/Tokyo'},
         'iCalUID': 'xxxid@google.com', 'sequence': 0,
         'reminders': {'useDefault': True}},
        {'kind': 'calendar#event', 'etag': '"2859385261594000"',
        'id': 'zzzzzzzzz', 'status': 'confirmed',
        'htmlLink': 'https://www.google.com/calendar/event?eid=xxxxx&ctz=Europe/Brussels',
        'created': '2015-03-11T15:42:23.000Z', 'updated': '2015-04-22T08:50:30.797Z',
        'summary': 'JRPASS', 'colorId': '4',
        'creator': {'email': 'yyyyy@gmail.com', 'displayName': 'John S.'},
        'organizer': {'email': 'zzzzzzzzz@group.calendar.google.com',
            'displayName': 'JAPAN', 'self': True},
        'start': {'date': '2015-05-09'}, 'end': {'date': '2015-05-16'},
        'transparency': 'transparent',
        'iCalUID': 'zzzzzzzzz@google.com', 'sequence': 5,
        'reminders': {'useDefault': False}}
     ]}
    ```
    """
    decompose_un(json)


def decompose_un(json_):
    """Décompose le json en vcalendar ou vevent."""
    json = defaultdict(str)
    json.update(json_)  # on evite les "key errors"
    v = None

    if json['kind'] == 'calendar#events':
        v = vobject.iCalendar()
        for item in json['items']:
            vevent = decompose_un(item)
            v.add(vevent)
    if json['kind'] == 'calendar#event':
        vevent = vobject.newFromBehavior('vevent')
        vevent.add('uid').value = json['iCalUID']
        vevent.add('status').value = json['status']
        vevent.add('resources').value = [json['htmlLink']]
        vevent.add('created').value = pytz.utc.localize(
            datetime.strptime(json['created'], '%Y-%m-%dT%H:%M:%S.%fZ'))
        vevent.add('last-modified').value = pytz.utc.localize(
            datetime.strptime(json['updated'], '%Y-%m-%dT%H:%M:%S.%fZ'))
        vevent.add('summary').value = json['summary']
        vevent.add('dtstart').value = decompose_date(json['start'])
        vevent.add('dtend').value = decompose_date(json['end'])
        vevent.add('location').value = json['location']
        return vevent
    return v


def decompose_date(date_json):
    """Gère le cas particulier des json "date"."""
    if 'date' in date_json:
        d = datetime.strptime(date_json['date'], "%Y-%m-%d").date()
    elif 'dateTime' in date_json:
        d = date_json['dateTime']
        # On remplace la TZ : 01:00 en 0100 sinon on ne peut pas "strptime"
        if ":" == d[-3:-2]:
            d = d[:-3] + d[-2:]
        d = datetime.strptime(d, '%Y-%m-%dT%H:%M:%S%z')
        if 'timeZone' in date_json:
            tz = pytz.timezone(date_json['timeZone'])
        else:
            tz = pytz.utc
        d = d.astimezone(tz)
    return d
