---
title: 任务式交互平台设计思考
category: chatbot
tags: [chatbot,api,ai]
author: weiwei
---

* TOC
{:toc}


# 系统结构
下图是一个非常简略便于理解的系统结构，把语音能力看做一个基础通道能力的话，核心的部分就是NLP相关的能力和对话管理。

NLP相关的能力核心是实体识别和意图识别，实体识别部分如果不需要上下文会简单些，但很多场景是要有上下文的，这时候我们称其为slot filling，这个做起来会复杂很多，因为需要大量语料去训练一个slot filling的模型。

意图识别抽象起来就是一个文本分类，但难点是可用于分类的样本是非常少的，考虑到在任务式场景中用户的目的性比较强（并且用户习惯会随着类似产品越来越多而增强），所以对精度的要求可以放低一些，但召回的要求比较高。

DM部分目前还做不到自动化，自动化的都无法很好handle任务式的场景，所以目前api.ai和ibm watson conversation都是用的对话树的结构在处理对话流程，这是局限于当前的技术还无法自动化做好这块，同时很多业务可能还没有很多数据积累，但系统一旦跑起来，数据的价值在后续的迭代中就能得到体现，慢慢的可以半自动，长期来看是可以做到自动化建模的。上下文传递能力是DM中非常核心的因素，还有上下文也要支持外部传入，因为很多场景需要外部传递信息来作为上下文，比如用户的画像信息可能是已经掌握的，作为上下文可以直接带入DM模块，而不需要用户语音或者文本来输入这些信息。

![](/assets/images/task-spoken-dialog-system.jpeg)


# 哪些是这个平台的核心技术问题

## 算法层面

### 意图匹配
下面是几种意图匹配的方法，search技术可以和分类模型结合起来使用，能够较好的平衡召回和准确率

* word vector
* fast text
* search


### 实体识别
实体这里面分为两类，系统实体和开发者实体，在api.ai还有用户实体，比如用户的playlist，是每个用户不同的，无法作为开发者实体存在，本文不介绍用户实体，其实现逻辑和开发者实体差别不大，这里我们也能看出来api.ai作为一家做了7年(2010年成立)的公司，处理了海量的需求和case，沉淀下来的能力非常值得参考借鉴

#### 系统实体
有些实体是相对通用的，对话系统自身就需要支持，以下列了一些比较重要的，并且这个可以随时向系统添加，并且有的实体如歌名，量比较大，更新频率也比较高，如果能作为系统实体提供会对使用者带来很大的便利

* 时间
* 地点
* 人名
* 组织机构
* 数字
* 手机号
* 身份证
* 邮箱
* .etc.

[api.ai系统实体](https://docs.api.ai/docs/concept-entities#section-system-entities)

#### 开发者实体

和场景业务相关的实体交给系统的使用者通过api或管理平台录入，比如做按摩的，有若干种套餐，这种就不适合作为系统实体，需要交给开发者来实现。

#### Slot识别
下图的例子能够很好的解释仅仅实体识别为什么会遇到问题，由于语义的上下文依赖，仅仅识别出地点在图中的case中是判断不出来这是个目的地还是出发地的，要结合上下文来识别，相关的介绍很多，主要是基于RNN来实现(LSTM属于RNN)。截图是从李宏毅老师的课程中截图的，下载地址点[这里](http://speech.ee.ntu.edu.tw/~tlkagk/courses/ML_2016/Lecture/RNN%20(v2).pdf)

![](/assets/images/slot-filling.png)


## 工程层面
### Dialog管理
在api.ai中的dialog管理是通过上下文context属性来控制的，ibm watson中是基于树状结构和条件触发来管理的，综合比较下来ibm watson的解决方法清晰度更高，更灵活，并且也具有更好的准确性。关于准确性是因为watson的上下文交互的条件不仅仅可以是意图还可以是任意的条件组合，这会减少意图识别错误率的级联累积。

dialog树的管理在前端交互上是比较复杂的，这部分会占据系统开发的大量时间，dialog tree evaluation的逻辑可以参考ibm watson的文档，也会占据不少开发工作量。

### Session的管理
这个比较简单，主要问题就是如何控制session的timeout，或者交给上游来控制session的timeout，我倾向于后者，比如微信等IM场景，聊天不是连续的，有可能说了上一句，下一句很久才回复，如果要在这种场景做上下文理解，timeout就不好放在这个系统中来控制。

### 每个workspace/agent的模型的管理、更新、查询
由于每个agent的模型是独立的，并且是要及时训练的，所以关于模型训练任务的管理、更新、查询需要有分布式的解决方案，这块可以参考[dubbo](http://dubbo.io/)的方案或者使用dubbo类似框架来解决


## 产品层面
### API设计
这块参考api.ai和watson就可以了，不参考也完全可以自主设计

[IBM Watson Conversation API](https://www.ibm.com/watson/developercloud/conversation/api/v1/#introduction)

### 易用性设计
这块需要在不停的迭代中优化提升，随着使用场景的增加，上面提到的设计方案和产品体验会比较技术化，要让小白可以用还有距离，这块就需要在迭代中不断沉淀，比如dialog tree是否可以模板化创建，常用的场景比如查天气、打开app这种功能是否都可以预置

### 上层扩展
本文介绍的这个对话式系统自身再往上构建场景化的应用才会更加实用，所以基于这个系统做分层设计，上层可以构建客服、营销等多个场景，当前切入点前期要focus，做深做透

### 导入导出
易用的导入导出功能和格式可以减少人工录入的工作量，提升系统建模效率

### 海量实体支持
很多场景会遇到大量的实体需要处理，比如酒店、歌曲、菜品等实体的规模全国范围看是较大量的，无论使用管理平台还是api都要能非常友好的支持


# 参考
1. [x.ai](https://x.ai/a-peek-at-x-ais-data-science-architecture/)
2. [IBM Watson Conversation API](https://www.ibm.com/watson/developercloud/conversation/api/v1/#introduction)
3. [api.ai](https://api.ai)


# 附：IBM Watson和api.ai中可以借鉴的点
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