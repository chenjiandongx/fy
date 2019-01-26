# 🌐 fy [![PyPI version](https://badge.fury.io/py/fy.svg)](https://badge.fury.io/py/fy)  [![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)

> Translate words via command line. Inspired by [afc163/fanyi](https://github.com/afc163/fanyi)，but more features.

### ✨ 特性

* 单词字典查询
* 中英句子互译
* 发音（只在 Windows 下，Linux/MacOS 暂时未找到合适的第三方库）
* Prompt shell，支持单词补全
* 支持配置文件（配置查询来源以及对应接口的 TOKEN KEY）

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
usage: fy [-h] [-s] [-v] [WORDS [WORDS ...]]

Translate words via command line

positional arguments:
  WORDS          the words to translate

optional arguments:
  -h, --help     show this help message and exit
  -s, --shell    whether to spawn the prompt shell
  -v, --version  displays the current version of fy
```

**查单词**

![](https://user-images.githubusercontent.com/19553554/51759080-60407900-2102-11e9-8d8b-3de94c8a9c8a.png)

**英译中**

![](https://user-images.githubusercontent.com/19553554/51759141-849c5580-2102-11e9-9097-08f85bcb873f.png)

**中译英**

![](https://user-images.githubusercontent.com/19553554/51759144-8534ec00-2102-11e9-9cf7-349ad5f4954b.png)

**prompt shell**

![](https://user-images.githubusercontent.com/19553554/51759432-2d4ab500-2103-11e9-948d-45320fd90504.gif)

### 🔧 配置

配置文件内容为

$ car ~/.fy.json
```json
{
    "query_source": "youdao,iciba",
    "youdao_key": "1945325576",
    "youdao_key_from": "Youdao-dict-v21",
    "iciba_key": "4B26F43688FA072E0B94F68FFCE224CF"
}
```

**查询源**

目前支持 youdao 以及 iciba

**TOKEN KEY**
> 现在两个暂时使用的都是我自己申请的，youdao 有限制，iciba 没有，开发者可以自行申请替换。

* `youdao_key` 和 `youdao_key_form` 是 youdao 接口需要的 token，申请地址为 http://open.iciba.com/index.php?c=api
* `iciba_key` 是 iciba 需要的 token，申请地址为 http://open.iciba.com/index.php?c=api

### 📅 Changelog

#### V1.0.0 - 2018-01-24
* Alpha: 第一个正式版发布

#### V1.1.0 - 2018-01-25
* Add: 新增发音功能

#### V1.2.0 - 2018-01-26
* Add: 提供配置文件

### 📃 LICENSE

MIT [©chenjiandongx](https://github.com/chenjiandongx)
