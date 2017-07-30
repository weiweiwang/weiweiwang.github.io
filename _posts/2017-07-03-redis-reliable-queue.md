---
title: 使用Redis来实现消息的可靠发送
category: redis
tags: [redis,reliable queue,message,mq]
author: weiwei
---

* TOC
{:toc}

# 基于RPOPLPUSH消息处理流程
当我们需要一个可靠消息处理流程的时候，使用一般的消息队列会出现各种消息丢失的问题（比如程序重启，网络或者程序错误等），基于Redis的`RPOPLPUSH`可以实现一个可靠的消息处理，`RPOPLPUSH`在从队列(redis list)中取出消息的时候同时将消息放到另一个队列中，这整个过程是一个原子操作，官方文档中是这么举例描述的：
>For example: consider source holding the list a,b,c, and destination holding the list x,y,z. Executing RPOPLPUSH results in source holding a,b and destination holding c,x,y,z.

根据文档中提到的方法，整个消息流程处理逻辑如下:
```
msg = RPOPLPUSH message_queue processing_list
...process ${msg}...
lrem ${msg} from processing_list if process ${msg} succeed
```
由于消息处理过程中会有各种异常导致消息处理失败，这时候就会导致部分消息留在了`processing_list`中，需要有一个单独的monitor线程去不停的扫描`processing_list`来将处理失败的消息(超时)扔回消息队列`message_queue`

# 陷阱
官方文档中对`processing_list`的处理描述的很简单，在实际操作中有两个问题要考虑：

1. 如何遍历`processing_list`?
2. 怎么算超时?

问题1的遍历不能用pop这类修改list的操作，因为可能会遇到和消息处理一样的问题，pop出来后程序重启了或遇到了其他异常情况，这时候这一条消息还是丢掉了，我选择的是用`while(true)`不停的查看队尾元素`LRANGE processing_list -1 -1`，因为队尾元素也是在processing_list中待的时间最长的，如果超时则删除并放回队列，注意这里的删除和放回队列我用的是transaction(`lrem`,`lpush`)操作，目的还是要保证整个处理的原子性

问题2的超时设置也是一个关键问题，超时时间要设置的远大于一条消息正常处理的时常，因为在异常情况下会出现消息已经被处理，但又被扔回队列了，如果超时设置的比较短，这种情况发生的概率还不小，举例说明这个情况如何发生的：

1. `processing_list`monitor线程取出了队尾元素，发现其超时了，这时cpu时间片切换给其他线程了
1. 这时候处理线程发现这条消息处理完了，从`processing_list`中删除了这个消息
1. monitor线程还是把这个消息扔回队列了

如果monitor线程判断超时的时间很长，基本不会发生上述的并发冲突情况，当然这种并发冲突情况还是要补救的，我目前的补救方式是在monitor线程中用transaction删除`processing_list`中元素的时候检查返回值是否为1(也就是删除成功),如果不是说明发生了上面的并发冲突情况，立刻用transaction(`lrem`,`lrem`)删除`message_queue`和`processing_list`中的这条消息，由于刚才的放回使用的是lpush，也就是`message_queue`的头部，而消息处理逻辑使用的`RPOPLPUSH`是从队尾处理消息，所以正常情况下这种补救不会导致消息重复处理，可能存在的重复消息处理情况就是`message_queue`的消息非常少，消息一扔回去就被处理了，这种情况目前还没想到特别好的处理方法

# 扩展
在一个微信接入项目中，需要循环检查所有登录的微信是否有新消息，并且要考虑到横向扩展和消息处理的可靠性，我就用一个`message_queue`来保存了所有待检查的微信号(**带了时间戳，为了能检查超时**)，一个`processing_list`来保存正在被处理的微信号，每一个微信号检查完消息之后扔回`message_queue`，这个情形比上面描述的略复杂，上面的情形一个消息处理完就可以完全扔掉了，在这个微信接入项目中需要扔回去，所以对`processing_list`的处理逻辑就非常关键，搞不好就会有重复的微信号被扔到`message_queue`，我目前采用的方法就是从`processing_list`队尾取元素，monitor线程中用比较长的超时时间来检查一个微信号被处理的时常是否过长，同时在用transation做`lrem`,`lpush`之后立刻检查lrem的结果是否为1，如果不是立刻采用transation(`lrem`,`lrem`)来同时从`message_queue`和`processing_list`删除刚才扔回去的消息来避免重复处理。

# 参考
[RPOPLPUSH](https://redis.io/commands/rpoplpush)
