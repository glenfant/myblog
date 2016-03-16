#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Gilles Lenfant'
SITENAME = u'Digital Snake and Family'
SITESUBTITLE = u'Gossips about (mostly) Python based technologies'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Previous blog', 'http://glenfant.wordpress.com'),
         ('Social / cultural blog (fr)', 'http://gillux.blogspot.fr/'))

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/glenfant'),
          ('github', 'https://github.com/glenfant'),
          ('linkedin', 'https://fr.linkedin.com/in/gilles-lenfant-57a9a810'),
          ('facebook', 'https://www.facebook.com/gilles.lenfant'))

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = 'notmyidea'