title: 优化网站访问速度
slug: optimize-web-speed
category: programming
tags: cdn,optimize,speed,webpage,gzip
date: 2012-11-11

[TOC]

#减少HTTP请求数
减少页面上css,js,图片的文件个数。

#使用内容分发网络(CDN)
解决夸地域访问使用CDN是最好的方式了，省钱又省力。

# Expires and Cache-Control
设置页面的Expires和Cache-Control:max-age来缓存页面，注意这时候服务端的访问统计就会受影响了，建议使用百度统计或者google统计来解决页面访问统计的问题。

#使用Gzip压缩
这个不用多说了，压缩为50%是很正常的，通常压缩比可以达到1/8或者更高(1/10)。这对于传输来说时间减少非常明显。

#css在前，js在后,不要在CSS中使用js
css放到Head里，js放到页面最后，避免在css中使用js表达式。
	
#css，js用外部文件，不要写在html中
css和js写在页面里面确实可以减少请求次数，但也存在的问题是这写不经常改变的资源也随着这个页面无法cache了，或者cache时间无法很长（页面需要更新）。所以这个必须折中考虑，并且应该尽量将css和js放在单独的文件中，然后include，这部分资源的cache时间可以设置很长，通过文件名戴上版本号来更新资源。

#压缩js，css
[YUI Compressor](http://developer.yahoo.com/yui/compressor/)你可以试试。

#减少Redirect
301,302这个是不cached


#Etag和Last-Modified Header
这些Header可以有助于产生304,避免相同内容重复传输。


#Ajax请求尽量多是GET请求
XMLHttpRequest的POST请求是个两阶段的，先发送header再发送data，如果不是提交数据而是请求数据的情况下，尽量使用GET请求来减少网络耗时。

#预加载和延迟加载
有些资源比如在下一个页面是需要的，可以在前一个页面用js来预加载。同时有些资源是在页面渲染完用户采取动作后才需要的，在当前页面就可以采用延迟加载来提高用户体验。

#减少页面复杂度
减少DOM元素的个数对提升页面速度是很有帮助的。[YUI CSS utilities](http://developer.yahoo.com/yui/)可以用来帮助你布局页面。

#使用多个域来提供性能
多个域有助于提高下载并发度，但同时dns lookup也是一个考虑因素，一般不建议超过4个域。

#减少Cookie体积
cookie在请求的时候都会携带在header中的，所以不要携带过长或没有意义的cookie。

#DOM access
[High Performance Ajax Applications](http://yuiblog.com/blog/2007/12/20/video-lecomte/)这个对提高Ajax的效率应该有帮助。

#图片尺寸优化
现在网站都用很多图片，效果是好看了，但速度上一定得做好优化。压缩图片体积，合并多张图片用css裁剪都是有效的提高加载速度的方法。


#参考
[Best Practices for Speeding Up Your Web Site](http://developer.yahoo.com/performance/rules.html)
