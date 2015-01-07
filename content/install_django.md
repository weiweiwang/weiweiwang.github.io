title: django环境安装
slug: django-environment-setup
category: sql_nosql
tags: mysql,character set,utf8
date: 2013-06-16

[TOC]

#django
		pip install django
		pip install flup(for fastcgi deploy)

#mysqldb

依赖参考：https://raw.github.com/farcepest/MySQLdb1/master/INSTALL

## ubuntu
		sudo apt-get install python-mysqldb
## centos
		yum install MySQL-python.x86_64
                或者
		yum install mysql-devel.x86_64
		pip install MySQL-python



#tutorial
https://docs.djangoproject.com/en/1.5/intro/tutorial01/

#captcha
		easy_install django-simple-captcha

#PIL(centos)
		yum install freetype-devel libjpeg-devel libpng-devel
		pip uninstall pil Pillow
		pip install pil Pillow
如果命令行提示：Some insecure and unverifiable files were ignored (use --allow-unverified pil to allow)则增加对应的选项即可
		pip install --allow-external pil --allow-unverified pil pil Pillow

#Ohters
		easy_install django
		easy_install mysql-python
		easy_install requests #这里需要依赖openssl
		easy_install django-simple-captcha
		easy_install six
		easy_install redis
		easy_install chardet
		easy_install mongoengine
		easy_install pyDes
		pip install mafan==0.2.3

# centos python升级到2.7

http://www.qwolf.com/?p=1166

http://toomuchdata.com/2012/06/25/how-to-install-python-2-7-3-on-centos-6-2/
