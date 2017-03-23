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

如果下面看完缺少一个感性直观的认识可以看这个[官方的例子](https://docs.api.ai/docs/profile-bot-example-agent)

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

不过官方文档也提醒大家慎用这个功能
>Use this feature with caution:
>
>For finite lists, stick to creating entities containing complete lists instead of providing a partial list and checking 'Allow automated expansion'.
>
>If 'Allow automated expansion' is checked in more than one entity in the same agent, it may cause conflicts and unexpected classification results.

## 意图(Intents)
api.ai中意图是一个设计的比较重的模块，api.ai中没有IBM Watson中的Dialog模块，所以dialog中的功能全都在intents中实现了。Intents由如下四个部分组成

* User says: 用户样例，用于意图匹配的文本，文档中推荐使用原始样例，而不是模板，我的判断有可能模板功能是历史遗留问题，在api.ai初期模板用的较多，后来ML方法成熟后替代了模板，但模板依然是早期用户的使用习惯
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

这里有一点需要明确的是，如果新建一个intent，输入第一个user says example的时候，自动识别的实体如果你在review window修改会导致parameter table中同步变化，修改完再新增一句user says example的时候再修改review window中的参数时parameter table就不再变化了，可以参看下面的图片样例
![](https://files.readme.io/eNir2gTVQXyTFDejovfD_param-number-to-age.gif)

关于修改有三种类型:

* 修改实体类别
* 修改参数名称
* 删除annotation

### Response
有两种回复格式，一个是文本，一个是富文本。response可以配置多个变种，这样系统会round-trip使用这些response来增加趣味性和拟人效果。response中可以引用上下文变量，方法如下：

>* $parameter_name.original – to refer to the original value of the parameter
>* $parameter_name_for_composite_entity.inner_alias – to refer to a value of one of the composite entity components
>* \#context_name.parameter_name – to reference a parameter value collected in some other intent with defined context，这里后面会介绍到**context**概念，疑问留到后面解答

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

### Events
Event是用来通过触发一个意图，不需要经过用户输入的过程
>**Events** is a feature that allows you to invoke intents by an event name instead of a user query.
>
>First, you define event names in intents. Then, you can trigger these intents by sending a /query request containing an "event" parameter.
![](https://files.readme.io/28248bd-Events_enter-event-name.png)

可以通过event name来触发一个intent，并且可以携带参数
![](https://files.readme.io/6b761e9-Events_Custom_welcome_intent_UI.png)

{% highlight bash %}
curl -X POST -H "Content-Type: application/json; charset=utf-8" -H "Authorization: Bearer YOUR_CLIENT_ACCESS_TOKEN" --data "{'event':{ 'name': 'custom_event', 'data': {'name': 'Sam'}}, 'timezone':'America/New_York', 'lang':'en', 'sessionId':'1321321'}" "https://api.api.ai/api/query?v=20150910"

{
  "id": "a3a27316-572a-443f-bdb9-ca65dd2325d6",
  "timestamp": "2016-12-01T19:46:07.379Z",
  "result": {
    "source": "agent",
    "resolvedQuery": "custom_event",
    "action": "welcome",
    "actionIncomplete": false,
    "parameters": {
      "user_name": "Sam"
    },
    "contexts": [
      {
        "name": "custom_event",
        "parameters": {
          "user_name": "Sam",
          "name": "Sam",
          "user_name.original": ""
        },
        "lifespan": 0
      }
    ],
    "metadata": {
      "intentId": "ade506c7-851b-4f62-ba85-2f33023d079a",
      "webhookUsed": "false",
      "webhookForSlotFillingUsed": "false",
      "intentName": "Custom welcome intent"
    },
    "fulfillment": {
      "speech": "Welcome, Sam!",
      "messages": [
        {
          "type": 0,
          "speech": "Welcome, Sam!"
        }
      ]
    },
    "score": 1.0
  },
  "status": {
    "code": 200,
    "errorType": "success"
  },
  "sessionId": "1321321"
}
{% endhighlight %}

在使用api.ai的webhook的时候可以通过`followupEvent`来触发一个intent
>You can invoke events via webhook by sending event name with the "followupEvent" parameter in the response from your web service.
>When the "followupEvent" parameter is sent from the web service, the system ignores "speech", "displayText", and "data" fields.



{% highlight json %}
{
   "followupEvent": {
      "name": "<event_name>",
      "data": {
         "<parameter_name>": "<parameter_value>"
      }
   }
}
{% endhighlight %}

### Dialog
api.ai中没有单独的dialog组件，是和intents融合到一起的，概念上api.ai把dialog分了两类:
>* **Linear dialogs**, the aim of which is to collect the information necessary to complete the required action (e.g. find the best hotel, turn on the right light bulb, or play the desired song).
>* **Non-linear dialogs**, which may have several branches, depending on users’ answers.


#### Linear Dialog
在这个概念下一个方便的工具是slot filling，就是api.ai会自动帮你建立一个交互流程把参数补充完整
![](https://files.readme.io/A61Z45WgQYWN5itgjgam_image00.gif)

并且这个参数填充的顺序也是可以控制的
![](https://files.readme.io/MKqC0utTeKrjrzKRJyNQ_image03.gif)

这里注意用户是随时可以取消当前的流程的，但这里没有具体说明什么样的用户指令会导致取消，我试了下cancel和stop都可以取消当前流程
>Your agent will continue to ask these questions until it has collected information for all required parameters. At any time, users can ask to cancel and start from the beginning.

#### Non-linear dialogs
官方文档中提供了一个问卷调查的例子，问题是如下两个：

* How would you rate the location of the property?
* How would you rate the facilities at the hotel?

每个问题有如下答案:

* poor
* fair
* good
* excellent

实现方法是将question和每个answer都model成一个intent，通过context来控制dialog flow，这个流程对于一个有几十个问题的调查问卷来说复杂度还是足够高的，尤其当问题前后还有依赖时，context流转会变得很复杂，这一点相比较与watson来说就设计的不够灵活了，watson不仅仅可以根据intent、context来控制dialog flow，也可以根据变量来控制，会简化一些调查问卷这类问题的modelling，大家可以看一下下面几张截图理解下，还有疑问可以看[原文档](https://docs.api.ai/docs/dialogs)

![](https://files.readme.io/tRkGgnXARYeFd5kQlh9I_Screenshot_2.png)

![](https://files.readme.io/cHxWQcBTRgiYCoyp6Grw_new-intent-with-context.gif)

![](https://files.readme.io/ZnDtOD6aTC2mQO7ctnSP_new-intent-speech.gif)

![](https://files.readme.io/rxWNnvYuRmHH4j9sSjmb_intents-list.png)

![](https://files.readme.io/XwA31VC2Qz6tKx8pTylH_Screenshot_4.png)

### Webhook
webhook用做在intent匹配上之后交由平台应用方的service来处理和响应，响应生成的response会作为对用户的反馈，而不是直接使用intent中配置的response，这在很多场景下都是需要的，比如订餐所有参数(slot)都获取了，要下单了，必须要调用使用方的服务来完成这个动作，还有比如当用户输入的某个entity无法满足的时候，可以调用应用方服务来推荐候选等。

这里面的流程需要澄清下，对api.ai的调用可以由应用方service中转，也可以直接由终端(比如手机，智能家居)请求api.ai，api.ai在识别意图后调用应用方webhook service，应用方webhook service基于这个请求做response，然后api.ai再基于这个response来回复调用方，文章开头的图很清晰的说明了这个流程，在这个图中对api.ai的调用是直接从终端发起的

![](https://files.readme.io/a769bab-API-AI_key-concepts.png)

如果webhook调用失败，会fallback到intent中配置的Speech Response文本。

# 理解和疑问

## 意图匹配
文档中提到了两种ML的方法，一个是hybrid，一个是ml only， hybrid我理解是融合了ml之外的方法，比如基于检索和规则的匹配方法，这类方法在用户样例比较少的情况下能保持足够不错的精度
>**Hybrid (Rule-based and ML)** match mode fits best for agents with a small number of examples in intents and/or wide use of templates syntax and composite entities.

>**ML only** match mode can be used for agents with a large number of examples in intents, especially the ones using @sys.any or very large developer entities.

意图模型的学习数据源，这里也会给我们一个指导性意见，仅仅靠少量的用户样例要做到足够好的精度是比较困难的，所以在具体工程实现中都需要一个基础的语言模型来协助，否则很难保证合适的精度

>The agent “learns” both from the data you provide in it (**annotated examples** in intents and entries in entities) and from the **language models** developed by API.AI. Based on this data, it builds a model (algorithm) for making decisions on which intent should be triggered by a user input and what data needs to be extracted. The model is unique to your agent.

意图和实体规模上升后要手工触发训练，这个我理解是数据规模大的时候training的cost会上升，少量数据修改就重新训练会带来很多不必要的大量资源消耗，也会对系统稳定性产生影响，让用户主动触发的好处是用户知道什么时候自己的编辑修改结束了，这样能够有效的减少无效的训练任务。

>For agents with more than 50 entities or more than 600 intents, you need to update the model manually. To do so, go to your agent settings > ML Settings and click the 'Train' button.


### 实体在训练中的作用
api.ai文档中提到实体和意图都会用来训练，这一点我在前期的意图分类考虑中是没有考虑这个因素的，至于这个必要性现在不明确，我能想到的点是用户的entity和分词器分出来的可能有较大差别，用上之后应该对模型的准确性有帮助

### Training
api.ai提供了review功能来改进数据和学习效果

![](https://files.readme.io/dU6vbAGUQ6S81yggk8yQ_Trainig-overview.png)

对于没有匹配的输入我们可以调整其意图匹配关系

![](https://files.readme.io/pqsFjWBzTRWCR6FUXpbH_Training-options-for-unmatched.png)

也可以修改annotation问题
![](https://files.readme.io/vV5G5vTXQQmIIOH9VjbG_Training-incomplete-annotation-1.png)

![](https://files.readme.io/zvni9KDRmiSx4Jw3Io0z_Training-Incomplete-annotation-fixed-1.png)

文档中有一句话值得大家关注，这句话的意思是说不要把实体填充的用户回答作为intent的example，这是我们比较容易犯的一个错误
>There is no need to assign user inputs used for slot filling to any intents.


## 领域知识
api.ai中领域知识的解释如下：
>Domains are pre-defined knowledge packages.

>By enabling Domains, you can make your agent understand thousands of diverse requests and turn them into actionable data!
![](https://files.readme.io/wGQ3aTPS9CeNfUoAamcw_Individual-domains-1.png)

比如你打开small talk这个domain之后，在test console中就可以和他聊天了，比如我试了输入you are so sweet, 然后点开show json返回的json response如下:

{% highlight json %}
{
  "id": "008d133c-34e5-42e0-87c8-ced9f9464648",
  "timestamp": "2017-03-21T10:25:17.218Z",
  "result": {
    "source": "domains",
    "resolvedQuery": "you are so sweet",
    "action": "smalltalk.agent",
    "parameters": {
      "simplified": "you are good"
    },
    "metadata": {},
    "fulfillment": {
      "speech": "I like you too. You're a lot of fun to talk to."
    },
    "score": 1
  },
  "status": {
    "code": 200,
    "errorType": "success"
  },
  "sessionId": "9e5f05dc-f80f-4fd0-97a0-7e1ff23da256"
}
{% endhighlight %}

api.ai支持的领域可以参看[这里](https://docs.api.ai/docs/domains)

# 和IBM Watson Conversation比较
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

# api.ai公司情况
api.ai是一个功能非常完善的chatbot平台，作为2010年成立的一家公司，在语料和技术上的积累还是非常丰富的，在同类平台的调研中，api.ai是处于第一梯队水平的，目前调研的平台中，ibm watson的设计和灵活性更好一些，api.ai于2016年被google收购，现在是google的全资子公司。更多的信息请看[这里](https://www.owler.com/iaApp/1827798/api-ai-company-profile?onBoardingComplete=true)

# 欢迎交流
[联系方式点这里](/about)