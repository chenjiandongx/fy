# 有道词典命令行版 [![PyPI version](https://badge.fury.io/py/youdao-wd.svg)](https://badge.fury.io/py/youdao-wd) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> Python3 编写的有道词典命令行版本，支持单词或句子中英互译

**NOTE:** Windows 下代码页为 gbk 的不能显示音标，所以看音标要 chcp 65001 切换为 utf-8

### 安装

pip 安装
```
$ pip install youdao-wd
```

源码安装
```
$ git clone https://github.com/chenjiandongx/youdao-wd.git
$ cd youdao-wd
$ pip install -r requirements.txt
$ python setup.py install
```

### 使用
```
>>> wd -h

usage: wd [-h] [-v] [QUERY [QUERY ...]]

Query words meanings via the command line

positional arguments:
  QUERY          the words to meanings

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  displays the current version of youdao
```

### 查询单词
```
>>> wd python

>>  python : python

    n. 巨蟒；大蟒
    n. （法）皮东（人名）

    python['蟒蛇', 'Python', '蟒属']
    Burmese Python['缅甸蟒', '缅甸蟒', '黄金蟒']
    Python regius['球蟒', '球蟒']
```

### 查询句子
```
>>> wd life is short,you need python

>>  life is short,you need python: 生命是短暂的,你需要python
```

### 中文翻译
```
>>> wd php是世界上最好的语言

>>  php是世界上最好的语言: PHP is one of the best language in the world
```

### LICENSE

MIT [@chenjiandongx](https://github.com/chenjiandongx)
