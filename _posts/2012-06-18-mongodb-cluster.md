---
title: mongodb cluster configuration
category: sql_nosql
tags: [nosql,mongodb,cluster,replica-set,sharding]
---

# caution
在实际部署的时候请注意替换下面例子中的ip地址,下面所有操作假设实在mongodb安装根目录中，比如/opt/mongodb

# shard a: 27018
## 节点

* 192.168.0.77
* 192.168.0.78
* 192.168.0.58 仲裁节点

## 部署

	mkdir data/shard_a
	mkdir data/key
	echo "demo shard key" > data/key/shard_key
	chmod go-rw data/key/shard_key
	numactl --interleave=all bin/mongod --shardsvr --replSet shard_a --fork --port 27018 --dbpath /home/work/local/mongodb/data/shard_a/ --logpath /home/work/local/mongodb/logs/shard_a.log --logappend --keyFile /home/work/local/mongodb/data/key/shard_key	
	cfg = {
    _id : "shard_a",
    members : [
        {_id : 0, host : "192.168.0.77:27018"},
        {_id : 1, host : "192.168.0.78:27018"},
        {_id : 2, host : "192.168.0.58:27018",arbiterOnly:true}
    ]
	}


# shard b: 27018
## 节点

* 192.168.0.79
* 192.168.0.80
* 192.168.0.59 仲裁

## 部署

	mkdir data/shard_b
	mkdir data/key
	echo "demo shard key" > data/key/shard_key
	chmod go-rw data/key/shard_key
	numactl --interleave=all bin/mongod --shardsvr --replSet shard_b --fork --port 27018 --dbpath /home/work/local/mongodb/data/shard_b/ --logpath /home/work/local/mongodb/logs/shard_b.log --logappend --keyFile /home/work/local/mongodb/data/key/shard_key
	cfg = {
    _id : "shard_b",
    members : [
        {_id : 0, host : "192.168.0.79:27018"},
        {_id : 1, host : "192.168.0.80:27018"},
        {_id : 2, host : "192.168.0.59:27018",arbiterOnly:true}
    ]
	}

# config server 27019

## 节点

* 192.168.0.77
* 192.168.0.79
* 192.168.0.59

## 部署
	
	mkdir data/config
	numactl --interleave=all bin/mongod --configsvr -dbpath=/home/work/local/mongodb/data/config/ --fork --logpath /home/work/local/mongodb/logs/config.log --logappend --port 27019  --keyFile /home/work/local/mongodb/data/key/shard_key

# mongos 27017

## 节点

* 192.168.0.78
* 192.168.0.80

## 部署

	numactl --interleave=all bin/mongos --configdb 192.168.0.77:27019,192.168.0.79:27019,192.168.0.59:27019 --port 27017 --logpath /home/work/local/mongodb/logs/mongos.log --fork --logappend  --keyFile /home/work/local/mongodb/data/key/shard_key

# shard管理
	
	bin/mongo admin
	db.addUser('admin','admin');
	db.auth('admin','admin');
	db.runCommand( { addshard : "shard_a/192.168.0.77:27018,192.168.0.78:27018" } );
	db.runCommand( { addshard : "shard_b/192.168.0.79:27018,192.168.0.80:27018" } );

# shard db and collections
## 举例
	
	db.runCommand( { enablesharding : "demo" } );
	db.runCommand( { shardcollection : "demo.Table", key : {cloumn1: 1,column2:1} } )


# 参考
[mongodb sharding](http://www.mongodb.org/display/DOCS/Sharding)
