# ImgLite-Django [![ImgLite](https://img.shields.io/badge/ImgLite-%40lWaterLite-blue)](http://imglite.lwaterlite.cc) [![Python](https://img.shields.io/badge/Python-%5Ev3.7-green)](https://www.python.org) ![Django](https://img.shields.io/badge/Django-v4.1.7-green) ![MySQL](https://img.shields.io/badge/MySQL-%5Ev8.0-green)

ImgLite-Dango is the backend application of ImgLite image hosting application.

---

## Translation
* [English](readme.md)
* [简体中文](readme-cn.md)

---

## Usage

### Requirements

* Python 3.7 and up
* MySQL 8.0 and up or other DBMS
* Linux or Windows

### Installation

Virtualenv is recommended. To use it, you need open console in the project folder and type:
```commandline
$ pip install virtualenv
```
This will install the virtualenv. After installation complete, type:
```commandline
$ virtualenv venv
```
This will establish the virtual environment, create a folder named 'venv'. Change it as your like. 

Now you need activate the virtual environment, type:
```commandline
$ .\venv\Scripts\activate # for Windows
$ source /venv/Scripts/activate # for Linux
```
Now you should see '(venv)' in the front of your command line. This means you successfully enter the virtual environment.

Now type:
```commandline
$ pip install -r requirement.txt
```
Now all dependencies should be auto installed.

To run a developing server, type:
```commandline
$ python manage.py runserver
```
Now the developing server should be run successfully. But this is not over yet.

Now you need to bind the Django application with your database, mine is MySQL, so here we use it for example.
First you need to log in to your mysql service.Type:
```commandline
$ mysql -uroot -proot
```
Replace your account and password here. Now in mysql terminal, type:
```mysql
CREATE DATABASE imglite;
```
A new database named imglite should be created now. Then type:
```mysql
USE imglite;
source imglite.sql;
```
Use the absolute path in your instance. After create all tables, exit to commandline and type:
```commandline
$ python manage.py makemigrations
$ python manage.py migrate
```
Now the Django app should be linked with MySQL database. I disable django auto management for database, 
if you want to enable it, find the app models' Meta class, change the 'managed' into True.

### Production
The steps given above is to start a developing server for test, **NEVER** use it in production environment.

For production, use python package uwsgi to start a web server.

To install it, type:
```commandline
$ pip install uwsgi
```
Now you need to start a web server, you can use commandline form or ini form. Check more in <https://uwsgi-docs.readthedocs.io/en/latest/>

---

## Structure

* _ImgLite_Django_

  This folder is the main project setup folder, settings and urls could be found inside.

* _authentication_
* _image_
* _statement_

  These three parts are Django applications
* _cache_ This folder is for temporary storage the middle file, such as csv, excel, ect.
* _utils_ This folder contains of some useful utilities.
  * **_Config.py_** This python script contains the project configurations. Database info, whitelist of hoster, ect are inside.
  * CacheCleaner.py This python script is for temporary file cleaning. ONLY run as script when developing, NEVER do such in production.
    For production, use system timing task solution like registering a system service.
  * **_RSA_** Place your RSA key in this folder for RSA encryption, name it as private.pem and public.pem
* _manage.py_ The default Django admin script.
* _imglite.sql_ sql for create the database.
* _requirement.txt_ Python package requirement.