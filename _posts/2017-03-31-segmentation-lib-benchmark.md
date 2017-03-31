---
title: 开源分词工具对比
category: nlp
tags: [nlp, 分词, 词性, segmentation, segment, pos tagging]
author: weiwei
---

* TOC
{:toc}

# 候选分词工具

参考清华NLP的对比试验[中文分词工具测评](http://rsarxiv.github.io/2016/11/29/%E4%B8%AD%E6%96%87%E5%88%86%E8%AF%8D%E5%B7%A5%E5%85%B7%E6%B5%8B%E8%AF%84/)的如下评测结果

msr_test（560KB）

Algorithm	| Time |	Precision |	Recall |	F-Measure
------------ | ------------- | ------------- | ------------- | -------------
LTP-3.2.0	| 3.21s |	0.867 | 0.896 |	0.881
ICTCLAS(2015版)	|	0.55s	|	0.869	|	**0.914**	|	**0.891**
jieba(C++版)	|	**0.26s**	|	0.814	|	0.809	|	0.811
THULAC_lite	|	0.62s	|	**0.877**	|	0.899	|	0.888


pku_test（510KB）

Algorithm	| Time |	Precision |	Recall |	F-Measure
------------ | ------------- | ------------- | ------------- | -------------
LTP-3.2.0	|	3.83s	|	**0.960**	|	**0.947**	|	**0.953**
ICTCLAS(2015版)	|	0.53s	|	0.939	|	0.944	|	0.941
jieba(C++版)	|	0.23s	|	0.850	|	0.784	|	0.816
THULAC_lite	|	0.51s	|	0.944	|	0.908	|	0.926


从F-measure上看，LTP>ICTCLAS>THULAC>jieba，jieba和其他三个精度差距较大，无法作为候选，LTP性能问题明显，NLPIR(ICTCLAS)-尝试了下发现在mac下run不起来(library无法加载)，此外社区和文档都比较弱，THULAC最近2017年3月还有更新，可以作为候选，此外比较流行的java分词工具还有ansj，HanLP这两个可以作为候选。

* THULAC-THU Lexical Analyzer for Chinese）由清华大学自然语言处理与社会人文计算实验室研制推出的一套中文词法分析工具包，具有中文分词和词性标注功能。
    * 能力强。利用我们集成的目前世界上规模最大的人工分词和词性标注中文语料库（约含5800万字）训练而成，模型标注能力强大。
    * 准确率高。该工具包在标准数据集Chinese Treebank（CTB5）上分词的F1值可达97.3％，词性标注的F1值可达到92.9％，与该数据集上最好方法效果相当。
    * 速度较快。同时进行分词和词性标注速度为300KB/s，每秒可处理约15万字。只进行分词速度可达到1.3MB/s。
    * 近1年内有更新维护
* Ansj-ict的真正java实现，分词效果速度都超过开源版的ict，支持中文分词、人名识别、词性标注、用户自定义词典
    * 这是一个基于n-Gram+CRF+HMM的中文分词的java实现。
    * 分词速度达到每秒钟大约200万字左右（mac air下测试），准确率能达到96%以上
    * 目前实现了：中文分词、中文姓名识别、用户自定义词典、关键字提取、自动摘要、关键字标记等功能
    * 可以应用到自然语言处理等方面，适用于对分词效果要求高的各种项目.
    * 近1年内有更新维护，更新活跃
* HanLP-(Han Language Processing)是由一系列模型与算法组成的Java工具包，目标是普及自然语言处理在生产环境中的应用。HanLP具备功能完善、性能高效、架构清晰、语料时新、可自定义的特点。
    * 中文分词
    * 词性标注
    * 实体识别
    * 关键词提取
    * 自动摘要
    * 短语提取
    * 拼音转换
    * 简繁转换
    * 文本推荐
    * 依存句法分析
    * 语料库工具
* NLPIR-尝试了下发现在mac下run不起来(library无法加载，no suitable image found)
    * mac下没跑起来
    * 文档较少，对java的支持不够，目前提供的都是jni方式

# 分词准确性
考虑到大家在项目中一般都是要处理比较general的分词需求，所以这里的对比试验中没有针对语料做训练，都是直接在测试数据上跑分词，然后用score工具评测，评测数据和工具使用的是第二届国际汉语分词测评中的素材，可以在这里[下载](http://sighan.cs.uchicago.edu/bakeoff2005/)

```
perl scripts/score gold/cityu_training_words.utf8 \
    gold/cityu_test_gold.utf8 test_segmentation.utf8 > score.ut8
```

msr_test（560KB）

Algorithm	|	Precision |	Recall |	F-Measure
------------ | ------------- | ------------- | -------------
THULAC_lite	|	0.859	|	0.887	|	0.872
ANSJ-ToAnalysis	|	0.875	|	**0.907**	|	0.891
ANSJ-NlpAnalysis	|	**0.895**	|	0.898	|	**0.897**
HanLP-StandardTokenizer	|	0.851	|	0.874	|	0.862
HanLP-NLPTokenizer	|	0.85	|	0.849	|	0.85


pku_test（510KB）

Algorithm	|	Precision |	Recall |	F-Measure
------------ | ------------- | ------------- | -------------
THULAC_lite	|	0.92	|	**0.908**	|	**0.914**
ANSJ-ToAnalysis	|	0.904	|	0.892	|	0.898
ANSJ-NlpAnalysis	|	**0.928**	|	0.882	|	0.904
HanLP-StandardTokenizer	|	0.899	|	0.888	|	0.893
HanLP-NLPTokenizer	|	0.886	|	0.852	|	0.869


# 词性标注准确性
测试方法，基于哈工大的"词性-词义_合并结果.txt"文件(下载自[哈工大同义词词林(扩展版)](http://www.ltp-cloud.com/download/))，对于每一行，评测分词结果相同的term总数累加为total，词性准确的term总数累加为correct， 最后通过correct/total计算词性识别的准确性

Algorithm	|	Precision
------------ | -------------
THULAC_lite	|	0.9179
ANSJ-ToAnalysis	|	**0.9338**
ANSJ-NlpAnalysis	|	0.929
HanLP-StandardTokenizer	|	0.924
HanLP-NLPTokenizer	|	0.919


# 结论

综合分词准确性和词性标注的准确性，ANSJ和THULAC相当，HanLP和这两个有差距，再结合ANSJ的发展历史较久，社区活跃，网上能搜到的信息较多，推荐选择ansj。如果是要求分词和词性标注较好的NLU场合，要用Ansj中的NlpAnalysis分词器（源代码注释是：自然语言分词，具有未登录词发现功能，建议在自然语言理解中用）

# 附-词性表格

符号	| 词性 |	解释 
------------ | ------------- | ------------- 
n|名词|取英语名词noun的第1个字母。
np|人名|
nr|人名|名词代码n和“人(ren)”的声母并在一起。
nh|人名|
ns|地名|名词代码n和处所词代码s并在一起
ni|机构名|
nz|其它专名|
nt|机构团体名|“团”的声母为t，名词代码n和t并在一起。
nl|名词性惯用语|
nd|方位名词|
ng|名词性语素|
b|区别词|
m|数词|取英语numeral的第3个字母，n，u已有他用。
q|量词|取英语quantity的第1个字母。
mq|数量词|
t|时间词|取英语time的第1个字母。
f|方位词|取汉字“方” 的声母。
s|处所词|取英语space的第1个字母
v|动词|取英语动词verb的第一个字母。
vd|副动词|
vn|名动词|
vshi|动词“是”|
vyou|动词“有”|
vf|趋向动词|
vx|形式动词|
vi|不及物动词（内动词）|
vl|动词性惯用语|
vg|动词性语素|
a|形容词|取英语形容词adjective的第1个字母。
an|名形词|
ad|副形词|
an|名形词|
ag|形容词性语素|
al|形容词性惯用语|
d|副词|取adverb的第2个字母，因其第1个字母已用于形容词。
h|前接成分|取英语head的第1个字母。
k|后接成分|
i|成语|取英语成语idiom的第1个字母。
j|简称|取汉字“简”的声母。
l|习用语|习用语尚未成为成语，有点“临时性”，取“临”的声母
r|代词|取英语代词pronoun的第2个字母,因p已用于介词。
c|连词|取英语连词conjunction的第1个字母。
p|介词|取英语介词prepositional的第1个字母。
u|助词|取英语助词auxiliary 的第2个字母,因a已用于形容词。
ud|结构助词|有
ug|时态助词|你
uj|结构助词的|迈向
ul|时态助词了|完成
uv|结构助词地|满怀信心
uz|时态助词着|眼看
y|语气助词|取汉字“语”的声母。
e|叹词|取英语叹词exclamation的第1个字母。
o|拟声词|取英语拟声词onomatopoeia的第1个字母。
g|语素|绝大多数语素都能作为合成词的“词根”，取汉字“根”的声母。
w|标点|
x|其它|非语素字只是一个符号，字母x通常用于代表未知数、符号。
z|状态词|取汉字“状”的声母的前一个字母。
tg|时语素|时间词性语素。时间词代码为t,在语素的代码g前面置以T。


# 参考

* [词性](http://itindex.net/detail/56121-%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80-%E8%AF%8D%E6%80%A7)
* [清华大学NLP分词工具](http://thulac.thunlp.org/)
* [哈工大语言云](http://www.ltp-cloud.com/)