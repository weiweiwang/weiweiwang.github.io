---
title: 【转载】ChatBots调研-Chatfuel
category: chatbot
tags: [Chatfuel, chatbot]
author: lixin
---

* TOC
{:toc}

[转载自李欣blog](http://blog.xinlulicheng.net/?p=224)

# 总结

Chatfuel是一个能完成简单交互功能的“智能”机器人，它的最大优势在于纯界面化操作，因此操作门槛很低。当然，如果你是一名资深“程序猿”，你也可以通过插件与自己的服务实现通讯回调。相比其他的AI平台，例如API.AI、一个AI等，Chatfuel实际没有“意图识别”的功能，相关场景是用户构建好的，在bot构建的过程中也没有“实体”、“槽位”等概念，也不能建立私有的词库，甚至文本识别都不能做到模糊匹配。综上所述，Chatfuel的定位不是一个AI平台，因此它所包含的功能也无法提供给其他复杂AI应用使用。

# 什么是Chatfuel？
目前我了解到的Chatfuel与fackbook紧密绑在一起，它像一个智能管家机器人，帮你应答访问你主页用户的一些问题。按照官方解释：“它是Facebook页面的消息传递功能的扩展，每个Facebook机器人必须与现有的Facebook页面链接”。

当然，Chatfuel也有出名的地方，就是号称可以完全无需编码，拥有超低的使用门槛。但是感觉由于过度界面化管理，相比“api.ai”或“一个AI”，它的AI的功能显得并不那么强大。也许我没挖掘到更“厉害”的点吧！



# 如何使用Chatfuel？
首先，你必须拥有一个facebook账号，先前说过，目前我看到它是与facebook绑在一起使用的。虽然很早之前我就申请过facebook账号，但是对于facebook的使用频率低的可怜，这次也算是一起补习一下吧。

其次，当你登陆完成账号，打开chatfuel网站的时候，你有需要创建一个fackbook“主页”，也就是每一个机器人对应的一个facebook page页面。这个有点难理解，facebook的主页我也弄得不是很明白，创建分类很局限，也没有个人主页的分类可以选。为了继续调研，只好随便创建了一个。之后我们需要将chatfuel与你创建的主页进行绑定，如图：

![](http://blog.xinlulicheng.net/wp-content/uploads/2017/03/20170313070638_32914.png)      



连接到fackbook页面之后，终于我们可以开始玩我们的机器人了，进入正题，chatfuel如何去做一个最简单的交互机器人。

## 第一步：创建一个空的机器人
![](http://blog.xinlulicheng.net/wp-content/uploads/2017/03/20170313074806_48216.png)

## 第二步：认识机器人编辑界面
![](http://blog.xinlulicheng.net/wp-content/uploads/2017/03/20170313075332_46027.png)

在这里作为入门，我重点介绍下红框内的功能说明，大家了解这些就够用了。

* Build Menu：机器人可视化编辑的主要承载区域，在这里我们可以编辑所有与机器人交互可以看到的信息，并且都是图文可视化操作的。
* Set up AI Menu：文本对话编辑的主要承载区域，在这里我们可以编辑一些文本问答对，这个功能实在是low爆了，必须要完全匹配才可以。
* Bot Structure：机器人所有可编辑组件的工作区域，可以直观的看到你增加的组件Block。
* Build-In Blocks：机器人生成的时候默认配置的Block，包含“欢迎语”和“默认回复”，也就是当机器人启动的第一句话，以及当机器人无法理解时给的反馈，其他AI平台将这个反馈标记为”anything else”分支流程。
* Add Blocks Heres：自己增加的组件block管理区域，对应右侧的工作区。Block是机器人的基本构建块，它由一个或多个消息卡组成，一起发送给用户。
* Add A Group：帮你将杂乱的Blocks进行分组管理，例如你需要做一个订餐的机器人，那么就可以将早餐、午餐、晚餐进行block的分组管理，在可视化界面上也会看着更清晰一些。
* Add Button：大家在图上看到的“中餐”、“西餐”、“日料”，实际就是一个个button，可以通过配置指向跳转到其他的block，从而形成一系列问题应答的对话“流”，完成基本交互。也就是我们所谓的“意图”， chatfuel的意图是靠用户提前配置好的，而并不是通过AI的自然语义理解分析出来的。（是不是很low啊）。
* Card：是我们能编辑的一系列卡片
	* Gallery：简单的理解就是这种卡片可以配置图片+文本（主标题、副标题）+Button，比较丰富
	* Text：只能配置文本+Button
	* Image：显示一张图片
	* Quick Reply：快速应答回复，可以包含多个文本Button，一般用作选择性回复，如yes please！，no thanks！
	* Plugh：chatfuel支持的大量第三方插件，这里就不一一讲述了，感兴趣的同学可以看看下图基本就懂了（部分插件截图）。
	![](http://blog.xinlulicheng.net/wp-content/uploads/2017/03/20170313081538_86147.png)


## 第三步：让我们编辑一个自己的机器人
构造一个对话场景(B代表机器人,U代表用户)：

>B：询问聊天场景（工作、学习、生活） 
>
>U：选择“工作”
>
>B：推送工作相关信息，包含图片等 
>
>U：文字输入：“感谢，我了解的已经够多了” 
>
>B：“欢迎再来”

1. 修改welcome message blocks：修改为：“欢迎来到XX的主页，您想和我聊些什么？”，提供三个button：工作、学习、生活，暂时都创建关联welcome message本身。
![](http://blog.xinlulicheng.net/wp-content/uploads/2017/03/20170313084438_69316.png)

2. 创建工作组，并新增一个introduce的block，新建gallery card，配置相关button跳转和图片内容 
![](http://blog.xinlulicheng.net/wp-content/uploads/2017/03/20170313085303_35377.png)                                 
3. 配置Set up AI：配置Q&A应答，结束对话
![](http://blog.xinlulicheng.net/wp-content/uploads/2017/03/20170313085549_81303.png)
4. 测试Demo：
	* 点击：Test This Chatbot    
	![](http://blog.xinlulicheng.net/wp-content/uploads/2017/03/20170313090456_26001.png)                                                     
	* 在你的Facebook页面你会看到如下bot入口：
	![](http://blog.xinlulicheng.net/wp-content/uploads/2017/03/20170313090537_76392.png)                                                                                                            
	* 点击“发消息”，你会进入对话框：   
	![](http://blog.xinlulicheng.net/wp-content/uploads/2017/03/20170313090701_69206.png)                                                                                                                                        
	* 根据模拟场景流程，选择“工作”：
	![](http://blog.xinlulicheng.net/wp-content/uploads/2017/03/20170313090826_69583.png)                                                                                                                                             
	* 输入：“感谢，我了解的已经够多了”： 
	![](http://blog.xinlulicheng.net/wp-content/uploads/2017/03/20170313090936_60550.png)        
	                                                                                                                             
# 想想我们学会了什么，能做什么？
* 我们知道如何构建一个faceboot的chatbots了，而且我们学会了两个技能：创建card和增加set up ai配置
* 我们可以通过gallery card或text card去创建一个树状结构的引导对话。或者通过文本Q&A创建语言交互。只要我们将case准备的足够充分，这的确是一个可以进行自动回复交流的机器人
* 当然bot也有很多限制，例如text显示320个字符，button限制每个card只能有3个。我们不得不遵守这些规则，去创建我们想要的对话流程
* 当然，如果你是一个资深“程序猿”，你也可以不用界面化操作配置你的机器人，结合Web服务，你可以借用Json API和用户输入记录与你自己的智能服务进行交互，完成Facebook的交互应答。参考：
	* [JSON API](https://help.chatfuel.com/facebook-messenger/plugins/json-plugin/)
	* [USER INPUT](https://help.chatfuel.com/facebook-messenger/plugins/user-input/)

# 插件试用知多少？
插件也是chatfuel一项很强大的功能，上文也讲过，通过插件的使用，一些高级别的“程序猿”可以扩展一些AI服务完善自己的机器人。那么简单介绍一些常用的插件使用吧！

* 获取用户输入的信息：界面化的操作提供了UserInput插件来捕获用户的输入，将输入数据存储到一个变量里，具体使用参考下图：
![](http://blog.xinlulicheng.net/wp-content/uploads/2017/03/20170314054440_23136.png)
* API接口服务交互：Json Api提供了与第三方服务的简单交互能力，支持GET和POST，详细信息如下图，我们同样使用上个插件中获取到的{{num}}变量
![](http://blog.xinlulicheng.net/wp-content/uploads/2017/03/20170314054556_18374.png)

# 吐槽
一定有朋友会质疑，AI识别至少不会不支持模糊匹配，但是这的确是亲自测试的结果，再提供个官方样例的配置截图，如下图写法，说明不支持数字替换。
![](http://blog.xinlulicheng.net/wp-content/uploads/2017/03/20170313093108_66908.png)



# 参考
* [官方手册](https://help.chatfuel.com/facebook-messenger/ ): 有个快速学习的弹窗，也很有用，可惜没有链接，我看完就找不到了
* [官方模板](https://dashboard.chatfuel.com/#/bots): 便于理解机器人创建流程
* [http://www.anyv.net/index.php/article-511778](http://www.anyv.net/index.php/article-511778)
* [https://www.producthunt.com/posts/chatfuel-for-messenger](https://www.producthunt.com/posts/chatfuel-for-messenger)
* [http://www.minecraftxz.com/chatfuel/](http://www.minecraftxz.com/chatfuel/)