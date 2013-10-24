title: ElasticSearch Configuration and Performance Tuning
slug: elasticsearch-configuration-and-performance-tuning 
category: search
tags: elasticsearch configuration,performance tuning
date: 2012-12-12

[TOC]

#下载与安装
## 下载
[http://www.elasticsearch.org/download/](http://www.elasticsearch.org/download/)

## 安装
	tar xvf elasticsearch-0.19.12.tar.gz
	

## 启动

	cd elasticsearch-0.19.12
	bin/elasticsearch -f

这里的-f参数是让程序在前台运行，这样可以看到程序运行的输出日志，正式环境不能这么运行，直接运行bin/elasticsearch就ok了。
#配置
上面启动的elasitcsearch没有做任何配置，正式使用的时候至少需要配置内存，一般情况下mapping配置也是不可缺少的。

## 系统配置
查看ulimit -n确保可以打开的文件句柄数目够大，如果使用memory lock的话还需要确保ulimit -l的大小足够使用。Java的版本至少1.6或者以上（1.7现在也支持的很好了）。ulimit -l和ulimit -n这两个配置的如下方法修改：

	vi /etc/security/limits.conf
	#max open files
	* hard nofile 65535
	* soft nofile 65535
	#max lock memory
	* soft  memlock 16000000
	* hard  memlock 16000000

        
## 内存配置
在bin/elasticsearch.in.sh最后增加如下一行：

	JAVA_OPTS="$JAVA_OPTS -Xmx4g -Xms4g -Xmn1g -XX:PermSize=128M -XX:MaxPermSize=128M"

elasticsearch中的默认配置是：

	-Xms2g -Xmx2g -Xss256k -Djava.awt.headless=true -XX:+UseParNewGC -XX:+UseConcMarkSweepGC -XX:CMSInitiatingOccupancyFraction=75 -XX:+UseCMSInitiatingOccupancyOnly -XX:+HeapDumpOnOutOfMemoryError -Xmx4g -Xms4g -Xmn1g -XX:PermSize=128M -XX:MaxPermSize=128M

实际使用的内存大小需要根据实际场景做调节，我目前2000w条数据，8g索引文件，4g内存完全够用。

##elasticsearch.yml配置
### 集群名称

	cluster.name: your_cluster_name

### shard和replica配置
参考[http://www.elasticsearch.org/guide/reference/api/admin-indices-create-index.html](http://www.elasticsearch.org/guide/reference/api/admin-indices-create-index.html)

	index.number_of_shards: 4
	index.number_of_replicas: 1
### refresh_interval
参考：[http://www.elasticsearch.org/blog/2011/03/23/update-settings.html](http://www.elasticsearch.org/blog/2011/03/23/update-settings.html)
refresh_interval这个值的默认值是1s，增加可以提高建立索引的速度，非实时搜索情况下建议设置的大一些，比如下面设置成120s

	index.refresh_interval: 120s

### cache设置
参考：[http://www.elasticsearch.org/guide/reference/index-modules/cache.html](http://www.elasticsearch.org/guide/reference/index-modules/cache.html)
节点的filter cache大小，默认是heap大小的20%，也可以制定绝对大小，比如下面指定为1g，注意如果设置为20%的时候需要加引号

	indices.cache.filter.size: 1g

### 开启memory lock

	bootstrap.mlockall: true

使用这个参数请确保memlock的系统配置已经设置，比如在我现在用的centos上需要如下设置：

	vi /etc/security/limits.conf
	* soft  memlock 10000000
	* hard  memlock 10000000

注意这里的单位是k，并且从我配置的经验看，这里的k是1000,而不是1024，所以如果你需要10g内存（也就是10737418240B），这里10000000会不够用的,需要至少设置为10737419才行



### 索引和分词的配置
参考:[http://www.elasticsearch.org/guide/reference/mapping/conf-mappings.html](http://www.elasticsearch.org/guide/reference/mapping/conf-mappings.html)
注意这里开启了mmapfs，如果你是linux/solaris 64bit的系统建议开启

	index:
	    store:
		type: mmapfs
	    analysis:
		analyzer:
		   edgeNGramAnalyzer:
		       type: custome
		       tokenizer: standard
		       filter: [standard,lowercase,englishSnowball,edgeNGramFilter]
		   nGramAnalyzer:
		       type: custome
		       tokenizer: standard
		       filter: [standard,lowercase,englishSnowball,nGramFilter]
		   standardAnalyzer:
		       type: custome
		       tokenizer: standard
		       filter: [standard,lowercase,englishSnowball]
		   mmsegAnalyzer:
		       type: custome
		       tokenizer: mmseg_maxword
		       filter: [standard,lowercase,englishSnowball]
		   complexAnalyzer:
		       type: custome
		       tokenizer: mmseg_complex
		       filter: [standard,lowercase,englishSnowball]
		   simpleAnalyzer:
		       type: custome
		       tokenizer: mmseg_simple
		       filter: [standard,lowercase,englishSnowball]
		tokenizer:
		   mmseg_maxword:
		       type: mmseg
		       seg_type: "max_word"
		   mmseg_complex:
		       type: mmseg
		       seg_type: "complex"
		   mmseg_simple:
		       type: mmseg
		       seg_type: "simple"
		filter:
		   nGramFilter:
		       type: nGram
		       min_gram: 1
		       max_gram: 64
		   edgeNGramFilter:
		       type: edgeNGram
		       min_gram: 1
		       max_gram: 64
		       side: front
		   englishSnowball:
		       type: snowball
		       language: English

这里需要注意的是我这里使用了mmseg分词工具，如果你不需要的话可以去掉相应的配置，mmseg分词插件的安装说明参看：[https://github.com/medcl/elasticsearch-analysis-mmseg](https://github.com/medcl/elasticsearch-analysis-mmseg)，如果你下载后的分词发现在并发情况下有bug（异常，分词结果错误），请用源码编译安装，源码里的这个bug已经修复。关于mmseg的说明可以参看<http://weiweiwang.github.com/mmseg.html>

### mappings的配置

	{
	    "test":{
		"_all":{
		    "enabled":false
		},
		"_source":{
		    "enabled":false
		},
		"properties":{
		    "id":{
		        "type":"string",
		        "index":"not_analyzed",
		        "store":"yes"
		    },
		    "name":{
		        "type":"string",
		        "index":"analyzed",
		        "index_analyzer":"mmsegAnalyzer",
		        "search_analyzer":"mmsegAnalyzer",
		        "store":"yes",
		        "term_vector":"with_positions_offsets"
		    },
		    "address":{
		        "type":"string",
		        "index":"analyzed",
		        "index_analyzer":"mmsegAnalyzer",
		        "search_analyzer":"mmsegAnalyzer",
		        "store":"yes",
		        "term_vector":"with_positions_offsets"
		    }
		}
	    }
	}

这个mapping的配置可以放置到config/mappings/{index}/{type}.json文件中，也可以通过命令设置

        curl -XPUT 'localhost:9200/test/test/_mapping' -d @test.json

## 测试
### 增加一条数据：

	curl -XPUT http://localhost:9200/test/test/1 -d '{"name":"test","address":"中关村","id":"1"}'

### 查询中关村(汉字需要编码）

    curl 'localhost:9200/test/test/_search?q=address:%E4%B8%AD%E5%85%B3%E6%9D%91&pretty=true'

### 查询中关(汉字需要编码)

	curl 'localhost:9200/test/test/_search?q=address:%E4%B8%AD%E5%85%B3&pretty=true'

### 使用query string查询

	curl 'localhost:9200/test/test/_search' -d '{
	    "from" : 0,
	    "size" : 20,
	    "timeout" : 5000,
	    "query" : {
		    "query_string" : {
		    "query" : "中关村",
		    "fields" : [ "address^1.0", "name^10.0"],
		    "default_operator" : "and",
		    "allow_leading_wildcard" : false
    		}
	    }
	}'

返回

	{
	  "took" : 1,
	  "timed_out" : false,
	  "_shards" : {
	    "total" : 4,
	    "successful" : 4,
	    "failed" : 0
	  },
	  "hits" : {
	    "total" : 1,
	    "max_score" : 0.19178301,
	    "hits" : [ {
	      "_index" : "test",
	      "_type" : "test",
	      "_id" : "1",
	      "_score" : 0.19178301
	    } ]
	  }
	}
	
# mmseg词典更新
从[https://code.google.com/p/sunpinyin/](https://code.google.com/p/sunpinyin/)下载sunpinyin_importer.tar.bz2，解压后里面有个import_sogou_celldict.py的python脚本，可以根据这个脚本来转换搜狗词库生成mmseg词库。
我拷贝修改了下可以批量转换:[点击下载](upload/convert_sogou_celldict_to_mmseg4j.py)

使用方法为:

     python convert_sogou_celldict_to_mmseg4j.py sogou_dict_dir mmseg_dict_dir

注意sogou词典scel文件请用英文名称命名，转换后会拼接成words-{原来的scel文件名称}.dic。转换完成后将这些文件拷贝到elasticsearch/config/mmseg目录下即可。词库文件[下载](http://pinyin.sogou.com/dict/)。


# 性能优化


## 准备工作
参考:[http://www.elasticsearch.org/guide/reference/modules/plugins.html](http://www.elasticsearch.org/guide/reference/modules/plugins.html)
安装elasticsearch-head和bigdesk来监控集群

	bin/plugin -install Aconex/elasticsearch-head
	bin/plugin -install lukas-vlcek/bigdesk

然后在浏览器里输入localhost:9200/_plugin/head/就可以访问监控页面。

## 影响性能的因素
### 内存要足够多，4G或以上
通过-Xmx -Xms -Xmn来调整heap内存的分配情况，同时建议参考jstat的使用说明来监控gc，可以参考[http://weiweiwang.github.com/jvm-gc-tuning.html](http://weiweiwang.github.com/jvm-gc-tuning.html)

### 如果可能开启memory lock

	vi /etc/security/limits.conf
	#max lock memory
	* soft  memlock 16000000
	* hard  memlock 16000000

### 文件句柄数是否足够，建议设置为65536或以上

	vi /etc/security/limits.conf
	#max open files
	* hard nofile 65535
	* soft nofile 65535

### 如果是64位linux/solaris系统，开启mmapfs
上面的例子已经给出了如何开启，参考[http://blog.thetaphi.de/2012/07/use-lucenes-mmapdirectory-on-64bit.html](http://blog.thetaphi.de/2012/07/use-lucenes-mmapdirectory-on-64bit.html)

### optimze索引文件为一个文件

	curl -XPOST 'http://localhost:9200/test/_optimize?max_num_segments=1'

### 调整cache保证足够使用
先通过bigdesk监控系统性能，然后确定这个参数如何调整。

### refresh_interval调大一些，比如60s或者更大
如果不要求实时搜索，可以调大这个值，注意这个值调大之后，新加入的索引并不是立刻就能搜索到，要超过这个interval之后才能检索到。

### 放大招了
上SSD硬盘，可以参考[这里](http://euphonious-intuition.com/2013/02/five-things-i-learned-from-elasticsearch-training/)

# 参考
[http://www.tuicool.com/articles/NbM7zi](http://www.tuicool.com/articles/NbM7zi)

[http://www.elasticsearch.org/](http://www.elasticsearch.org/)

[http://blog.thetaphi.de/2012/07/use-lucenes-mmapdirectory-on-64bit.html](http://blog.thetaphi.de/2012/07/use-lucenes-mmapdirectory-on-64bit.html)

[http://euphonious-intuition.com/2013/02/five-things-i-learned-from-elasticsearch-training/](http://euphonious-intuition.com/2013/02/five-things-i-learned-from-elasticsearch-training/)
