---
layout: post
title: 轻量级近景人像检测
author: weiwei
category: ai
tags: [人脸检测，face detection]
---

* TOC
{:toc}

# 背景
最近由于产品需要，需要研究下如何识别用户上传的照片人像是否合适，以及如何做背景和人脸替换。
调研了几个成熟实现最终选用了非常轻量级的mediapipe，下面分享下大致遇到的问题和解决思路。

# 问题分析
用户上传的照片主要存在几方面问题：
1. 不包含人像
2. 包含多个人像
3. 人像超出图片
4. 人像太远
5. 偏离中心
6. 侧脸
7. 不合规图片过滤

# 问题解决
识别的步骤:
1. 用工具识别出每张人脸的位置和关键点
2. 不包含和包含多个很好判断，不过多介绍
3. 人像超出图片：情况是人脸识别出来的宽度会出现负数或者>1的情况，这个可以作为这个判断依据
4. 人像太远：转化为程序逻辑就是人脸占照片的比例太小，比如横向占比<10%
5. 偏离中心：这个可以基于鼻子这个关键点的位置来判断
6. 侧脸：判断左眼睛和左耳朵的距离 以及 右眼睛和右耳朵的距离的相对大小
7. 图片合规审核：接入了某AI大厂的图片审核API

# 效果
扫码点击任意人像后自行上传图片体验效果：

![扫码体验](https://cdn.avatar.dmc-ai.cn/avatar/images/2024/02/06/4K6tZMunytDP5shp.jpeg)

# 一点感受
* 用户是非常多样化的，产品要能提供比较顺滑的体验
* 用户很想要一个好玩的产品，但怎么算好玩用户也不知道，对于产品和技术就要多挖掘和思考
* 很多开源工具离商用还有很远的距离，拿来就能用的不多，这个过程要做好场景覆盖测试


# 祝大家新年快乐
[![Watch the video](https://cdn.avatar.dmc-ai.cn/avatar/images/2024/02/06/EkJrDM47NuWPVrMr.jpeg)](https://cdn.avatar.dmc-ai.cn/avatar/videos/2024/02/02/UQSWmRdskw29BM7b.mp4)


# 参考
* [Photoroom](https://www.photoroom.com/): 图片处理工具，抠图换背景效果很不错
* [Mediapipe](https://developers.google.com/mediapipe): google开源的媒体处理AI工具，非常轻量级，支持移动端调用
* [PixelLib](https://github.com/ayoolaolafenwa/PixelLib): 开源库，图像分割场景，效果一般，主要分割和抠图不一样
* [U-2-Net](https://github.com/xuebinqin/U-2-Net)：开源的抠图工具
* [MODNet](https://github.com/ZHKKKe/MODNet): 开源的抠图工具，效果比U-2-Net要好

# 下期预告
下一期分享抠图相关的实践，如果有兴趣一起探讨产品和技术可以邮件联系[巍巍](mailto:wangweiwei@dmc-ai.com)
