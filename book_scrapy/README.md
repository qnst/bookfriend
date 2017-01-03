##  概览

> 此项目用于从[豆瓣图书](https://book.douban.com/)爬取相关图书信息，存放到数据库中，供其它程序的使用。

## 配置环境

```
# 新建虚拟环境
mkvirtualenv scrapy
# 安装依赖包
pip install -r requirements.txt
```

## 启动爬虫

```
workon scrapy
scrapy crawl book >> /var/log/scrapy_book.log 2>&1 &
```

## 配置爬虫的定时自动运行

1. 执行 `crontab -e` 
2. 加入下面一行
    ```
    */10 * * * *  sh /var/housebang/cron/cron_scrapy.sh
    ```

## 遇到的问题

### 豆瓣的防屏蔽，如何绕过？ 

#### 一般方式

1. 动态设置user agent
2. 禁用cookies
3. 设置延迟下载
4. 使用IP地址池（Tor project、VPN和代理IP）

[参考链接](http://www.cnblogs.com/rwxwsblog/p/4575894.html)

#### 使用crawlera

[crawlera](http://scrapinghub.com/crawlera)是一个利用代理IP地址池来做分布式下载的第三方平台，除了scrapy可以用以外，普通的java、php、python等都可以通过curl的方式来调用。
[参考链接](http://www.cnblogs.com/rwxwsblog/p/4582127.html)

### 编码问题

str和Unicode不能混用，要么将Unicode类型encode为其他编码。要么将str类型decode为其他编码
python的内部使用Unicode，str如“电影： ”是字节串，由Unicode经过编码(encode)后的字节组成的
下句等价于 print "电影: " + title.encode("utf-8") + " 链接: " + link.encode("utf=8")
print "top".decode("utf-8") + rank + ".".decode("utf-8") + title + " 评分".decode("utf-8") + star + '('.decode("utf-8") + rate + ')'.decode("utf-8") + "\n链接：".decode("utf-8") + link +  "\n豆瓣评论：".decode("utf-8") + quote + "\n"

####  其他方式：
* 使用Google cache

