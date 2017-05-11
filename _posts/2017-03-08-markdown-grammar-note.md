---
title: markdown语法备忘
category: misc
tags: [markdown,语法,备忘]
---
# 参考
[mastering markdown][mastering-markdown]

[writing on github][writing-on-github]

# 图片
`
Here is an inline ![smiley](smiley.png){:height="36px" width="36px"}.
`
	Here's our logo (hover to see the title text):
	
	Inline-style: 
	![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")
	
	Reference-style: 
	![alt text][logo]
	
	[logo]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"

渲染结果

Here's our logo (hover to see the title text):

Inline-style: 
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

Reference-style: 
![alt text][logo]

[logo]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"


# 代码
## Inline代码
	Inline `code` has `back-ticks around` it.

渲染结果

Inline `code` has `back-ticks around` it.

## 代码高亮
	```javascript
	var s = "JavaScript syntax highlighting";
	alert(s);
	```
	 
	```python
	s = "Python syntax highlighting"
	print s
	```
	 
	```
	No language indicated, so no syntax highlighting. 
	But let's throw in a <b>tag</b>.
	```

渲染的效果
	
```javascript
var s = "JavaScript syntax highlighting";
alert(s);
```
 
```python
s = "Python syntax highlighting"
print s
```
 
```
No language indicated, so no syntax highlighting. 
But let's throw in a <b>tag</b>.
```

# Blockquotes
	> Blockquotes are very handy in email to emulate reply text.
	> This line is part of the same quote.
	Quote break.

	> This is a very long line that will still be quoted properly when it wraps. Oh boy let's keep writing to make sure this is long enough to actually wrap for everyone. Oh, you can *put* **Markdown** into a blockquote. 

渲染的结果
	
> Blockquotes are very handy in email to emulate reply text.
> This line is part of the same quote.

Quote break.

> This is a very long line that will still be quoted properly when it wraps. Oh boy let's keep writing to make sure this is long enough to actually wrap for everyone. Oh, you can *put* **Markdown** into a blockquote. 
 
# Reference/Anchor
如果要引用某个header可以使用如下的方式

```
[跳回参考Header](#参考)
```
[跳回参考Header](#参考)


[mastering-markdown]:https://guides.github.com/features/mastering-markdown/
[writing-on-github]:https://help.github.com/categories/writing-on-github/
