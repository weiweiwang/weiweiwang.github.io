title:Blogging with pelican+markdown+github
slug:blogging-with-pelican+markdown+github
category:misc
tags:blog,pelican,markdown,github


这篇文章很多内容来自于xieyu的一篇博文[markdown+pelican+github=Perfect blog platform](http://xieyu.github.com/pelican-github-markdown.html), 本着引用注明出处的原则，我得先声明这一点:-)

# 安装一些必备的东东
* python 2.7或更高版本(是否可以更低版本我不确定，我的版本是2.7)

		sudo apt-get install  python2.7

* 安装easy_install

		sudo apt-get install python-setuptools

* 安装pelican和markdown

		sudo easy_install pelican
		sudo easy_install Markdown
		sudo easy_install ghp-import

# 创建blog
* 初始化

		mkdir -p ~/myblog
		cd ~/myblog
		pelican-quickstart

* 编译测试

		make html;firefox output/index.html

* 一些小修改
		
		vi pelican.conf.py
		修改TIMEZONE='Asia/Shanghai'
		修改LOCALE=('zh_CN.utf8','en_US.utf8')
		修改DEFAULT_DATE_FORMAT=('%Y/%B/%d %A')
		LINKS和SOCIAL根据需要修改

* 使用git管理
		
		git init;git add src pelican.conf.py Makefile;git commit -m "first commit"
		git checkout -b source master;git branch -d master

这里删除master分支，是因为github page需要占用master分支，所以选择把blog源文件放到source分支。

# 如何使用github
* 创建github账号并登录
* 登录github,创建仓库,仓库名必须为${username}.github.com,${username}替换为你的github账号
* 增加remote
		
		git remote add origin https://github.com/${username}/${username}.github.com.git

* 修改~/myblog/Makefile
		
		修改git push origin gh-pages为git push -f origin gh-pages:master

这里的意思是用ghp-import管理分支，但这个工具是针对project page的，所以需要将master分支每次都更新为gh-pages这个分支。github page分为两种，一种是user/organization page，另一种是project page。我们这里用的是user/organization page，详细说明看[这里](https://help.github.com/articles/user-organization-and-project-pages)

* 测试github
		
		cd ~/myblog;make github此处需要输入github的用户名密码
		用浏览器访问${username}.github.com试试看

# 写日志
	vi src/test.md
	输入如下内容
	title: get familar with redis:a great data structure server
	slug: get-familar-with-redis
	category: sql_nosql
	tags: redis,nosql,memcache
	然后运行make clean github再访问你的页面试试看

# 高级主题

## 如何配合使用GOOGLE ANALYTICS
默认的notmyidea主题支持google analytics,为你的这个页面申请好google analytics串号，然后在pelican.conf.py中增加如下内容即可
	
	GOOGLE_ANALYTICS='UA-7072537-7'

## 如何增加评论

去disqus注册一个， 然后在pelican.conf.py里面加入如下内容

	DISQUS_SITENAME = 'siteShortName'


这里的siteShortName替换成在注册页面所填写的siteShortName。
