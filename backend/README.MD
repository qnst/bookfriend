## 安装依赖包
```
mkvirtualenv bookfriend
pip install -r requirements.txt
```

## 同步数据库

在项目中添加了新的model,执行如下命令,在数据库中即可生成对应的表
```
python manage.py makemigrations [appname]
python manage.py migrate
```

## 运行方式
```
python manage.py runserver 0.0.0.0:9100
# 后台运行方式: nohup python manage.py runserver 0.0.0.0:9100 &
```

## demo 地址

用户名：admin 密码：password
* 后台管理系统 http://121.42.58.246:9100/admin   
* api管理页面: http://121.42.58.246:9100/api/books/  