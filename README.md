# spichi
> SpicyChicken

轻量级web应用框架。专注于提供后端API服务（不做模板渲染）。
通过WSGI接口对外提供服务。

## 搭建环境以及安装

支持linux以及mac系统。

依赖于`MySQL`以及`redis`, 所以需要安装他们。
安装好后，clone 代码，并安装第三方包依赖。
```shell
git clone https://github.com/ifkite/spichi.git
cd spichi
pip install -r requirements.txt
```

## 运行

有两种运行方式
1. gunicorn
```shell
gunicorn -w4 your_app:app
```
your_app.py 创建app, 并定义若干视图函数

2. python your_app.py
your_app.py 内容类似于：
```python
from wsgiref.simple_server import make_server
from autoreload import autoreload
from spichi import create_app
app = create_app()
# define some views
def run():
    httpd = make_server(host='', port=8848, app=app)
    httpd.serve_forever()
if __name__ == '__main__':
    autoreload(run)
```

## 功能介绍

目前包含以下内容：
* HTTP API 框架
* session会话存储
* 缓存(string类型的结果)
* 支持MySQL SQLite数据库
* 热加载

## 配置

默认配置文件是 spichi/develop.json

```json
{
   "DATABASES": {   #设置数据库
   "mysql": {       #数据库配置名
                    #访问数据库相关的代码中，指定的数据库名需要与此配置一致
                    #举例：app.databases['mysql']
       "db_type": "sql", #MySQL SQLite 都填 'sql'，此时底层数据库连接使用SQLAlchemy
       "db_conf": "mysql+mysqldb://root:@localhost/spichi_test"     #填连接方式，也可参考SQLAlchemy文档
                    # 大同小异
                    # MySQL: mysql+mysqldb://user:password@host:port/dbname[?key=value&key=value...]
                    # SQLite: sqlite+pysqlite:///file_path
       }
    },
   "UPLOAD_CLASS": "local",    #上传文件处理方式，只支持local，即存在本地
   "SESSION_STORE": "redis",   #session存储方式，只支持redis，即存在redis中
   "CACHE": {                  #缓存存储方式，只支持redis，即存在redis中
        "redis": {             #使用cache前需要指明使用的哪种存储方式
            "host": "127.0.0.1",    #redis的host
            "port": 6379,           #redis的端口
            "db": 0                 #redis的db
        }
    }
}
```

## Licensing

ifkite/spichi is licensed under the MIT License
