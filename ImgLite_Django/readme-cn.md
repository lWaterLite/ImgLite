# ImgLite-Django [![ImgLite](https://img.shields.io/badge/ImgLite-%40lWaterLite-blue)](http://imglite.lwaterlite.cc) [![Python](https://img.shields.io/badge/Python-%5Ev3.7-green)](https://www.python.org) ![Django](https://img.shields.io/badge/Django-v4.1.7-green) ![MySQL](https://img.shields.io/badge/MySQL-%5Ev8.0-green)

ImgLite-Django 是 ImgLite 的后端应用。

---

## 翻译
* [English](readme.md)
* [简体中文](readme-cn.md)

---

## 使用

### 必要条件

* Python 3.7 and up
* MySQL 8.0 and up 或者其他的数据库管理系统
* Linux or Windows

### 安装

推荐使用虚拟环境，要启用它，首先在项目文件夹打开命令行输入：
```commandline
$ pip install virtualenv
```
这会开始安装virtualenv包。安装完成后输入：
```commandline
$ virtualenv venv
```
这会创建一个虚拟环境，创建一个名为venv的文件夹，你可以根据自己的喜好改变它的名字。

现在你需要启用虚拟环境，输入：
```commandline
$ .\venv\Scripts\activate # for Windows
$ source /venv/Scripts/activate # for Linux
```
现在你应该在命令行前看到’(venv)‘的字样，这代表你的虚拟环境成功启动了。

现在输入:
```commandline
$ pip install -r requirement.txt
```
所有的需求应该会被自动安装。

要启动一个测试用服务器，输入：
```commandline
$ python manage.py runserver
```
现在测试服务器应该成功启动了，但是还没结束！

现在你需要将Django应用和你的数据库绑定，我使用的是MySQL，这里以它为例子。
首先你需要登录你的mysql：
```commandline
$ mysql -uroot -proot
```
将账号和密码改成你自己的， 现在在mysql终端中输入：
```mysql
CREATE DATABASE imglite;
```
一个名叫imglite的数据库应该被新建完成，然后输入：
```mysql
USE imglite;
source imglite.sql;
```
使用绝对路径在你的实例中。当所有表创建完成后，退出到命令行，输入：
```commandline
$ python manage.py makemigrations
$ python manage.py migrate
```
现在Django应用应该和MySQL数据库连接了。我禁用了Django对数据库的自动管理，如果希望启用它，在对应Models中寻找Meta类，将‘managed’更改为True。

### Production
上面所有的步骤都是用来启动一个测试服务器的，**永远不要**在生产环境中使用。
如果要在生产环境中使用，你可以使用python的uwsgi库来启动一个web server。

要安装它，输入：
```commandline
$ pip install uwsgi
```
现在你需要启动一个web server， 你可以使用命令行方式或是ini配置文件方式。在 <https://uwsgi-docs.readthedocs.io/en/latest/>中查看更多。

---

## 项目结构

* _ImgLite_Django_ 这个文件夹是Django项目的根文件夹，配置脚本就在其中。

* _authentication_
* _image_
* _statement_

  这三个文件夹是Django app。
* _cache_ 这个文件夹用来存储一些应用运行时的临时文件。
* _utils_ 这个文件夹存了一些有用的工具。
  * **_Config.py_** 这个Python脚本存放了一些应用配置信息，包括数据库配置信息，域名白名单等。
  * CacheCleaner.py 这个Python脚本用来清理临时文件，仅仅在开发中以Python脚本运行，在生产环境中使用系统提供的定时任务方案启动，例如注册成系统服务。
  * **_RSA_** 将你的RSA密钥放在这，将它命名成private.pem和public.pem
* _manage.py_ 默认的Django命令行管理脚本。
* _imglite.sql_ 构建数据库的sql语句。
* _requirement.txt_ Python包依赖。