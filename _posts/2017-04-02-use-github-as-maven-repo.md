---
title: 使用github做maven仓库
category: maven
tags: [github,maven,repository]
author: weiwei
---

本文以[mandarintools](https://github.com/weiweiwang/mandarintools)项目为例

# 创建github仓库

创建一个mvn-repo仓库(举例的名字，可以修改，不过建议使用这个)

然后通过git clone同步到本地，以我自己的mvn-repo为例
```
cd /Users/weiwei/workspace/github/
git clone https://github.com/weiweiwang/mvn-repo.git
```

# 在mandarintools项目中增加配置并发布到本地
```
    <distributionManagement>
        <repository>
            <id>weiweiwang-mvn-repo</id>
            <url>file:/Users/weiwei/workspace/github/mvn-repo/repository/</url>
        </repository>
    </distributionManagement>
```

运行如下命令发布

```
mvn deploy
```


# 进入到mvn-repo中commit&push
```
cd /Users/weiwei/workspace/github/mvn-repo
git add repository
git commit -m "release mandarintools v1.0.0"
git push origin master
```

# 在其他项目中使用
在
```
    <repositories>
    </repositories>
```

中增加一个repository

```
       <repository>
            <id>weiweiwang-maven-repo</id>
            <url>https://raw.githubusercontent.com/weiweiwang/mvn-repo/master/repository</url>
        </repository>
```

在dependencies中增加
```
        <dependency>
            <groupId>io.github.weiweiwang</groupId>
            <artifactId>mandarintools</artifactId>
            <version>1.0.1</version>
        </dependency>
```


