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
         ('Social / cultural blog (french)', 'http://gillux.blogspot.fr/'))

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/glenfant'),
          ('github', 'https://github.com/glenfant'),
          ('linkedin', 'https://fr.linkedin.com/in/gilles-lenfant-57a9a810'),
          ('stackoverflow', 'https://stackoverflow.com/users/826736/glenfant'),
          ('facebook', 'https://www.facebook.com/gilles.lenfant'))

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = 'notmyidea'

# https://github.com/streeter/pelican-gist
PLUGINS = ['pelican_gist']

# Tell pelican where it should copy that file to in your output folder
STATIC_PATHS = ['images', 'assets']

# Tell pelican where your custom.css file is in your content folder
EXTRA_PATH_METADATA = {
    'assets/custom.css': {'path': 'theme/css/custom.css'}
}

CSS_FILE = 'custom.css'

DISQUS_SITENAME = 'monbloggithub'
