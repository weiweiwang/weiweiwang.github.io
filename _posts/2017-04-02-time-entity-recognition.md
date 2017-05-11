---
title: 时间实体识别
category: nlp
tags: [time,nlp,entity,recognition,时间,实体,识别]
author: weiwei
---

# maven依赖
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
            <version>1.0.5</version>
        </dependency>
```

# 代码库
[mandarintools](https://github.com/weiweiwang/mandarintools)，使用过程中遇到问题欢迎提issue

# 功能说明
越来越多的聊天机器人出现，其中时间实体等系统实体的识别是痛点之一，本开源代码基于[复旦nlp](https://github.com/FudanNLP/fnlp)开源库实现，增加offset，优化了代码清晰度和结构

对外暴漏的是`parse`函数，test case代码如下，调用是thread-safe的

```
@Test
public void testTimeEntityRecognition() {
    TimeEntityRecognizer timeEntityRecognizer = new TimeEntityRecognizer();
    String[] texts = {"上上周日", "六月十五日", "1972年", "80年", "今天", "去年", "1997年", "今晚", "今年", "最近两三年", "Hi，all.下午三点开会",
            "周一开会", "早上六点起床", "下下周一开会"};
    for (String txt : texts) {
        List<TimeEntity> timeEntityList = timeEntityRecognizer.parse(txt);
        LOGGER.debug("text:{}, time entities:{}", txt, timeEntityList);
    }
}
```

返回的time entity具有如下三个属性：

```
    private String original;
    private Date value;
    private int offset;
```