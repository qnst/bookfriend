# bookfriend(书友)

> 用framework7实现的一个web-app，帮助用户方便的借到想看的书，以书会友。

## 需求分析

帮助用户方便的借到想看的书,只要有可以借出的书,每个人就是一个私人图书馆.

* 用户人群是哪些?
* app吸引人的功能点在哪里?
* 如何鼓励用户上传以及借出自己的书
* 如何在微信中传播?

![图书馆](https://raw.githubusercontent.com/sniperyen/bookfriend/master/analysis/%E5%9B%BE%E4%B9%A6%E9%A6%86.jpg)

### 第一期

* 用户的注册和登陆(微信联合登陆)
* 图书的上传与展示
* 搜索周边的用户于图书
* 添加好友
* 私信

### 后期

* 读书打卡功能,并可以分享到朋友圈
* 线下活动
* 公共图书馆图书借阅
* 找不到的图书,导流到线上书店购买

## 涉及到相关技术

前后端分离,后端只是提供api,前端通过ajax调用,然后通过vue来双向绑定数据.

### 后端
* web框架: django + restfulapi
* 数据库: sqlite(后期迁移到mysql)

### 前端
* [framework7](http://framework7.cn/)
* [vue](http://cn.vuejs.org/)
