#!/usr/bin/env python
# coding=utf-8

import argparse

import huepy
import requests

__version__ = "1.0.0"

HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
}

# 有道 KEY
YOUDAO_KEY = "1945325576"
YOUDAO_KEY_FROM = "Youdao-dict-v21"

ERR_MSG = "Sorry, something wrong, may be you should check your network or just try again later"


def get_parser():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(description="Translate words via command line")
    parser.add_argument(
        "words", metavar="WORDS", type=str, nargs="*", help="the words to translate"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="displays the current version of fy",
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

    if not args["words"]:
        parser.print_help()
        return

    words = " ".join(args["words"])
    youdao_api(words)


def youdao_api(words):
    print()
    url = (
        "http://fanyi.youdao.com/openapi.do?keyfrom={}&key={}&"
        "type=data&doctype=json&version=1.1&q={}"
    )
    try:
        resp = requests.get(
            url.format(YOUDAO_KEY_FROM, YOUDAO_KEY, words), headers=HEADERS
        ).json()

        phonetic = ""
        basic = resp.get("basic", None)
        if basic and resp.get("basic").get("phonetic"):
            phonetic += huepy.purple("  [ " + basic.get("phonetic") + " ]")

        print(" " + words + phonetic + huepy.grey("  ~  fanyi.youdao.com"))
        print()

        if basic and basic.get("explains", None):
            for item in basic.get("explains"):
                print(huepy.grey(" - ") + huepy.green(item))
        print()

        web = resp.get("web", None)
        if web and len(web):
            for i, item in enumerate(web):
                print(huepy.grey(" " + str(i + 1) + ". " + item.get("key")))
                print("   " + huepy.cyan(", ".join(item.get("value"))))

    except Exception:
        print(" " + huepy.red(ERR_MSG))


if __name__ == "__main__":
    command_line_runner()
