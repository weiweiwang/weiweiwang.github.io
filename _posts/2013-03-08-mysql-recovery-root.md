---
title: 重置mysql的root密码
category: sql_nosql
tags: [mysql,root,recovery,password]
date: 2013-03-08
---

#查看当前的启动命令
		ps auxf|grep mysql
		/bin/sh /usr/local/mysql/bin/mysqld_safe --datadir=/data/mysql --pid-file=/usr/local/mysql/tmp/mysql.pid

# 关闭Mysql

		killall -TERM mysqld

# 启动不需要认证的mysql

		nohup /bin/sh /usr/local/mysql/bin/mysqld_safe  --skip-grant-tables --datadir=/data/mysql --pid-file=/usr/local/mysql/tmp/mysql.pid &


# 重设密码

		mysql -uroot
		update mysql.user set password=PASSWORD('xxx') where user='root';
		flush privileges;


#重启mysql
注意这次不需要--skip-grant-tables

		bin/mysqladmin -uroot -p shutdown
		nohup /bin/sh /usr/local/mysql/bin/mysqld_safe --datadir=/data/mysql --pid-file=/usr/local/mysql/tmp/mysql.pid &
