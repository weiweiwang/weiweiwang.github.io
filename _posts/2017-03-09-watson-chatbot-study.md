---
title: Chatbots调研-IBM Watson
category: chatbot
tags: [chatbot,ibm watson]
author: weiwei
---

* TOC
{:toc}

# 参考
[IBM Watson How to build a chatbot][ibm-watson-how-to-build-a-chatbot]

[如何构建Dialog Tree](https://www.ibm.com/watson/developercloud/doc/conversation/dialog-build.html)

[Dialog概念解释](https://www.ibm.com/watson/developercloud/doc/conversation/dialog-build.html#overview)

# Book-Car Workspace

这里提供了一个Demo供下载和测试用，目前(2017-03-09)中文支持还是Experimental状态，后面也会提到有坑，暂时不建议使用

[Book Car Demo Json File Download](/assets/data/watson-book-car-workspace.json)

右键下载之后可以用下面的方式导入

![Watson Workspace Import](/assets/images/watson-workspace-import.png)

没有账号可以到[这里](https://www.ibmwatsonconversation.com)注册试用账号，注册完导入上面下载的json就可以进行尝试了。

# Watson的几个概念

#### Intents
意图，通过用户的一些example sentence来训练学习识别，背后就是一个文本多分类模型，可以用LSTM这样的网络来学习，难点在于解决泛化，这块目前我想到的方法是将sentence中的某些term泛华之后再加入训练，比如时间、地点、同义词归一化(比如要去，想去）。

#### Entities
实体在维基百科的定义是

>An entity is something that exists as itself, as a subject or as an object, actually or potentially, concretely or abstractly, physically or not.

具体点比如时间、日期、地点、人名、数字、货币、百分比、电视剧名称、电影名称这些都是实体，是一个实际存在的或者抽象出来的概念。

给Watson喂很多entity，他就可以在用户输入中识别出来，同时我判断也会用来泛华Intents和匹配Intents。

#### Dialog
Watson中的Dialog是无状态的，官方文档里是这么描述的：
>The dialog is stateless, meaning that it does not retain information from one interchange to the next. Your application is responsible for maintaining any continuing information. However, the application can pass information to the dialog, and the dialog can update the context information and pass it back to the application.

这里要区分开Dialog和Node的概念，Dialog是由Node构成的，Dialog无状态是合理的，而不是Node是无状态的，Node上下传递需要Context信息，所以Node是要有状态的。

Watson中Dialog是以树状结构组织的，看一下workspace中book car demo就全懂了。

# 配置
#### Intents
![Intents Configuration](/assets/images/watson-intents.png)

#### Entities
![Entities Configuration](/assets/images/watson-entities.png)

#### Dialog
对Dialog tree具体的理解和解释下面一节会展开
![Book Car Dialog Tree](/assets/images/watson-book-car-dialog.png)



# 理解和疑问

#### Dailog Tree匹配的逻辑
下图是book car demo的dialog tree

![Book Car Dialog Tree](/assets/images/watson-book-car-dialog.png)

Dialog tree匹配在文档中的术语叫dialog tree evaluation。这个evaluation是一轮一轮进行的，每一轮都从某一个节点开始。如下是文档原文。
>Tree evaluation is the processing of the user's input against the dialog flow that has been defined in the dialog builder. Dialog trees are evaluated in rounds, and a round always starts on a specific node.

文档里提到一个`contextual node`的概念，这个表示当前对话栈上的最近的一个节点，每个节点的信息包括用户的输入、响应以及配置UI中的相关节点属性。
>Each time the dialog returns a response and waits for user input, it stores the ID of the node at which the conversation should resume. This node is called the `contextual node`, and its ID is added to the `context.system.dialog_stack` property, which contains a JSON array of dialog node IDs that are currently on the dialog stack. The last node on this stack is the `contextual node` at which evaluation begins in the next round.

watson中是一个2-stage evaluation。第一步先查找当前`contextual node`的子节点，如果子节点找到则执行这个子节点的response，并将其放入堆栈。如果没有找到任何匹配的子节点，则进入第二阶段，用用户当前的输入去匹配top level dialog nodes，也就是第一层的节点。top level dialog nodes需要包含一个*anything_else*的节点作为最后一个节点，这样在用户输入没有任何匹配的时候能保证有响应，这个节点watson bot ui会自动帮助创建，这个节点和普通节点的区别在于condition是anything_else这个一个预定义的变量，具体可以参考开头的workspace json文件。

在这个评估的过程中，`contextual node`的选择逻辑是，如果当前节点没有子节点，是一个叶子节点，则`contextual node`置为*Conversation starts*这个虚拟根节点。下一轮会从当前的`contextual node`节点开始做2-stage evaluation。在匹配`contextual node`子节点的时候，是按照子节点在UI中的顺序来匹配的。


#### 关于Jump to
Jump to可以target到目的节点的condition或者response上，如果是到condition则会evaluate这个条件然后执行response中内容或者继续跳转，如果是response则会忽略这个节点的condition直接执行response内容。

还有jump to的目的节点能够直接用`@{entity_name}`获取到方式获取到从上个节点输入中识别的实体信息。

jump to node condition条件的执行策略如下
>**Condition:** If the statement targets the condition part of the selected dialog node, the service checks first whether the condition of the targeted node evaluates to true.
>
* If the condition evaluates to true, the system processes this node immediately by updating the context with the dialog node context and the output with the dialog node output.
* If the condition does not evaluate to true, the system continues the evaluation process of a condition of the next sibling node of the target dialog node and so on, until it finds a dialog node with a condition that evaluates to true.
* If the system processes all the siblings and no condition evaluates to true, the basic fallback strategy is used, and the dialog evaluates the nodes at the top level too.


不过对于Jump to逻辑，watson的策略最近做了升级，参看这一段描述就明白了，也就是jump to的节点及其peer节点如果都匹配不上会提示匹配失败，下一轮匹配将会从这个dialog的根节点开始。如果想保持原来的逻辑，在jump to的节点同一level最后加一个peer node，然后让其jump to整个dialog tree的root level的第一个节点。
>**Note:** the processing of Jump to actions changed with the February 3, 2017 release. Previously, if you jumped to the condition of a node, and neither that node nor any of its peer nodes had a condition that was evaluated as true, the system would jump to the root-level node and look for a node whose condition matched the input. In some situations this processing created a loop, which prevented the dialog from progressing. Under the new process, if neither the target node nor its peers is evaluated as true, the dialog turn is ended. Any response that has been generated is returned to the user, and an error message is returned to the application: Goto failed from node DIALOG_NODE_ID. Did not match the condition of the target node and any of the conditions of its subsequent siblings. The next user input is handled at the root level of the dialog. This update might change the behavior of your dialog, if you have Jump to actions that target nodes whose conditions are false. If you wish to restore the old processing model, simply add a final peer node with a condition of true and in the response use a Jump to action that targets the condition of the first node at the root level of your dialog tree.


#### Context变量
在Node编辑器重点击![](https://www.ibm.com/watson/developercloud/doc/conversation/images/json_16.png)可以修改context变量。在文档中我没看到在child node中如果获取上一轮识别的实体变量，我目前是用如下的方式解决的，也就是将这个变量放到上一轮的contex中，下一轮用`${variable_name}`方式访问，比如我在某些节点的response是这样的`your car is ready, have a nice trip to @location at $time`。context变量在上下两个节点之间传递的时候更新策略是相同属性名的替换，不同属性名的merge。

{% highlight json %}
{
  "context": {
    "time": "@time"
  },
  "output": {
    "text": {
      "values": [
        "where?"
      ],
      "selection_policy": "sequential"
    }
  }
}
{% endhighlight %}

#### 实体的挖掘和匹配
Watson中实体有用户自定义的和系统实体(system entities)，系统实体是通过大量语料挖掘的，用户自定义的实体就是一个完整的entity。假设system entities已经ready，实体识别就回归到倒排索引检索的问题了，不过这里面还有泛化的问题，数量词这些以及特殊字符(比如表示美元的$符号)需要做预处理，并且这个预处理在索引和查询的时候都需要。像时间啊、百分比、货币这种特别明确的entity，用正则基本就可以解决的差不多了，中文的数字比如`二十一`这种识别也可以用正则来处理，当然可能有更好的方法能解决适应性问题和多语问题。


#### 用户命名实体和系统自带实体
关于system entities有哪些可以参考[这里](https://www.ibm.com/watson/developercloud/doc/conversation/system-entities.html)

对于对话系统实体识别能力是必备的，系统级的实体也是必备能力，参考api.ai和watson都能发现这个实现逻辑，并且也能得到不少技术架构设计上的经验参考。

#### 参数补全的疑问
目前对于Intent匹配后实体参数补全的方案没有看到太好的文档描述，目前book car demo中是需要两个参数location和time，这个已经让这个dialog tree有点复杂了，如果需要5个实体参数呢？第一层分支逻辑会非常多(2^5，用0/1来表示每个参数的状态，因为用户的第一句就可能带上了部分或者全部需要的参数)，每一层再往下建立child node，工作量会非常大也比较容易出错。如果没有别的方法的话，那这个dialog tree只能用于简单的对话场景了。api.ai中是将Intent和Dialog的逻辑融合到一起了，对于参数补全是可以配置必选然后配置提问话术，系统会一直追问直到参数都补全，这个会更加方便。api.ai中intent(dialog)的上下文传递使用context input/output condition来控制的，理解起来不如watson这个直观，但也取得了更灵活的效果。如果将两者结合起来，用户体验会更加好一些。

#### 不同Intent之间转移和Context传递
拿play music这样的请求来说，用户发出这个请求后，系统会要求补充完相关的信息，比如歌星、专辑、歌曲名等，然后开始播放歌曲，再然后用户可以对这首歌曲执行暂停、快进、下一首、上一首等操作。这个在api.ai中是非常容易modeling的。在watson中做到类似功能dialog tree的构建可以再play music这个branch的叶子节点增加一个jump to到另一个top level node上，并且要把参数放到context中带过去，这样也就可以做到类似的效果，否则用户说了句pause，你都不知道去pause哪首歌。

# 遇到的问题

#### Intent匹配问题
输入anything else，我的intent配置中根本没有这样的句子，竟然匹配了book-car，和官方example对比了下，发现时语言选择的问题，好坑

![Intent Matching Problem](/assets/images/watson_intent_matching.png)

我重新换了个例子book-hotel，然后语言设置为English(U.S.)后就可以正常match intent了，match不到的会跑到anything_else分支去

![Watson Workspaces](/assets/images/watson_workspaces.png)

上面下载的book car demo是英文的，Intents匹配问题是我一开始设置的如下中文的Intents和Entities导致的

![Intents Configuration](/assets/images/watson-chinese-intents.png)

![Entities Configuration](/assets/images/watson-chinese-entities.png)

#### 参数补全问题
这个上面也描述了，目前还没想到简单的解决方案，有好的solution随时补充到这里.

**[2017-03-10更新]**：昨天(2017-03-09)睡觉前想到一个解决方法，今天试了下确实可以
[Book Hotel Demo Json File Download](/assets/data/watson-book-hotel-workspace.json)，思路就是每一层解决一个参数的识别问题，在识别intent后的子节点以及后续层，将参数通过context来传递下去，目前还遇到一个问题是最后一个节点用`$hotel_chain`来作为条件不work，但我增加一个peer节点同样用这个条件就ok了，懵逼了...，不知道是bug还是我弄错了啥

![Bool Hotel Explain](/assets/images/watson-book-hotel-dialog.png)

**[2017-03-11更新]**：昨天的问题今天晚上回头看终于定位到原因了，今天我把下图节点
的conditiaon修改为true仍然不work，我就开始怀疑底层的模型存储是不是出问题了。

![Watson Persistence Bug](/assets/images/watson_dialog_persistence_bug.png)

为了找出原因我把整个workspace导出成json文件，然后发现这个节点存储的状态还是以前的某个状态：
{% highlight json%}
    {
      "go_to": null,
      "output": {
        "text": {
          "values": ["@hotel_chain booked for you at $location on $time"],
          "selection_policy": "sequential"
        }
      },
      "parent": "node_12_1489110007522",
      "context": {"hotel_chain": "@hotel_chian"},
      "created": "2017-03-10T01:25:54.965Z",
      "updated": "2017-03-10T01:40:14.642Z",
      "metadata": null,
      "conditions": "@hotel_chain",
      "description": null,
      "dialog_node": "node_13_1489110014371",
      "previous_sibling": null
    }
{% endhighlight %}

我刷新整个页面，UI终于把这个底层模型展示出来了，我再修改为我预期的属性值，然后再尝试一轮对话发现就ok了，说明这个确实是UI界面和底层模型同步之间存在的bug，如果是网络异常或者什么原因同步不成功是要告知用户的，我在整个过程中没有看到任何提示或者警示。不过在这个json文件导出的时候也发现一个问题：`dialog_node`这个属性是UI中dialog的名字，如果不填充系统会用内部的某个id来代替，导出的json文件的可读性会受到很大影响，所以建议：**关键节点都要命名来提高可读性，会有利于debug**

最终的worksapce模型下载：[Book Hotel Demo Final Json File Download](/assets/data/watson-book-hotel-final-workspace.json)

最终的dialog tree:
![Bool Hotel Final Dialog Tree](/assets/images/watson-book-hotel-final-dialog.png)

**[2017-03-20更新]**: Book Hotel的参数填充被我整复杂了，雪峰给我建议了一个更[简单的方案](/assets/data/watson-workspace-order-dish.json),右键下载然后导入即可


# 欢迎交流
[联系方式点这里](/about)


[ibm-watson-how-to-build-a-chatbot]:https://www.ibm.com/watson/how-to-build-a-chatbot/
