title: Android上的单元测试
slug: android-unit-tests
category: android
tags: unit-test,android
date: 2013-02-25

[TOC]

#工作流程
## Android Application Tests
1. Application
2. Test Project
## Android Library Project
1. Application for the lib-project
2. Test project for the application

# 命令行
## 创建Application Project

## 创建Library Project

## 创建Test Project


## 编译运行测试
		
		adb shell pm list instrumentation
		adb shell am instrument -w <test_package_name>/<runner_class>

# 混淆相关
(参看)[http://www.deepbluelambda.org/programming/clojure/creating-android-applications-with-clojure--slimming-things-down-with-proguard]
