#!/usr/bin/python3
#-*- encoding: utf-8 -*-
import re
import os
from time import mktime
from datetime import datetime

# todo pip
import rfeed


class Syndication(rfeed.Feed):
    def __init__(self, feed):
        """Initialisation à partir d'un objet feedparser.

        :param feed: objet feedparser
        """
        items = self.convertir_items(feed.entries)
        self.initialize(items=items, **feed.feed)

    def initialize(self, title='', link='', description='', language=None,
                   copyright=None, managingEditor=None, webMaster=None,
                   pubDate=None, lastBuildDate=None, categories=None,
                   generator=None, docs=None, cloud=None, ttl=None, image=None,
                   rating=None, textInput=None, skipHours=None, skipDays=None,
                   items=None, extensions=None, **kwargs):
        if image:
            image = self.convertir_image(**image)
        super(Syndication, self).__init__(
            title, link, description, language, copyright, managingEditor,
            webMaster, pubDate, lastBuildDate, categories, generator, docs,
            cloud, ttl, image, rating, textInput, skipHours, skipDays, items,
            extensions)
        for arg, value in kwargs.items():
            setattr(self, arg, value)
#        self.items = []

    def __setattr__(self, arg, value):
        try:
            if arg == 'updated_parsed':
                arg = 'lastBuildDate'
                value = datetime.fromtimestamp(mktime(value))
            rfeed.Feed.__setattr__(self, arg, value)
        except Exception as e:
            print(e)
            pass

    def convertir_items(self, items):
        res = []
        for it in items:
            e = self.convertir_item(it)
            res.append(e)
        return res

    def convertir_item(self, item):
        return SyndicationItem(enclosures=item.enclosures, **item)

    def convertir_image(self, url=None, title=None, link=None, width=None,
                        height=None, description=None, **kwargs):
        # print('debug {}'.format(kwargs))
        url = kwargs['href'] if not url else url
        return rfeed.Image(url, title, link, width=width, height=height,
                           description=description)


class SyndicationItem(rfeed.Item):
    """Classe rfeed.Item qui permet l'import direct depuis feedparser.
    """

    def __init__(self, title=None, link=None, description=None, author=None,
                 creator=None, categories=None, comments=None, enclosure=None,
                 guid=None, pubDate=None, source=None, extensions=None,
                 **kwargs):
        super(SyndicationItem, self).__init__(
            title=title, link=link, description=description, author=author,
            creator=creator, categories=categories, comments=comments,
            enclosure=enclosure, guid=guid, pubDate=pubDate, source=source,
            extensions=extensions)
        for arg, value in kwargs.items():
            setattr(self, arg, value)

    def __setattr__(self, arg, valeur):
        try:
            if arg == 'enclosures':
                arg = 'enclosure'
                valeur = rfeed.Enclosure(
                    url=valeur[0]['href'], length=valeur[0]['length'], type=valeur[0]['type'])
            if arg == 'id':
                arg = 'guid'
                valeur = rfeed.Guid(valeur)
            if arg == 'summary':
                arg = 'description'
            if arg == 'published_parsed':
                arg = 'pubDate'
                valeur = datetime.fromtimestamp(mktime(valeur))
            rfeed.Item.__setattr__(self, arg, valeur)
        except Exception as e:
            print('ERROR {}'.format(e))
            pass
