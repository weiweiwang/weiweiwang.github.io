---
title: 用jekyll和github写blog
category: misc
tags: [jekyll,github,blog,博客]
---

# 本地环境

参看：[Jekyll中文文档](http://jekyllcn.com/)

{% highlight bash %}
 $ gem install jekyll bundler
 $ jekyll new my-awesome-site
 $ cd my-awesome-site
~/my-awesome-site $ bundle install
~/my-awesome-site $ bundle exec jekyll serve
# => 打开浏览器 http://localhost:4000
{% endhighlight %}

# 写blog
根据第一步生成的项目中的样例可以开始写blog了，注意index.md, about.md以及_posts文件夹中xxx.md文件中的layout属性的差别

# github代码库

在github中创建一个以{username}.github.io为名称的代码库
然后再my_awesome-site中执行

{% highlight bash %}
  cd my-awesome-site
  git init
  git remote add origin https://github.com/{username}/{username}.github.io
  git fetch
  git add xxx
  git commit -m "first commit"
  git push origin master
{% endhighlight %}

# 遇到问题如何解决
  参考别人的blog代码库，比如本blog代码库地址在[这里](https://github.com/weiweiwang/weiweiwang.github.io)

# 参考
[jekyllcn](http://jekyllcn.com/)