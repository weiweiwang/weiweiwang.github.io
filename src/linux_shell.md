title: 常用shell命令
slug: common-shell-command
category: misc
tags: bash,shell,log

# 测试文件
## test.txt
	title
	slug
	category
	tag
	slug
	tag

#sort
这个命令可以对文件或者输入流进行排序输出。
## 常用参数说明
* -t 分隔符，通过这个可以将每一行分隔成若干字段，比如\t分隔的时候要传递-t $'\t'
* -k 选择排序的字段，比如以第一个字段k1,1，以前两个字段排序的话就是-k1,2
* -n 以数字排序而非字符串的字典序
* -r 倒序排列

## 举例

	>cat test.txt|sort -t $'\t' -k1,1 -r
	title
	tag
	tag
	slug
	slug
	category
#uniq
这个命令可以统计文件中重复行，需要输入是排序过的。
## 常用参数说明
* -f 表示跳过若干个字段，也就是这写字段不作为唯一性检查的key，分隔符是空白字符，无法指定
* -s 表示跳过若干个字符
* -c 打印重复行的数目
* -i 忽略大小写
* -d 只输出重复行
* -u 只输出不同的行

需要注意的是uniq输入需要是sort过的，否则结果不正确。

## 举例

	>cat test.txt|sort -t $'\t' -k1,1|uniq -c
	1 title
	2 tag
	2 slug
	1 category


#join
这个命令可以join两个文件中的若干列，类似与mysql的join命令, 输入的文件需要是排序过的。
## 常用参数说明
* -1 第一个文件的join字段
* -2 第二个文件的join字段
* -o 指定输出格式，每个字段的格式是M.N，M是文件编号1或者2,N是字段编号，从1开始。
* -t 指定分隔符，类似与sort命令中的-t

## 举例

	>sort test.txt > 1.txt
	>head -1 1.txt > 2.txt
	>join -1 1 -2 1 -o 1.1 2.1 -t $'\t' 1.txt  2.txt
	category	category

#awk
awk是一种编程语言，用于在linux/unix下对文本和数据进行处理。数据可以来自标准输入、一个或多个文件，或其它命令的输出。它支持用户自定义函数和动态正则表达式等先进功能，是linux/unix下的一个强大编程工具。它在命令行中使用，但更多是作为脚本来使用。awk的处理文本和数据的方式是这样的，它逐行扫描文件，从第一行到最后一行，寻找匹配的特定模式的行，并在这些行上进行你想要的操作。如果没有指定处理动作，则把匹配的行显示到标准输出(屏幕)，如果没有指定模式，则所有被操作所指定的行都被处理。awk分别代表其作者姓氏的第一个字母。因为它的作者是三个人，分别是Alfred Aho、Brian Kernighan、Peter Weinberger。gawk是awk的GNU版本，它提供了Bell实验室和GNU的一些扩展。下面介绍的awk是以GUN的gawk为例的，在linux系统中已把awk链接到gawk，所以下面全部以awk进行介绍。以上文字摘自[Awk学习笔记](http://man.lupaworld.com/content/manage/ringkee/awk.htm)。awk语法比上述命令复杂的多，所以学习的话可以参考上面的学习笔记，这里只举例说明下awk在文本分析上的用途。

## 常用参数说明
* -F 指定字段分隔符，awk的字段从1开始，0表示整行。
* -f 指定从文件读入awk代码，不是直接写在命令后面。
* -v VAR=VAL 从外部向awk脚本传递参数

## 分析http server的处理速度
假设我们的access.log每一行的字段使用-t分隔，第13个字段是每个请求的耗时,第七个字段是请求类型GET/POST。下面的脚本就可以统计GET请求的最大耗时，最小耗时,平均耗时，请求总数。

	awk -F'\t' 'BEGIN{max=0;min=1000000000;}$7 ~/GET/{if($13>max)max=$13;if($13<min)min=$13;sum+=$13;}END{print max,min,sum/NR,NR}' access.log


#sed
sed是一种在线编辑器，它一次处理一行内容。处理时，把当前处理的行存储在临时缓冲区中，称为“模式空间”（pattern space），接着用sed命令处理缓冲区中的内容，处理完成后，把缓冲区的内容送往屏幕。接着处理下一行，这样不断重复，直到文件末尾。文件内容并没有改变，除非你使用重定向存储输出。Sed主要用来自动编辑一个或多个文件；简化对文件的反复操作；编写转换程序等。以下介绍的是Gnu版本的Sed 3.02。以上文字摘自[sed学习笔记](http://www.tsnc.edu.cn/tsnc_wgrj/doc/sed.htm)。sed语法也比较复杂，学习的话可以参考上面的sed学习笔记。

## 举例

	sed 's/ubuntu/linux/g' 

在整行范围内把ubuntu替换为linux。如果没有g标记，则只有每行第一个匹配的字符串会被替换。

#需要注意的地方
由于sort命令是基于当前字符集的，而不同字符集的字符大小排序和比较方式，所以经常会出现，sort后的join结果不正确的问题。举例:

## 1.txt
	1002547 14
	10025472 14
	1002549 15
	10025492 15
## 2.txt
	10025471 01
	1002547 14
	10025473 01
	10025476 01
	1002549 135
	10025492 115
	10025498 135
## join with default LANG

	>env|grep LANG
	LANG=en_US.UTF-8
	>sort 1.txt > 1.sort.txt
	>sort 2.txt > 2.sort.txt
	>join 1.sort.txt 2.sort.txt
	join: file 2 is not in sorted order
	1002549 15 135
	10025492 15 115

## join with LC_ALL=C

	>export LC_ALL=C
	>sort 1.txt > 1.sort.txt
	>sort 2.txt > 2.sort.txt
	>join 1.sort.txt 2.sort.txt
	1002547 14 14
	1002549 15 135
	10025492 15 115
