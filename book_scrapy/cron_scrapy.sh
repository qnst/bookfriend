#! /bin/sh

cd /var/dev/bookfriend/book_scrapy  # 配置你自己拍冲的目录
workon scrapy
nohup scrapy crawl book >> /var/log/scrapy_book.log 2>&1 &