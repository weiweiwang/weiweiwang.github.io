---
title: Chatbots调研-api.ai
category: chatbot
tags: [chatbot,api,ai]
author: weiwei
---

* TOC
{:toc}

# api.ai是什么
api.ai是一个构建对话能力的平台，通过api方式提供给需要构建对话能力的应用，不限于硬件设备，app等。
>API.AI is a platform for building conversational interfaces for bots, applications, and devices.

下图是一个api.ai的业务流程图，绿色部分是api.ai提供的能力。
![](https://files.readme.io/a769bab-API-AI_key-concepts.png)

# 概念
## 实体(Entities)
这里的实体概念和IBM Watson中几乎完全一样，不一样的地方在于api.ai中有三类实体，相较于watson多了一类用户实体

* 系统实体：平台定义的保留实体空间
* 开发者实体：开发者定义的实体
* 用户实体：每个请求粒度定义的实体，这个实体的存在意义是特定用户需要的，比如歌曲列表(命名列表)这样的实体是某个用户都不一样的，放到请求中或者一个session中传递是有助于这样的实体识别而又不会污染实体空间的，这个只能通过api来实现，参见文档[https://docs.api.ai/docs/userentities](https://docs.api.ai/docs/userentities)

并且每个实体的类型可以是如下几种:

* mapping: 有同义词的(原文have reference values)
* enum type: 没有reference values
* compposite: 由其他实体组成，比如下面的配置样例
![](https://files.readme.io/vf7WhcKqTVSiR9IW2OEi_direction_entity.gif)
![](https://files.readme.io/bbAEXYSVTwi6VAU4ymVk_move_entity.gif)
![](https://files.readme.io/d4aaf0e-Entities-robot-moves.gif)
“Move five steps forward”的返回参数会是这样的

{% highlight json %}
{ "parameters": {
    "move": {
        "direction": "forward",
        "steps": 5
    }
  }
}
{% endhighlight %}

### 实体自动扩展
用下面官方文档的例子来解释下，在打开扩展开关(allow automated expansion)后，做如下配置
![](https://files.readme.io/150b39f-Allow-automated-expansion-check.png)
![](https://files.readme.io/e25e53d-Allow-automated-expansion-intent-example.png)
这时候当遇到用户输入"I need to buy some vegetables"时vegetables可以被系统识别为item实体，返回的json如下:

{% highlight json %}
{"result": {
    "source": "agent",
    "resolvedQuery": "I need to buy some vegetables",
    "action": "",
    "actionIncomplete": false,
    "parameters": {
      "item": "vegetables"
    },
    "contexts": [],
    "metadata": {
      "intentId": "2c5470c1-2749-45e8-992f-b5dff7645456",
      "webhookUsed": "false",
      "intentName": "buy-items"
    },
    "fulfillment": {
      "speech": "Ok, adding vegetables."
    }
}
{% endhighlight %}

## 意图(Intents)
api.ai中意图是一个设计的比较重的模块，api.ai中没有IBM Watson中的Dialog模块，所以dialog中的功能全都在intents中实现了。Intents由如下四个部分组成

* User says: 用户样例，用于意图匹配的文本，文档中推荐使用原始样例，而不是模板
>We recommend using examples rather than templates, because it’s easier and Machine Learning learns faster this way. And remember: the more examples you add, the smarter your agent becomes.
* Action: 动作，目前理解是一个action name供hook识别用，一个intent可以配置一个action，多个intent可以共用同一个action，api.ai中Music-Player例子中action全部是和intent name是一样的，从例子中看不出action的作用
* Response: 回复
* Contexts: 上下文

### User says
这里面可以基于模板，也可以基于自然语言的样例，官方也是推荐样例方式配置

api.ai中可以对用户输入样例做annotation和实体修改，比如：
![](https://files.readme.io/a051c07-Intents-review-win-and-param-table.png)
![](https://files.readme.io/368a601-Intents_local-changes.png)
这里面有两个地方可以修改实体，一个是review window，一个是parameter table，review window的修改只影响这一个样例，而parameter table中的修改影响当前意图下的所有样例。

>Changes in the review window won’t affect other examples containing the same annotations.
>
>Changes in the parameter table will affect all ‘User says’ examples with the same annotation.

关于修改有三种类型:

* 修改实体类别
* 修改参数名称
* 删除annotation

### Response
有两种回复格式，一个是文本，一个是富文本。response可以配置多个变种，这样系统会round-trip使用这些response来增加趣味性和拟人效果。response中可以引用上下文变量，方法如下：

>* $parameter_name.original – to refer to the original value of the parameter
>* $parameter_name_for_composite_entity.inner_alias – to refer to a value of one of the composite entity components
>* \#context_name.parameter_name – to reference a parameter value collected in some other intent with defined context，这里后面会介绍到context概念，疑问留到后面解答

如果需要使用$,\#符号在回复文本中，使用{}符号来转义，比如
>${100} – where 100 is a constant value
>
>${$number} – where $number is a reference to the parameter value
>
>\#{channel} – where channel is a string
>
>\#{#channel.name} – where #channel.name is the reference to the parameter value "name" from the context "channel"

对于输入{或者}，可以用两个代替，也就是{% raw %}{{和}}{% endraw %}

对于参数值是可选的情况来说，response中那些引用了某个参数而参数值为空时不会被作为候选回复，也就是这种情况的参数个数如果是n个，那么回复变种的个数就需要是![equation](http://latex.codecogs.com/svg.latex?2^n)个

关于富文本是和第三方平台接入的时候会用到，本文不多介绍，文档参看这里[https://docs.api.ai/docs/rich-messages](https://docs.api.ai/docs/rich-messages)

### Contexts
contexts在api.ai中有两个作用，一个是传递上下文参数，一个是控制dialog flow。

dialog flow上前后两个节点的输出和输入context需要match上才能匹配，比如下面第一个图中的output context和第二图中的input context是一样的，第二个图中的intent会是第一个图中的intent执行后下一步的候选，如果只有它一个候选，就会执行它，如果有多个还要看优先级。
![](https://files.readme.io/x2dSnVCjShyZfE7Sjler_output-context.png)
![](https://files.readme.io/TGWofPu9SxK7CM7OyBAL_input-context.png)

context还有个生命周期的概念，控制在后几步能被感知到，默认是5步或者10分钟，也可以通过界面修改
![](https://files.readme.io/1r7UBT1ASYi8kFp9rgxM_context-lifespan.png)

也可以重置context，比如命中一个intent之后，context中的属性不能再往下传递了，就可以重置它
![](https://files.readme.io/DZnk10TtTXSCDbKoX82B_context-lifespan-zero.png)

对于input contexts，原文档中有个例子，对于"I want to hear more of them"这样的输入，如果没有input context我们就需要询问要听的是谁的歌，如果有input context我们就知道them指代的是谁。

注意这里使用了参数填充功能

![](https://files.readme.io/3WkVJdDwS66w6jPveVBi_add-slot-filling.png)

这是test样例

![](https://files.readme.io/TWRwu9RhScPpDYuNCljA_slot-filling-dialog.gif)

这是具有input context的intent，注意parameter中artist的值是通过获取context中的参数填充的
![](https://files.readme.io/Tl3ifBOJSoiGuAt1Z2Qh_intent-input-context.png)

这是具有和上图对应的output context的intent
![](https://files.readme.io/wY26jzsHSuwNkdm69EmK_intent-output-context.png)

一个intent可以配置多个input和output contexts，如果一个intent配置了多个input context，所有这些input contexts都满足才能触发这个intent
>In case of multiple input contexts defined in a single intent, all these contexts should be active in order for this intent to be matched.


### Intents优先级
当有多个候选intents时候，通过intents的优先级来确定最终匹配的intent

![](https://files.readme.io/633a9a2-Intent-priority-new.gif)

# 理解和疑问

## 意图匹配

>**Hybrid (Rule-based and ML)** match mode fits best for agents with a small number of examples in intents and/or wide use of templates syntax and composite entities.

>**ML only** match mode can be used for agents with a large number of examples in intents, especially the ones using @sys.any or very large developer entities.

意图模型的学习数据源

>The agent “learns” both from the data you provide in it (**annotated examples** in intents and entries in entities) and from the **language models** developed by API.AI. Based on this data, it builds a model (algorithm) for making decisions on which intent should be triggered by a user input and what data needs to be extracted. The model is unique to your agent.

意图和实体规模上升后要手工触发训练

>For agents with more than 50 entities or more than 600 intents, you need to update the model manually. To do so, go to your agent settings > ML Settings and click the 'Train' button.


### 实体在训练中的作用
api.ai文档中提到实体和意图都会用来训练，这一点我在前期的意图分类考虑中是没有考虑这个因素的，至于这个必要性现在不明确，我能想到的点是用户的entity和分词器分出来的可能有较大差别，用上之后应该对模型的准确性有帮助


## 领域知识
TODO


# 比较
相比较IBM Watson值得借鉴的地方：

* 调试信息: 在evaluation过程中提供intent相关的匹配信息，辅助调试和优化配置
![](https://files.readme.io/0e91ce6-getting-started-testing-results.png)
* 参数自动补齐
![](/assets/images/api-ai-parameter-fillment.png)
* 用户实体，具体实现起来还比较复杂，需要用户的临时索引，能简化建议简化掉
* 上下文参数传递比watson中简单
* 实体annotation功能
* 领域知识组件
* [automated expansion](https://docs.api.ai/docs/concept-entities#allow-automated-expansion)
* Public/Private Agent，可以将agent开放给其他人使用，这个特性有助于形成社区文化
* Avatar and Description，个性化bot

# 设计参考
## 架构
TODO
## API
TODO

# 欢迎交流
[联系方式点这里](/about)