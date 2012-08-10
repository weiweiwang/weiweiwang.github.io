title: In Project Maven Dependency:Maven本地依赖配置
slug: in-project-maven-dependency
category: programming
tags: maven,dependency,in-project


# In Project Repository

	<repository>
	    <id>lib</id>
	    <name>lib</name>
	    <releases>
	        <enabled>true</enabled>
	        <checksumPolicy>ignore</checksumPolicy>
	    </releases>
	    <snapshots>
	        <enabled>false</enabled>
	    </snapshots>
	    <url>file://${project.basedir}/lib</url>
	</repository>


# Lib structure
对于groupId=x.y.z的目录结构如下

	lib
	  |-- x
	      |-- y
	          |-- z
	              |-- ${artifactId}
	                  |-- ${version}
	                      |-- ${artifactId}-${version}.pom
	                      |-- ${artifactId}-${version}.pom.sha1
	                      |-- ${artifactId}-${version}.jar
	                      |-- ${artifactId}-${version}.jar.sha1 
由于上面的repository设置了ingore checksum,所以sha1的文件不是必须的
# 如何生成${artifactId}-${version}.pom

	mvn install:install-file -Dfile=xxx.jar -DgroupId=x.y.z -DartifactId=${artifactId} -Dversion=${version} -Dpackaging=jar

生成完之后拷贝到lib目录下的对应位置即可。

