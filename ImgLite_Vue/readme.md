# ImgLite-Vue [![ImgLite](https://img.shields.io/badge/ImgLite-%40lWaterLite-blue)](http://imglite.lwaterlite.cc) [![Python](https://img.shields.io/badge/Node-v18.12.1-green)](https://www.python.org) ![Vue](https://img.shields.io/badge/Vue-v3.2.47-green) ![Vite](https://img.shields.io/badge/Vite-v4.2.1-green)

ImgLite-Vue is the frontend application of ImgLite image hosting application.

---

## Translation
* [English](readme.md)
* [简体中文](readme-cn.md)

---

## Usage

### Requirements

* Node.js v16 and up
* Windows or Linux

### Installation

```commandline
$ yarn install
$ yarn dev
```
This should start a developing server.

### Production

```commandline
$ yarn build
```
This will build the static file. Use Nginx or other web server to apply the web page.

Change your host site in src/utils/axios.js before build.
