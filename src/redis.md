title: get familar with redis:a great data structure server
slug: get-familar-with-redis
category: sql/nosql
tags: redis,nosql,memcache


#intro
redis是一个基于内存的数据结构database，相对于memcache，它提供了更为丰富的数据结构:string,hash,list,set,sorted set，同时它还提供了持久化能力，master-slave数据备份。同时在速度上与memcache也不相上下:[redis-memcached-benchmark](http://antirez.com/post/redis-memcached-benchmark.html),有同学质疑这个给出了个相反的[benchmark](http://dormando.livejournal.com/525147.html)，当然redis作者antirez又给出了一个[新的评测](http://antirez.com/post/update-on-memcached-redis-benchmark.html),不想仔细看英文的同学我大概总结一下，redis和memcached在同样的硬件配置下并且都是单线程的情况下吞吐也是相当的，100k每秒是问题不大的，大家可以follow这几篇文章自测一下。我很懒，没有对这个做过测试。

使用redis你可以做很多事情:

1. 做一个k-v系统用，不过这个k-v系统没有mongodb强大，不支持value查询，只能简单的get/set。
2. 做一个任务优先队列使用，list结构支持这样的各种api
3. 做一个消息队列使用，redis提供pub/sub这样的api来提供消息队列服务。
4. 数据统计，实时计数服务。微博上的各种数字都可以用这个服务来实时计数。
5. 做类似与memcached的内存cache，还可以持久化，性能也超级赞～

# install
* 下载最新的redis版本[redis download page](http://redis.io/download "redis-download")
* 加上你下载到/tmp目录下了，解压编译安装

		tar xvf redis-2.4.14.tar.gz
		cd redis-2.4.14
		make
		sudo make PREFIX=/opt/redis install
		sudo mkdir /opt/redis/etc
		sudo cp redis.conf /opt/redis/etc
		sudo mkdir -p /opt/redis/var/{db,run,log}
		sudo vim /opt/redis/etc/redis.conf 根据目录结构做相应修改，主要修改的就是包含/var路径的几行
* 启动服务

		sudo bin/redis-server etc/redis.conf

# test
	cd /opt/redis/
	bin/redis-cli
	redis 127.0.0.1:6379>set test 1
	redis 127.0.0.1:6379>get test

# lib
请参考官方网站的[redis client](http://redis.io/clients)

我用的是java版的client:jedis,这个client支持多机hash，连接池等，但是封装的不够好，使用的适合需要自己封装一层负责连接的申请和释放。


# ebook
[redis cookbook](http://vdisk.weibo.com/s/xhrM/1313680831)

# reference
1. [redis author's blog](http://antirez.com/)
2. [nosqlfan.com](http://blog.nosqlfan.com)
