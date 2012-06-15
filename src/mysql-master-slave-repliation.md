title: mysql master slave replication resync
slug: mysql-master-slave-replication-resync
category: sql_nosql
tags: mysql,replication

# master（可以是一个slave）
192.168.0.77

# slave
192.168.0.78

# 主从复制步骤和方法
## master
### 执行锁表操作

	flush tables with read lock;
### 查看当前状态

	show master status

### dump

	bin/mysqldump -uroot -p --default-character-set=utf8 {database} > {database}.dump

### 解锁
	
	unlock tables;

## slave
###  停止slave

	mysql -uroot -p -e "stop slave;"
### 导入

	mysql -uroot -p  {database} <  {database}.dump
### 重新设置master
举例

	change master to master_host='192.168.0.77',master_user='backup',master_password='backup',master_log_file='mysql-bin.000003',master_log_pos=1650;

### 启动slave

	mysql -uroot -p -e "start slave;"
