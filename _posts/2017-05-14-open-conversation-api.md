---
title: 开放域对话
category: chatbot
tags: [ domain,spoken dialogue system]
author: weiwei
---

* TOC
{:toc}


# 常见方法
目前我们国内常见的开放式机器人

* Retrieval Model，基于检索的模型，在特定的对话数据集上，使用一些规则、启发式方法、机器学习方法、搜索技术来实现最优响应的选择。在语料足够多的情况下，对话可能七七八八我们觉得还是比较make sense的，但如果有点上下文，这个方法就很难handle了，下图是图灵机器人的例子

![](/assets/images/tuling.png) 
        
* Generation Model，生成式模型，不依赖于固定的问题回答集合，这个方法从已有的corpus中学习到一个生成式模型，目前常用的方法就是RNN，之所以用带记忆能力的RNN(LSTM)也不难理解，RNN有记忆就可以有上下文。但这类方法存在的问题是生成的response无法解释，也可能会语义不通顺，所以目前这个方法还不成熟，这也就是为什么目前主要是基于检索的模型被大量应用到生产中。这里推荐大家看看这个李宏毅老师的课程视频[Conditional Generation by RNN & Attention](https://www.youtube.com/watch?v=f1KUUz7v8g4)

* Hybrid模型，看到hybrid大家就可以很容想到这个方法是上述两个方法的混合体，这也是目前比较practical的方法，我们可以看到基本上现有的对话系统都会结合两种方式，或者正在给retrieval model增加生成式方法来增强对话的合理性，让对话逐步能理解上下文，我们来看这篇[阿里小蜜技术揭秘文章](http://mini.eastday.com/mobile/170301092324458.html)中的陈述，这是一个使用Hybrid模型的实例，并且影响力也是非常大的一个系统，而京东JIMI还有比较长的路要走：
> * 一种是Generation Model(生成模型)：
>	1. 优点：通过深层语义方式进行答案生成，答案不受语料库规模限制；
>	2. 缺点：模型的可解释性不强，且难以保证一致性和合理性回答。
>另外一种方式就是通过传统的检索模型的方式来构建语聊的问答匹配。
> * Retrieval Model(检索模型)：
>	1. 优点：答案在预设的语料库中，可控，匹配模型相对简单，可解释性强；
>	2. 缺点：在一定程度上缺乏一些语义性，且有固定语料库的局限性。
>
>因此在阿里小蜜的聊天引擎中，我们结合了两者各自的优势，将两个模型进行了融合形成了阿里小蜜聊天引擎的核心。先通过传统的检索模型检索出候选集数据，然后通过Seq2Seq Model对候选集进行Rerank，重排序后超过制定的阈值就进行输出，不到阈值就通过Seq2Seq Model进行答案生成，整体流程如下图：
>![](https://07.imgmini.eastday.com/mobile/20170301/20170301092324_fb1cde294ca9cad82605d13e8d0695aa_14.jpeg)


# 核心能力
基于上面的方法的介绍，我们很容易看出来目前做开放域对话的瓶颈在什么地方--**数据、数据、数据**。而数据的收集是一个比较漫长的过程，所以竞争力的体现就是一个先发优势和规模的问题，至于技术目前不再是核心瓶颈。

具有对话场景的产品比如微博、贴吧、IM软件和一些对话能力平台(如tuling)，并且已经积累了一定量的用户，就无疑具有了非常好的数据优势，这个优势是新进入者短期内无法赶超，指望抓取数据不可能超越，只能解决冷启动的问题。


# 对比
目前国内的我试了下小黄鸡和图灵，试了一些对话场景（非严格对比测试）发现还是图灵的回答体验更好一些，虽然都还谈不上能够流畅对话，但图灵能够做到回答的更精准、更丰富、并且更少黄段子。。。

# 思考
现在越来越多的场景用上了聊天能力，所以目前这类聊天平台一下又火起来了，但仅仅提供这样的api是比较危险的，要提供完整的solution才会比较有持久的竞争力，我们看出门问问和小米的合作就能看出来，如果只是提供了语义理解、语音识别建模这样的能力，而上层入口不在可控范围内，被replace的成本其实不大，当然不可能什么都做，但具有一定的不可替代性这样的危机意识是不得不时刻保持的

# API
基于开放的api我做了封装(目前只是集成了图灵和翻译api，后续会扩充)，现release第一版给大家使用，目图灵返回的图片和新闻质量一般，我做了替换，当前也不支持简单的上下文，比如你问：天气怎样，他会问你的城市，当你说了城市信息，他回答的是城市的介绍，把天气这事给忘记了，这个也留作后续改进的内容，有任何使用上的疑问请移步[About](/about)加微信咨询。

## 调用代码示例
下面是java代码样例，uid是用户的唯一标示，留作上下文处理用，目前还不支持上下文，后续增加支持就会依赖这个uid信息
```
conversation.appkey=677fe98541c91845abb2ffbfb1f72de5
conversation.appsecret=d33a550a38bc11e7b85cb8e8563bd1d0
conversation.api=http://caap.prototypeplus.org/api/v2/conversation

        HttpUrl.Builder builder = HttpUrl.parse(configuration.getString("conversation.api"))
                .newBuilder()
                .addEncodedQueryParameter("q", URLEncoder.encode(question,"UTF-8"))
                .addQueryParameter("uid", uid)
                .addQueryParameter("appkey", configuration.getString("conversation.appkey"));

        HttpUrl httpUrl = builder.build();
        Map<String, String> signParams = new TreeMap<>();
        httpUrl.queryParameterNames()
                .forEach(name -> signParams.put(name, httpUrl.queryParameterValues(name)
                        .get(0)));


        StringBuilder stringBuilder = new StringBuilder();
        for (Map.Entry<String, String> entry : signParams.entrySet()) {
            String k = entry.getKey();
            String v = entry.getValue();
            stringBuilder.append(k).append(v);
        }
        stringBuilder.append(configuration.getString("conversation.appsecret"));
        String sign = DigestUtils.md5Hex(stringBuilder.toString().getBytes("UTF-8"));
        builder.addQueryParameter("sign", sign);
        Request request = new Request.Builder().url(builder.build()).build();

        Response response = okHttpClient.newCall(request).execute();
        String responseText = response.body().string();
        ObjectNode objectNode = CommonUtils.JACKSON_OBJECT_MAPPER
                .readValue(responseText, ObjectNode.class);
```

返回值的样例：

```
{
   "code":200,
   "time":1494781827320,
   "msg":"ok",
   "data":{
      "text":"亲，已帮你找到图片",
      "category":"link",
      "url":"http://image.baidu.com/search/wiseala?tn=wiseala&word=%E6%9D%A5%E4%B8%AA%E7%BE%8E%E5%A5%B3%E5%9B%BE%E7%89%87"
   }
}
```

## category字段说明5
* text
```
{
   "code":200,
   "time":1494777834931,
   "msg":"ok",
   "data":{
      "category":"text",
      "text":"颜延之是南北朝时期宋国的文学家。颜延之交友广泛，与当时的名士何尚之有很深的友谊。二人虽然都以文采、学识盛名，但长相丑陋，个子矮小。二人甚至互相戏称对方为猴子。一次，两人结伴到太子西池游览。路上碰到一个行人。颜延之就开玩笑地问行人：“你看我们两个人谁更像猴子？”行人不认得两位大人物，就坦率地指着何尚之说：“我觉得他长得很像。” 颜延之听了十分得意。但是，行人又接着说：“他长得像猴子，可是先生您却是真的猴子！” 何尚之不顾形象地哈哈大笑起来。"
   }
}
```
* link
```
{
   "code":200,
   "time":1494781827320,
   "msg":"ok",
   "data":{
      "text":"亲，已帮你找到图片",
      "category":"link",
      "url":"http://image.baidu.com/search/wiseala?tn=wiseala&word=%E6%9D%A5%E4%B8%AA%E7%BE%8E%E5%A5%B3%E5%9B%BE%E7%89%87"
   }
}
```
* news
```
{
   "code":200,
   "time":1494782661996,
   "msg":"ok",
   "data":{
      "text":"亲，已帮您找到相关新闻",
      "category":"news",
      "list":[
         {
            "icon":"https://pic2.zhimg.com/v2-112b7400e1ca4dd3ec8d8486729d5855.jpg",
            "source":"知乎",
            "title":"小事 · 成为母亲的代价",
            "url":"http://daily.zhihu.com/story/9397327"
         },
         {
            "icon":"https://pic1.zhimg.com/v2-6bbcb10411c2770de80934de64de4368.jpg",
            "source":"知乎",
            "title":"3 段太过经典的床戏，掩盖了《色，戒 》里真正的爱情",
            "url":"http://daily.zhihu.com/story/9416252"
         },
         {
            "icon":"https://pic2.zhimg.com/v2-91d89736f690ad0d34020f6c58040de1.jpg",
            "source":"知乎",
            "title":"- 天上的一颗星就是……\r\n- 不对，数量完全不一样",
            "url":"http://daily.zhihu.com/story/9419736"
         },
         {
            "icon":"https://pic2.zhimg.com/v2-a9d41f20f056f9262a22174bac447b35.jpg",
            "source":"知乎",
            "title":"竟然有谣言说孕妇不用吃叶酸，这事必须义正辞严地反驳",
            "url":"http://daily.zhihu.com/story/9419481"
         },
         {
            "icon":"https://pic3.zhimg.com/v2-4fd43d967aeba1dbe4484565de0b1892.jpg",
            "source":"知乎",
            "title":"那些创业失败的人，问题出在了哪儿？",
            "url":"http://daily.zhihu.com/story/9420032"
         },
         {
            "icon":"https://pic3.zhimg.com/v2-01ca2cf9a25305bb71c8d61986c57652.jpg",
            "source":"知乎",
            "title":"- 猫：嗯，爱你\r\n- 狗：我真的很爱爱爱爱爱你",
            "url":"http://daily.zhihu.com/story/9419790"
         },
         {
            "icon":"https://pic1.zhimg.com/v2-83e227acc16f4d4788b4959f7db0f18c.jpg",
            "source":"知乎",
            "title":"为什么高铁站台没有像地铁一样装屏蔽门？",
            "url":"http://daily.zhihu.com/story/9419650"
         },
         {
            "icon":"https://pic4.zhimg.com/v2-adb6fba068b8f0f09381e4c87d41269f.jpg",
            "source":"知乎",
            "title":"玩游戏就能理财赚钱？卧底玩家群才发现是「新型传销」",
            "url":"http://daily.zhihu.com/story/9419798"
         },
         {
            "icon":"https://pic2.zhimg.com/v2-a83f52b8adcf3901ec7028b94ac5e585.jpg",
            "source":"知乎",
            "title":"小时候总是被妈妈带出去玩的我们，该带妈妈去哪里玩？",
            "url":"http://daily.zhihu.com/story/9419471"
         },
         {
            "icon":"https://pic4.zhimg.com/v2-d8b28b9a32717fb4582cbfa3c88b9f9f.jpg",
            "source":"知乎",
            "title":"漂泊在外的人总要回家，因为还有一碗「卤水」等着你",
            "url":"http://daily.zhihu.com/story/9417843"
         },
         {
            "icon":"https://pic3.zhimg.com/v2-522f8e511d675f8a9425b988f16fef9e.jpg",
            "source":"知乎",
            "title":"大误 · 网文还是得这么写",
            "url":"http://daily.zhihu.com/story/9418759"
         },
         {
            "icon":"https://pic2.zhimg.com/v2-343eb692e3b9c14157ce3142820e0b15.jpg",
            "source":"知乎",
            "title":"母亲节 · 他们说，「孩子是你生的，相夫教子是应该的」",
            "url":"http://daily.zhihu.com/story/9419430"
         },
         {
            "icon":"https://pic1.zhimg.com/v2-0b0f0e0cd87899244c9de7209afdfab0.jpg",
            "source":"知乎",
            "title":"有什么法律可以管管「网络暴力」吗？",
            "url":"http://daily.zhihu.com/story/9417056"
         },
         {
            "icon":"https://pic4.zhimg.com/v2-79e2e3a52f45664aa7ce5ff0372345bb.jpg",
            "source":"知乎",
            "title":"《银河护卫队 2》有哪些漫画里才有的背景知识？",
            "url":"http://daily.zhihu.com/story/9416860"
         },
         {
            "icon":"https://pic2.zhimg.com/v2-8de41aa38390ea2246187895ff45379d.jpg",
            "source":"知乎",
            "title":"谈恋爱会「作」，当然还是因为「作」很有用嘛",
            "url":"http://daily.zhihu.com/story/9418848"
         },
         {
            "icon":"https://pic2.zhimg.com/v2-6e15ffdc6707939d1ae7525e0c1d9489.jpg",
            "source":"知乎",
            "title":"「我从小看到的上海，更多的是一个克勤克俭的上海」",
            "url":"http://daily.zhihu.com/story/9418846"
         },
         {
            "icon":"https://pic2.zhimg.com/v2-db690f96a173e300f2c7abbfd8dab839.jpg",
            "source":"知乎",
            "title":"老板跟会计不一样，抓住这 8 个关键点就差不多了",
            "url":"http://daily.zhihu.com/story/9416452"
         },
         {
            "icon":"https://pic2.zhimg.com/v2-fb04739e1ddb6b91fb01ae09be07f3c9.jpg",
            "source":"知乎",
            "title":"刘看山 · 千万别多想",
            "url":"http://daily.zhihu.com/story/9417004"
         },
         {
            "icon":"https://pic1.zhimg.com/v2-f1f4e148dcfc9c10c55e0b6adb8cf984.jpg",
            "source":"知乎",
            "title":"瞎扯 · 如何正确地吐槽",
            "url":"http://daily.zhihu.com/story/9416224"
         }
      ]
   }
}
```
* cookbook
```
{
   "code":200,
   "time":1494778324584,
   "msg":"ok",
   "data":{
      "text":"亲，已帮你找到菜谱信息",
      "category":"link",
      "url":"http://m.haodou.com/recipe/search?keyword=%E7%83%AD%E9%97%A8%7E"
   }
}
```