#!/usr/bin/env python
# coding=utf-8

import argparse

import requests

__version__ = "0.1.0"

HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
}

# 有道申请的 key
KEY = "1945325576"
KEY_FROM = "Youdao-dict-v21"


def get_parser():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(
        description="Query words meanings via the command line"
    )
    parser.add_argument(
        "query",
        metavar="QUERY",
        type=str,
        nargs="*",
        help="the words to meanings",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="displays the current version of youdao",
    )
    return parser


def command_line_runner():
    """
    执行命令行操作
    """
    parser = get_parser()
    args = vars(parser.parse_args())

    if args["version"]:
        print(__version__)
        return

    if not args["query"]:
        parser.print_help()
        return

    query_words(" ".join(args["query"]))


def query_words(words):
    """
    使用有道 API 查询词典并在终端打印，输出的 result 格式
    （空格，>>，换行之类的）不要在意因为我有强迫症- -!

    :param words:
        要查询的单词或句子
    """
    url = (
        "http://fanyi.youdao.com/openapi.do?keyfrom={}&key={}&"
        "type=data&doctype=json&version=1.1&q={}"
    )

    try:
        req = requests.get(
            url.format(KEY_FROM, KEY, words), headers=HEADERS
        ).json()
        # errorCode 为 0 是正常状态
        if req["errorCode"] == 0:
            print(">>  {}: {} \n".format(words, "".join(req["translation"])))
            # 类似短语和缩写词如 API,JDK 之类的无音标属性
            try:
                us_phonetic = req["basic"]["us-phonetic"]
                uk_phonetic = req["basic"]["uk-phonetic"]
                print("    美:[{}]  英:[{}]".format(us_phonetic, uk_phonetic))
            except:
                pass
            # 查询不到内容时没有 'basic' 属性
            if "basic" in req:
                # 词典释义内容
                for _, value in enumerate(req["basic"]["explains"]):
                    print("    {}".format(value))
                print("")
                # 网络释义内容
                for _, value in enumerate(req["web"]):
                    print("    {}{}".format(value["key"], value["value"]))
        else:
            # 输入查询的内容有误，检查拼写
            print(
                ">>  Exception: The words can't be found,"
                "please check your spelling"
            )
    except Exception:
        # 网络错误，API 无法访问或者输入了奇怪的东西，如 fuck$#$#
        print(">>  Please check your spelling or network connection")


if __name__ == "__main__":
    command_line_runner()
