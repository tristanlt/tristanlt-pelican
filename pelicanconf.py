#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'tristanlt'
SITENAME = u'Tristanlt blog'
SITEURL = ''

SITESUBTITLE = 'Tristanlt blog'
SITEDESCRIPTION = ''
SITELOGO = '/img/m02-FvqA_200x200.jpg'
# FAVICON = '/images/favicon.ico'
BROWSER_COLOR = '#333333'
PYGMENTS_STYLE = 'monokai'

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'fr'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

#USE_FOLDER_AS_CATEGORY = True
#DEFAULT_CATEGORY = 'blog'
DELETE_OUTPUT_DIRECTORY = False

ARTICLE_URL = 'blog/{slug}.html'
ARTICLE_SAVE_AS = 'blog/{slug}.html'
#ARTICLE_URL = 'blog/{slug}/'

STATIC_PATHS = ['img']

#THEME = "./pelican-themes/pelican-blue"
THEME = "./pelican-themes/Flex"

#THEME = 'notmyidea'

MAIN_MENU = True

SOCIAL = (
            ('github', 'https://github.com/tristanlt'),
            ('twitter', 'https://twitter.com/tristanlt'),
)

MENUITEMS = (('Archives', '/archives.html'),
                     ('Categories', '/categories.html'),
                     ('Tags', '/tags.html'),)

# Blogroll
#LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)


DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
