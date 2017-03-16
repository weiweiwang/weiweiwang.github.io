---
title: word2vec学习笔记
category: NLP
tags: [nlp,word2vector,cbow,skipgram]
author: weiwei
---
* TOC
{:toc}

# 什么是词向量

在介绍词向量之前我们先介绍下vector space model:

* 字典空间V
* 每一个词可以表示为一个V维的向量称作one-hot vector，这个词所在位置的向量元素值为1，否则为0, 举例:字典空间<am,is,are,this>, am的表示是[1,0,0,0]

词向量是将一个词映射到一个N维的实数向量上，目的要做到相近语义的次词向量也比较接近，体现为两个向量cosine的值较大，这便于从计算机角度比较两个词的相似性


# 为什么需要词向量

有时候我们需要表达字面意思之外的相似性来满足场景上的需求
比如年龄、几岁，再比如母亲节、康奶昔，这些词在one-hot vector上的表示是正交的，但从语义上他们是有相关性的。

# Word2Vector方法
word2vector本身是一个单隐层神经网络，用训练完的网络的输入层和隐藏层的权重来表示每个词的词向量，这里介绍两种方法: CBOW(continuous bag of words)和Skig Gram

## BOW
下图是CBOW的网络结构

![cbow]({{ site.url }}/assets/images/cbow.png)

这里使用某个词![equation](http://latex.codecogs.com/svg.latex?\matchbf{w_t})前后的若干个词作为输入![equation](http://latex.codecogs.com/svg.latex?\matchbf{x})，![equation](http://latex.codecogs.com/svg.latex?\matchbf{w_t})作为要预测的输出![equation](http://latex.codecogs.com/svg.latex?\matchbf{y})，这里假设窗口大小为4，也就是用连续的5个词中间的词![equation](http://latex.codecogs.com/svg.latex?\mathbf{w_t})作为![equation](http://latex.codecogs.com/svg.latex?\mathbf{y}), 前后各两个词作为输入![equation](http://latex.codecogs.com/svg.latex?\mathbf{w_{t-2}}), ![equation](http://latex.codecogs.com/svg.latex?\mathbf{w_{t-1}}), ![equation](http://latex.codecogs.com/svg.latex?\mathbf{w_{t+1}}), ![equation](http://latex.codecogs.com/svg.latex?\mathbf{w_{t+2}})，这里的![equation](http://latex.codecogs.com/svg.latex?\mathbf{w})是一个one-hot vector，大小是词典的大小V。由于这里是4个one-hot vector，但图中我们看到输入和隐藏层是一个权重矩阵![equation](http://latex.codecogs.com/svg.latex?W_{V\times%20N})，那这个输入到隐藏层是如何计算的呢，论文和各种文章里会介绍将这4个向量拼成了一个![equation](http://latex.codecogs.com/svg.latex?4\times%20V)的向量，然后计算隐藏层的输出，这个解释会让大家很困惑，实际上做法是分别和![equation](http://latex.codecogs.com/svg.latex?W_{V\times%20N})做矩阵乘法然后计算平均值，换一个思维是实际上的输入是：![equation](http://latex.codecogs.com/svg.latex?(w_{t-2}+w_{t-1}+w_{t+1}+w_{t+2})/4)，这样理解起来就简单了，相当于还是一个V维的输入向量，这里面还有一个特殊的地方是隐藏层是没有激活函数的，所以隐藏层的输出向量![equation](http://latex.codecogs.com/svg.latex?h=W_{V\times%20N}^T\times%20\(w_{t-2}+w_{t-1}+w_{t+1}+w_{t+2}\)/4)，注意这里4是为了举例子，实际情况中根据窗口大小来调整。


### BOW loss function
以下是参考论文和网上文章中的公式推导，便于了解BP的原理，使用现成的library中有很多参数会和这些推导过程相关，了解之后有助于使用。

假设window size是C个词(表示上下文context):![equation](http://latex.codecogs.com/svg.latex?\{x_1,...,x_c\})，那么隐藏层
![equation](http://latex.codecogs.com/svg.latex?h=W_{V\times%20N}^{T}\frac{\sum_{i=1}^{C}\mathbf{x_i}}{C})

定义Loss function E如下：

![equation](http://latex.codecogs.com/svg.latex?E=-\log%20p(w_o\mid%20w_{i,1},\ldots,w_{i,C}))

![equation](http://latex.codecogs.com/svg.latex?=-u_{j^*}+\log\sum_{j\prime=1}^{V}\exp(u_j^\prime))

![equation](http://latex.codecogs.com/svg.latex?=-{v^\prime}_{w_o}^{T}\cdot%20{h}+\log\sum_{j^\prime=1}^{V}\exp({v^\prime}_{w_j}^{T}\cdot\%20{h}))

对输出层softmax之前的u做偏微分：

![equation](http://latex.codecogs.com/svg.latex?\frac{\partial{E}}{\partial{u_j}}=y_j-t_j=e_j)
其中![equation](http://latex.codecogs.com/svg.latex?t_j=1(j=j^*))

对隐藏层到输出层的权重做偏微分：

![equation](http://latex.codecogs.com/svg.latex?\frac{\partial{E}}{\partial{w^\prime_{ij}}}=\frac{\partial{E}}{\partial{u_j}}\cdot\frac{\partial{u_j}}{\partial{w^\prime_{ij}}}=e_j\cdot%20h_i)

隐藏层到输出层的权重更新：

![equation](http://latex.codecogs.com/svg.latex?{v^\prime}_{w_j}={v^\prime}_{w_j}-\eta\cdot%20e_j\cdot%20{h})


对隐藏层的输出做偏微分：

![equation](http://latex.codecogs.com/svg.latex?\frac{\partial{E}}{\partial{h_i}}=\sum_{j=1}^{V}\frac{\partial{E}}{\partial{u_j}}\cdot\frac{u_j}{h_i}=\sum_{j=1}^{V}e_j\cdot%20w^\prime_{ij}:={EH}_i)

输入层到隐藏层的权重更新：

![equation](http://latex.codecogs.com/svg.latex?{v}_{w_{I,c}}={v}_{w_{I,c}}-\frac{1}{C}\eta\cdot%20e_j\cdot%20{h})


## Skip-Gram
![skipgram]({{ site.url }}/assets/images/skipgram.png)

这个模型可以看做CBOW模型的翻转，现在输入变成了某一个词，输出变成了这个词的上下文(context)

这时候隐藏层的输出为
![equation](http://latex.codecogs.com/svg.latex?h=W_{k,\cdot}^T:=v_{w_I}^T)

由于隐藏层到输出层的权重是共享的，所以每个输出![equation](http://latex.codecogs.com/svg.latex?y)是相同的

![equation](http://latex.codecogs.com/svg.latex?p(w_{c,j}=w_{O,c}\mid%20W_I)=y_{c,j}=\frac{\exp(u_{c,j})}{\sum_{j^\prime=1}^{V}\exp(u_{j^\prime})})其中![equation](http://latex.codecogs.com/svg.latex?u_{c,j}=u_j=v^\prime_{w_j}^T\cdot%20h), ![equation](http://latex.codecogs.com/svg.latex?v^\prime_{w_j})是隐藏层到输出层参数矩阵的某一列

### Skip-Gram loss function
我们先定义Loss Function， 最大化给定w情况下上下文的输出概率，反过来就是最小化这个概率的负数，如下：

![equation](http://latex.codecogs.com/svg.latex?E=-\log%20p(w_{O,1},\ldots,w_{O,C}\mid%20w_I)=-\log\prod_{c=1}^C\frac{\exp(u_{c,j_c^*})}{\sum_{j^\prime=1}^{V}\exp(u_j^\prime)})

![equation](http://latex.codecogs.com/svg.latex?=-\sum_{c=1}^{C}u_{j_c^*}+C\cdot\log\sum_{j^\prime=1}^{V}\exp(u_{j^\prime}))

计算E的偏微分:
![equation](http://latex.codecogs.com/svg.latex?=\frac{\partial{E}}{\partial{u_{c,j}}}=\sum_{c=1}^{C}(y_{c,j}-t_{c,j})=\sum_{c=1}^{C}e_{c,j})


为了简化，我们定义![equation](http://latex.codecogs.com/svg.latex?{EI}=\{ {EI}_1,\ldots,{EI}_V\})，其中
![equation](http://latex.codecogs.com/svg.latex?{EI}_j=\sum_{c=1}^{C}e_{c,j})

针对隐藏层到输出层的权重计算偏微分：
![equation](http://latex.codecogs.com/svg.latex?\frac{\partial{E}}{\partial{w^\prime_{ij}}}=\sum_{c=1}^{C}\frac{\partial%20E}{\partial%20u_{c,j}}\cdot\frac{\partial%20u_{c,j}}{\partial{w^\prime_{ij}}})


![equation](http://latex.codecogs.com/svg.latex?={EI}_j\cdot%20h_i)

则隐藏层到输出层的更新函数为：
![equation](http://latex.codecogs.com/svg.latex?w^\prime_{ij}=w^\prime_{ij}-\eta\cdot%20{EI}_j\cdot%20h_i)

输入层到隐藏层的更新函数可以参考BOW中的分析：
![equation](http://latex.codecogs.com/svg.latex?v_{wI}=v_{wI}-\eta\cdot{EH}^T)其中![equation](http://latex.codecogs.com/svg.latex?{EH}_i=\sum_{j=1}^{V}{EI}_j\cdot%20w^\prime_{ij})


# Sentence2Vec
待调研，可参考如下文章：

* [stentence vector from word vector](http://stackoverflow.com/questions/29760935/how-to-get-vector-for-a-sentence-from-the-word2vec-of-tokens-in-sentence)
* [paragraph vector](https://cs.stanford.edu/~quocle/paragraph_vector.pdf)
* [Distributed Representations of Words and Phrases
and their Compositionality](https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf)

>There are differet methods to get the sentence vectors :

>Doc2Vec : you can train your dataset using Doc2Vec and then use the sentence vectors.
Average of Word2Vec vectors : You can just take the average of all the word vectors in a sentence. This average vector will represent your sentence vector.
Average of Word2Vec vectors with TF-IDF : this is one of the best approach which I will recommend. Just take the word vectors and multiply it with their TF-IDF scores. Just take the average and it will represent your sentence vector.


# 参考
[word2exp explaination](http://www-personal.umich.edu/~ronxin/pdf/w2vexp.pdf)

[dl4j word2vec](https://deeplearning4j.org/word2vec.html)
