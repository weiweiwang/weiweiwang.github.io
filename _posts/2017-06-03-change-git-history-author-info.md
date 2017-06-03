---
title: 修改git历史中的作者信息
category: git
tags: [git,author,history]
author: weiwei
---

* TOC
{:toc}


# 参考github文档
[Changing author info](https://help.github.com/articles/changing-author-info/)

# 操作步骤

## 代码
拷贝下属代码，并修改`OLD_EMAIL`,`CORRECT_NAME `,`CORRECT_EMAIL `三个属性为你自己需要的值，假设脚本存储名称为`fix_author_info.sh`

```
#!/bin/sh

git filter-branch --env-filter '
OLD_EMAIL="your-old-email@example.com"
CORRECT_NAME="Your Correct Name"
CORRECT_EMAIL="your-correct-email@example.com"
if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags
```

## checkout临时代码
将你的代码库checkout到一个临时目录，拷贝上述代码到这个目录下，然后执行脚本

```
bash -x fix_author_info.sh
```

## 推送
用`git log` review提交历史，确认没有问题后使用下面命令强制推送

```
git push --force --tags origin 'refs/heads/*'
```

## 备份原代码目录，重新clone远程代码库
这一步git pull会失败，google下有个命令是`git pull origin master --allow-unrelated-histories`，试了下history中还是存在author信息不正确的，所以还是建议先备份，重新clone