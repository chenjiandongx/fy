<p align="center">
    <img src="https://user-images.githubusercontent.com/19553554/51784033-185f3780-217e-11e9-8a06-c0f43c5c0145.png" alt="pyecharts logo" width=200 height=200 />
</p>
<h1 align="center">🌐 fy</h1>
<p align="center">
    <em>Translate words via command line. Inspired by <a href="https://github.com/afc163/fanyi">afc163/fanyi</a>, but more features.</em>
</p>
<p align="center">
    <a href="https://travis-ci.org/chenjiandongx/fy">
        <img src="https://travis-ci.org/chenjiandongx/fy.svg?branch=master" alt="Travis Build Status">
    </a>
    <a href="https://ci.appveyor.com/project/chenjiandongx/fy">
        <img src="https://ci.appveyor.com/api/projects/status/k1q0s2a5mn8roid2?svg=true" alt="Appveyor Build Status">
    </a>
     <a href="https://codecov.io/gh/chenjiandongx/fy">
        <img src="https://codecov.io/gh/chenjiandongx/fy/branch/master/graph/badge.svg" alt="Appveyor Build Status">
    </a>
    <a href="https://badge.fury.io/py/fy">
        <img src="https://badge.fury.io/py/fy.svg" alt="PyPI - Python Version">
    </a>
    <a href="https://pypi.org/project/fy/">
        <img src="https://img.shields.io/pypi/pyversions/fy.svg?colorB=brightgreen" alt="PyPI - Python Version">
    </a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-brightgreen.svg" alt="MIT License">
    </a>
</p>

### ✨ 特性

* 单词字典查询
* 中英句子互译
* 关键词高亮
* 发音（只在 Windows 下，Linux/MacOS 暂时未找到合适的第三方库）
* Prompt shell，支持单词补全
* 支持配置文件（配置查询来源以及对应接口的 TOKEN KEY）
* records shell，记录查询历史

### 🔰 安装

**pip 安装**
```bash
$ pip install fy
```

**源码安装**
```bash
$ git clone https://github.com/chenjiandongx/fy.git
$ cd fy
$ pip install -r requirements.txt
$ python setup.py install
```

### 📝 使用

```bash
$ fy --help
usage: fy [-h] [-s] [-r] [-R] [-v] [WORDS [WORDS ...]]

Translate words via command line

positional arguments:
  WORDS          the words to translate

optional arguments:
  -h, --help     show this help message and exit
  -s, --shell    spawn a query prompt shell.
  -r, --records  spawn a records prompt shell.
  -R, --reset    reset fy configuration.
  -v, --version  displays the current version of fy.
```

**查单词**

![](https://user-images.githubusercontent.com/19553554/64939403-75396a80-d893-11e9-9772-021f165d6647.png)

**英译中**

![](https://user-images.githubusercontent.com/19553554/64939404-75d20100-d893-11e9-97a3-c574dc75df2a.png)

**中译英**

![](https://user-images.githubusercontent.com/19553554/64939405-75d20100-d893-11e9-88d7-48b59cd107f7.png)

**query prompt shell**

![](https://user-images.githubusercontent.com/19553554/64939406-766a9780-d893-11e9-81a0-d0d5b9c4897d.png)

**records prompt shell**
> 使用 SQLite 数据库，表名称为 `words`

![](https://user-images.githubusercontent.com/19553554/64939407-77032e00-d893-11e9-97e0-3f70328148b9.png)


### 🔧 配置

配置文件内容为

$ car ~/.fy.json
```json
{
    "query_source": "google,youdao,iciba",
    "youdao_key": "1945325576",
    "youdao_key_from": "Youdao-dict-v21",
    "iciba_key": "4B26F43688FA072E0B94F68FFCE224CF",
    "enable_sound": true
}
```

**查询源**

目前支持 google、youdao、iciba，如果只想使用 youdao 源，可修改为 `query_source: "youdao"`，google/iciba 同理

**TOKEN KEY**

> 目前使用的 TOKEN KEY 都是我自己申请的，youdao 有限制，iciba 没有，开发者可以自行申请替换。

* `youdao_key` 和 `youdao_key_form` 是 youdao 接口需要的 token，申请地址为 http://open.iciba.com/index.php?c=api
* `iciba_key` 是 iciba 需要的 token，申请地址为 http://open.iciba.com/index.php?c=api

### 📅 Changelog

#### V1.6.0 - 2019-09-16
* Update: 新增 `pangu` 分词

#### V1.5.2 - 2019-08-28
* Add: 新增 `-R` 参数，重置配置信息

#### V1.5.1 - 2019-08-19
* Update: 输出格式调整

#### V1.5.0 - 2019-08-19
* Add: 新增 google 翻译源

#### V1.4.1 - 2019-01-28
* Add: 新增关闭声音配置项

#### V1.4.0 - 2019-01-28
* Update: 使用 sqlite prompt shell

#### V1.3.0 - 2019-01-27
* Add: 支持保存历史查询记录

#### V1.2.1 - 2019-01-26
* Update: 声明支持的 Python 版本

#### V1.2.0 - 2019-01-26
* Add: 提供配置文件

#### V1.1.0 - 2019-01-25
* Add: 新增发音功能

#### V1.0.0 - 2019-01-24
* Alpha: 第一个正式版发布

### 📃 LICENSE

MIT [©chenjiandongx](https://github.com/chenjiandongx)
