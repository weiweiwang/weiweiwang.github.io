title: get familar with redis:a great data structure server
slug: get-familar-with-redis
category: sql_nosql
tags: redis,nosql,memcache


#intro
redis是一个基于内存的数据结构database，相对于memcache，它提供了更为丰富的数据结构:string,hash,list,set,sorted set，同时它还提供了持久化能力，master-slave数据备份。同时在速度上与memcache也不相上下:[redis-memcached-benchmark](http://antirez.com/post/redis-memcached-benchmark.html),有同学质疑这个给出了个相反的[benchmark](http://dormando.livejournal.com/525147.html)，当然redis作者antirez又给出了一个[新的评测](http://antirez.com/post/update-on-memcached-redis-benchmark.html),不想仔细看英文的同学我大概总结一下，redis和memcached在同样的硬件配置下并且都是单线程的情况下吞吐也是相当的，100k每秒是问题不大的，大家可以follow这几篇文章自测一下。

## 关于作者
![antirez avatar](images/antirez.png)

Salvatore Sanfilippo,also known [antirez](http://antirez.com/), programmer@VMWare，同时还是一家移动设备开发公司Kiurma的股东，意大利人。此兄的about页面上提到他主要都是在做open source code，并且几乎所有代码都放在[这里](http://github.com/antirez)，目前主要精力都在redis上，[这里](http://antirez.com/post/redis-manifesto.html)有antirez写的redis宣言。

## 使用redis你可以做哪些事情

1. 做一个k-v系统用，不过这个k-v系统没有mongodb强大，不支持value查询，只能简单的get/set。
2. 做一个任务优先队列使用，list结构支持这样的各种api
3. 做一个消息队列使用，redis提供pub/sub这样的api来提供消息队列服务。
4. 数据统计，实时计数服务。微博上的各种数字都可以用这个服务来实时计数。
5. 做类似与memcached的内存cache，还可以持久化，性能也超级赞～
6. more...

# install
* 下载最新的redis版本[redis download page](http://redis.io/download "redis-download")
* 加上你下载到/tmp目录下了，解压编译安装

		tar xvf redis-2.4.14.tar.gz
		cd redis-2.4.14
		make
		make test
		sudo make PREFIX=/opt/redis install
		sudo mkdir /opt/redis/etc
		sudo cp redis.conf /opt/redis/etc
		sudo mkdir -p /opt/redis/var/{db,run,log}
		sudo vim /opt/redis/etc/redis.conf 根据目录结构做相应修改，主要修改的就是包含/var路径的几行
如果跑测试提示tclsh不存在，请下载tcl8.5: sudo apt-get install tcl8.5
* 启动服务

		sudo bin/redis-server etc/redis.conf

# test
	cd /opt/redis/
	bin/redis-cli
	redis 127.0.0.1:6379> set test 1
	OK
	redis 127.0.0.1:6379> get test
	"1"


# benchmark
 
## 系统配置
* Linux pc 2.6.38-15-generic #60-Ubuntu SMP Tue May 22 11:30:47 UTC 2012 i686 i686 i386 GNU/Linux
* Intel(R) Core(TM) i7-2620M CPU @ 2.70GHz
* 4G memeory

## 使用的命令

	Usage: redis-benchmark [-h <host>] [-p <port>] [-c <clients>] [-n <requests]> [-k <boolean>]
	 -h <hostname>      Server hostname (default 127.0.0.1)
	 -p <port>          Server port (default 6379)
	 -s <socket>        Server socket (overrides host and port)
	 -c <clients>       Number of parallel connections (default 50)
	 -n <requests>      Total number of requests (default 10000)
	 -d <size>          Data size of SET/GET value in bytes (default 2)
	 -k <boolean>       1=keep alive 0=reconnect (default 1)
	 -r <keyspacelen>   Use random keys for SET/GET/INCR, random values for SADD
	  Using this option the benchmark will get/set keys
	  in the form mykey_rand:000000012456 instead of constant
	  keys, the <keyspacelen> argument determines the max
	  number of values for the random number. For instance
	  if set to 10 only rand:000000000000 - rand:000000000009
	  range will be allowed.
	 -P <numreq>        Pipeline <numreq> requests. Default 1 (no pipeline).
	 -q                 Quiet. Just show query/sec values
	 --csv              Output in CSV format
	 -l                 Loop. Run the tests forever
	 -t <tests>         Only run the comma separated list of tests. The test
                    names are the same as the ones produced as output.
	 -I                 Idle mode. Just open N idle connections and wait.

	Examples:

	 Run the benchmark with the default configuration against 127.0.0.1:6379:
	   $ redis-benchmark

	 Use 20 parallel clients, for a total of 100k requests, against 192.168.1.1:
	   $ redis-benchmark -h 192.168.1.1 -p 6379 -n 100000 -c 20

	 Fill 127.0.0.1:6379 with about 1 million keys only using the SET test:
	   $ redis-benchmark -t set -n 1000000 -r 100000000

	 Benchmark 127.0.0.1:6379 for a few commands producing CSV output:
	   $ redis-benchmark -t ping,set,get -n 100000 --csv

	 Fill a list with 10000 random elements:
	   $ redis-benchmark -r 10000 -n 10000 lpush mylist ele:rand:000000000000
## 测试结果

### value size 32

	wangweiwei@pc:/opt/redis$ bin/redis-benchmark -n 100000 -q -r 10000 -d 32
	PING_INLINE: 133333.33 requests per second
	PING_BULK: 135135.14 requests per second
	SET: 123001.23 requests per second
	GET: 105374.08 requests per second
	INCR: 115874.85 requests per second
	LPUSH: 121802.68 requests per second
	LPOP: 119474.31 requests per second
	SADD: 125313.28 requests per second
	SPOP: 129533.68 requests per second
	LPUSH (needed to benchmark LRANGE): 114942.53 requests per second
	LRANGE_100 (first 100 elements): 43936.73 requests per second
	LRANGE_300 (first 300 elements): 11580.78 requests per second
	LRANGE_500 (first 450 elements): 4827.42 requests per second
	LRANGE_600 (first 600 elements): 4644.03 requests per second
	MSET (10 keys): 48146.36 requests per second

### value size 128

	wangweiwei@pc:/opt/redis$ bin/redis-benchmark -n 100000 -q -r 10000 -d 128
	PING_INLINE: 125000.00 requests per second
	PING_BULK: 124843.95 requests per second
	SET: 116822.43 requests per second
	GET: 117785.63 requests per second
	INCR: 122249.39 requests per second
	LPUSH: 132978.72 requests per second
	LPOP: 128534.70 requests per second
	SADD: 117647.06 requests per second
	SPOP: 125000.00 requests per second
	LPUSH (needed to benchmark LRANGE): 123915.73 requests per second
	LRANGE_100 (first 100 elements): 24770.87 requests per second
	LRANGE_300 (first 300 elements): 7216.05 requests per second
	LRANGE_500 (first 450 elements): 4908.70 requests per second
	LRANGE_600 (first 600 elements): 3758.97 requests per second
	MSET (10 keys): 45207.96 requests per second


### value size 512

	Pngweiwei@pc:/opt/redis$ bin/redis-benchmark -n 100000 -q -r 10000 -d 512
	ING_INLINE: 134589.50 requests per second
	PING_BULK: 135685.20 requests per second
	SET: 110987.79 requests per second
	GET: 109051.26 requests per second
	INCR: 120336.95 requests per second
	LPUSH: 126582.28 requests per second
	LPOP: 125628.14 requests per second
	SADD: 100704.94 requests per second
	SPOP: 134228.19 requests per second
	LPUSH (needed to benchmark LRANGE): 131233.59 requests per second
	LRANGE_100 (first 100 elements): 10895.62 requests per second
	LRANGE_300 (first 300 elements): 3354.02 requests per second
	LRANGE_500 (first 450 elements): 2206.68 requests per second
	LRANGE_600 (first 600 elements): 1614.31 requests per second
	MSET (10 keys): 37750.09 requests per second

### value size 2048
	wangweiwei@pc:/opt/redis$ bin/redis-benchmark -n 100000 -q -r 10000 -d 2048
	PING_INLINE: 130548.30 requests per second
	PING_BULK: 133511.34 requests per second
	SET: 115340.25 requests per second
	GET: 112994.35 requests per second
	INCR: 122699.38 requests per second
	LPUSH: 118343.20 requests per second
	LPOP: 93720.71 requests per second
	SADD: 123456.79 requests per second
	SPOP: 116009.28 requests per second
	LPUSH (needed to benchmark LRANGE): 103519.67 requests per second
	LRANGE_100 (first 100 elements): 3332.22 requests per second
	LRANGE_300 (first 300 elements): 1011.06 requests per second
	LRANGE_500 (first 450 elements): 635.90 requests per second
	LRANGE_600 (first 600 elements): 432.38 requests per second
	MSET (10 keys): 24021.14 requests per second

### value size 2048 with pipeline 4 and 20 clients(default 50 clients)

	wangweiwei@pc:/opt/redis$ bin/redis-benchmark -n 100000 -q -r 10000 -d 2048 -c 20 -P 4
	PING_INLINE: 343642.62 requests per second
	PING_BULK: 395256.91 requests per second
	SET: 156006.23 requests per second
	GET: 152671.75 requests per second
	INCR: 216919.73 requests per second
	LPUSH: 163132.14 requests per second
	LPOP: 183150.19 requests per second
	SADD: 238663.48 requests per second
	SPOP: 302114.81 requests per second
	LPUSH (needed to benchmark LRANGE): 168634.06 requests per second
	LRANGE_100 (first 100 elements): 3061.66 requests per second
	LRANGE_300 (first 300 elements): 947.69 requests per second
	LRANGE_500 (first 450 elements): 613.75 requests per second
	LRANGE_600 (first 600 elements): 436.58 requests per second
	redis-benchmark: redis-benchmark.c:278: createClient: Assertion `c->randlen < (signed)(sizeof(c->randptr)/sizeof(char*))' failed.
	Aborted

# use case

## cache系统
	wangweiwei@pc:/opt/redis$ bin/redis-cli 
	redis 127.0.0.1:6379> set test 1
	OK
	redis 127.0.0.1:6379> get test
	"1"
	redis 127.0.0.1:6379> EXPIRE test 1
	(integer) 1
	redis 127.0.0.1:6379> get test
	(nil)
## 任务队列
* terminal 1
	
		redis 127.0.0.1:6379> blpop test 0
		1) "test"
		2) "1"
		(7.54s)

* terminal 2

		redis 127.0.0.1:6379> lpush test 1
		(integer) 1

## 消息队列
* terminal 1

		redis 127.0.0.1:6379> SUBSCRIBE test_channel
		Reading messages... (press Ctrl-C to quit)
		1) "subscribe"
		2) "test_channel"
		3) (integer) 1
		1) "message"
		2) "test_channel"
		3) "hello"
		1) "message"
		2) "test_channel"
		3) "let's hang out today?"

* terminal 2

		redis 127.0.0.1:6379> PUBLISH test_channel 'hello'
		(integer) 1
		redis 127.0.0.1:6379> PUBLISH test_channel 'let's hang out today?'
		Invalid argument(s)
		redis 127.0.0.1:6379> PUBLISH test_channel 'let\'s hang out today?'
		(integer) 1


## 实时计数
	redis 127.0.0.1:6379> set test 1
	OK
	redis 127.0.0.1:6379> INCR test
	(integer) 2
	redis 127.0.0.1:6379> get test
	"2"

## map使用
	redis 127.0.0.1:6379> hset test f1 '1'
	(integer) 1
	redis 127.0.0.1:6379> HGETALL test
	1) "f1"
	2) "1"
	redis 127.0.0.1:6379> HMSET test f2 '2' f3 '3'
	OK
	redis 127.0.0.1:6379> HGETALL test
	1) "f1"
	2) "1"
	3) "f2"
	4) "2"
	5) "f3"
	6) "3"
	redis 127.0.0.1:6379> HMGET test f1,f2
	1) (nil)
	redis 127.0.0.1:6379> HMGET test f1 f2
	1) "1"
	2) "2"
	redis 127.0.0.1:6379> HMGET test f1 f2 f4
	1) "1"
	2) "2"
	3) (nil)


## set使用
	redis 127.0.0.1:6379> SADD test 1 2
	(integer) 2
	redis 127.0.0.1:6379> SMEMBERS test
	1) "1"
	2) "2"
	redis 127.0.0.1:6379> sadd test1 2 3
	(integer) 2
	redis 127.0.0.1:6379> SMEMBERS test1
	1) "2"
	2) "3"
	redis 127.0.0.1:6379> SDIFF test test1
	1) "1"
	redis 127.0.0.1:6379> SINTER test test1
	1) "2"
	redis 127.0.0.1:6379> SUNION test test1
	1) "1"
	2) "2"
	3) "3"
	redis 127.0.0.1:6379> SISMEMBER test 1
	(integer) 1
	redis 127.0.0.1:6379> SREM test 1
	(integer) 1
	redis 127.0.0.1:6379> SMEMBERS test
	1) "2"

## sorted set使用
	redis 127.0.0.1:6379> ZADD test 3 1 2 2 1 3
	(integer) 3
	redis 127.0.0.1:6379> ZRANGE test 0 -1
	1) "3"
	2) "2"
	3) "1"
	redis 127.0.0.1:6379> ZREVRANGE test 0 -1
	1) "1"
	2) "2"
	3) "3"
	redis 127.0.0.1:6379> ZADD test1 1 1 2 2
	(integer) 2
	redis 127.0.0.1:6379> ZINTERSTORE out 2 test test1 
	(integer) 2
	redis 127.0.0.1:6379> ZRANGE out 0 -1 WITHSCORES
	1) "1"
	2) "4"
	3) "2"
	4) "4"
## Transaction

	redis 127.0.0.1:6379> multi
	OK
	redis 127.0.0.1:6379> incr foo
	QUEUED
	redis 127.0.0.1:6379> incr bar
	QUEUED
	redis 127.0.0.1:6379> incr bar
	QUEUED
	redis 127.0.0.1:6379> exec
	1) (integer) 1
	2) (integer) 1
	3) (integer) 2
	redis 127.0.0.1:6379> 
EXEC调用的过程中多个命令作为一个原子命令执行，在执行中间redis不会同时执行其他客户端的命令。在调用EXEC之前调用DISCARD会清除命令队列并退出事务。

事务中的命令即使执行失败也不会rollback，要么全执行，要么全不执行，命令的结果不影响事务。

事务中的命令在事务执行前都是没有结果返回的，所以无法在事务中进行check-and-set这样的操作。

如果exec执行的过程中server down机（crash or kill)，同时配置启用了aof，那么aof中记录的可能不是完整的日志，这时候如果重启会出现错误无法启动，需要先用redis-check-aof修复问题后重启。

	redis 127.0.0.1:6379> multi
	OK
	redis 127.0.0.1:6379> lpop bar
	QUEUED
	redis 127.0.0.1:6379> incr bar
	QUEUED
	redis 127.0.0.1:6379> exec
	1) (error) ERR Operation against a key holding the wrong kind of value
	2) (integer) 3
还有就是语法错误的命令不会被放入执行队列:

	redis 127.0.0.1:6379> multi
	OK
	redis 127.0.0.1:6379> incr a b c
	(error) ERR wrong number of arguments for 'incr' command
	redis 127.0.0.1:6379> incr bar
	QUEUED
	redis 127.0.0.1:6379> exec
	1) (integer) 4
Watch CAS(check-and-set)
terminal 1:

	redis 127.0.0.1:6379> watch a
	OK
	redis 127.0.0.1:6379> multi
	OK
	redis 127.0.0.1:6379> incr a
	QUEUED
	redis 127.0.0.1:6379> exec
	(nil)

terminal 2:
	
	redis 127.0.0.1:6379> set a 5
	OK
如果watch的key是有失效期的，并且在watch之后被redis失效删除了，那么EXEC会正常执行。

## Pipeline
批量发送一堆命令，然后一次性获取命令的执行结果。

	Pipeline pipeline = jedis.pipelined();
	long start = System.currentTimeMillis();
	for (int i = 0; i < 100000; i++) {
	    pipeline.set("" + i, "" + i);
	}
	List<Object> results = pipeline.execute();
	long end = System.currentTimeMillis();
	System.out.println("Pipelined SET: " + ((end - start)/1000.0) + " seconds");



## 新浪和instagram的redis实践
* [新浪](http://blog.nosqlfan.com/html/3295.html)
* [instagram](http://blog.nosqlfan.com/html/3379.html)

# lib
请参考官方网站的[redis client](http://redis.io/clients)

我用的是java版的client:jedis,这个client支持多机hash，连接池等，但是封装的不够好，使用的适合需要自己封装一层负责连接的申请和释放。


# ebook
[redis cookbook](upload/redis.pdf)

# reference
1. [redis author's blog](http://antirez.com/)
2. [nosqlfan.com](http://blog.nosqlfan.com)
