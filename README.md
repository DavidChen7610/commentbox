# Commentbox

一个抓取网易云音乐精彩评论的爬虫

爬虫实现可见[Python之美](https://zhuanlan.zhihu.com/p/22456856)。请访问[云音乐评论](http://music.python-cn.org/)看真实效果。

预览，Web端：

![](https://cloud.githubusercontent.com/assets/841395/18956907/baa10988-868f-11e6-868f-36702546ddec.png)

移动端效果：

![](https://cloud.githubusercontent.com/assets/841395/18956895/b2e7a1fc-868f-11e6-8283-f7740632f03b.jpg)

### 使用技术

1. 后端： Flask + Mongoengine + Mako + requests + Redis + lxml + concurrent.futures

2. 前端：React + Mobx + Fetch + Material-UI + ES6 + Webpack + Babel

### Getting Started

#### 虚拟环境和安装应用依赖

```
❯ git clone https://github.com/dongweiming/commentbox
❯ cd commentbox
❯ virtualenv venv
❯ source venv/bin/activate
❯ pip install -r requirements.txt
❯ cp local_settings.py.tmpl local_settings.py  # 然后修改其中的配置(如Redis，MongoDB)
```

#### 爬虫篇

1. 抓取之前可以添加一些代理地址到local_settings.py中，否则会影响爬取速度。
2. 修改run.py中max_workers的数量，建议选择服务器CPU核数作为这个值。 然后启动`python run.py`就开始抓取了。

#### 前端开发篇

先安装：

```
❯ cd assets
❯ npm install  # 推荐使用cnpm, 要不然有点慢
```

开发：

开发时可以先修改server.js里面的主机和端口号，然后启动

```
❯ make dev
```

目前默认后端使用8100端口，开发模式使用3000端口。

部署：

```
 ❯ make build
```

执行完毕就会在生成新的static/js/dist/index.bundle.js*文件了。

Enjoy it!

===================================

#### 修改：

```
1、爬虫项目修改为python3.5运行
2、增加一个run_demo.py的爬虫demo，功能是获取精彩评论
3、修改encrypt.py里的解密部分
4、修改run.py为单线程，方便调试
5、删除views包下__init__.py里内容
6、修改spider包下utils.py里post的headers部分
```
