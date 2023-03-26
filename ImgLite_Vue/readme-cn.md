# ImgLite-Vue [![ImgLite](https://img.shields.io/badge/ImgLite-%40lWaterLite-blue)](http://imglite.lwaterlite.cc) [![Python](https://img.shields.io/badge/Node-v18.12.1-green)](https://www.python.org) ![Vue](https://img.shields.io/badge/Vue-v3.2.47-green) ![Vite](https://img.shields.io/badge/Vite-v4.2.1-green)

ImgLite-Vue 是 ImgLite的前端应用。

---

## Translation
* [English](readme.md)
* [简体中文](readme-cn.md)

---

## 使用

### 必要条件

* Node.js v16 and up
* Windows or Linux

### 安装

```commandline
$ yarn install
$ yarn dev
```
这会运行一个开发服务器

### 生产

```commandline
$ yarn build
```
这会构建静态文件，使用Nginx或其他web server来部署。

构建前在src/utils/axios.js中更改你的域名。
