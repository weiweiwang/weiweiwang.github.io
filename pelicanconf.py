#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u"wangweiwei"
SITENAME = u"Careless Whisper"
SITEURL = 'http://weiweiwang.github.com'


TIMEZONE = 'Asia/Shanghai'

GITHUB_URL = 'http://github.com/weiweiwang/'

PDF_GENERATOR = False
MD_EXTENSIONS=['toc']
DEFAULT_PAGINATION = 5
FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'
DEFAULT_METADATA = (('wangweiwei', 'weiweiwang'),('internet','cloud computing'),('search','nosql'),)


DEFAULT_LANG='zh'
DEFAULT_DATE_FORMAT=('%Y/%B/%d %A')

LOCALE=('zh_CN.utf8','en_US.utf8')

STATIC_PATHS=['images',"upload"]
DISQUS_SITENAME='cloudornot'

# Blogroll
LINKS =  (
		('Xieyu','http://xieyu.github.com'),
		(u'刘未鹏','http://mindhacks.cn'),
         )

# Social widget
SOCIAL = (
          (u'新浪微博','http://weibo.com/lolorosa'),
         )

DEFAULT_PAGINATION = 20

THEME='sneakyidea'

GOOGLE_ANALYTICS='UA-7072537-7'

FILES_TO_COPY = (('googleb1b731a5802d3353.html', 'googleb1b731a5802d3353.html'),)



