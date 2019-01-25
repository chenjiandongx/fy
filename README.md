# 🌐 fy [![PyPI version](https://badge.fury.io/py/fy.svg)](https://badge.fury.io/py/fy) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> Translate words via command line. Inspired by [afc163/fanyi](https://github.com/afc163/fanyi)，but more features.

### ✨ 特性

* 单词字典查询
* 中英句子互译
* 发音（暂时只在 Windows 下，Linux/MacOS 暂时未找到合适的第三方库）
* Prompt shell，支持单词补全

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

**查询单词**

![](https://user-images.githubusercontent.com/19553554/51759080-60407900-2102-11e9-8d8b-3de94c8a9c8a.png)

**翻译句子**

![](https://user-images.githubusercontent.com/19553554/51759141-849c5580-2102-11e9-9097-08f85bcb873f.png)

**中文翻译**

![](https://user-images.githubusercontent.com/19553554/51759144-8534ec00-2102-11e9-9cf7-349ad5f4954b.png)

**prompt shell**

![](https://user-images.githubusercontent.com/19553554/51759432-2d4ab500-2103-11e9-948d-45320fd90504.gif)


### 📃 LICENSE

MIT [©chenjiandongx](https://github.com/chenjiandongx)
