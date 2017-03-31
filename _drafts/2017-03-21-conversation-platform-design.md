---
title: 智能交互平台设计思考
category: chatbot
tags: [chatbot,api,ai]
author: weiwei
---

* TOC
{:toc}

# IBM Watson和api.ai中可以借鉴的点
## api.ai
* Test Console中要提供调试信息
* Response Variants
* 参数自动补全机制
* 系统实体，用户实体(存疑?)
* 上下文参数传递机制
* 实体annotation
* 领域知识
* automated expansion
* public/private agent
* 机器学习模块settings
## IBM Watson
* Dialog Tree
* Jump to
* 系统实体
* Conditional Response
* Conditional Jump to
* Response Variants


# 哪些是这个平台的核心技术问题

## 算法层面

### 意图匹配
word vector & paragraph vector(not good)


### 实体识别


### 自学习和改进

## 工程层面
### Dialog管理

### Session的管理

### 每个workspace/agent的模型的管理、更新、查询
namespace word vecotr->redis

### 同一个workspace训练管理
a fixed size mq queue and a same fixed size single thread consumer which consumes only one queue?

### 集群管理和自动扩容
mq server scale and redis scale

### 多语言架构

## 产品层面
### API设计
[IBM Watson Conversation API](https://www.ibm.com/watson/developercloud/conversation/api/v1/#introduction)
### 傻瓜式体验
### 领域知识积累
api.ai支持的领域可以参看[这里](https://docs.api.ai/docs/domains)，基于这个结合自身的业务情况可以规划一个domain knowledge todo


# 参考
1. [x.ai](https://x.ai/a-peek-at-x-ais-data-science-architecture/)
2. [IBM Watson Conversation API](https://www.ibm.com/watson/developercloud/conversation/api/v1/#introduction)