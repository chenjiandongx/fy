#!/usr/bin/env python
# coding=utf-8

import argparse
import re
import sys

import huepy
import requests
import xmltodict

__version__ = "1.0.0"

HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
}

# YOUDAO KEY
YOUDAO_KEY = "1945325576"
YOUDAO_KEY_FROM = "Youdao-dict-v21"

# iciba KEY
ICIBA_KEY = "D191EBD014295E913574E1EAF8E06666"

ERR_MSG = "Sorry, something wrong, may be you should check your network or just try again later"


def get_parser():
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
    iciba_api(words)
    say(words)


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

        translation = resp.get("translation", [])
        if len(translation) > 0:
            print(" - " + huepy.green(translation[0]))

        if basic and basic.get("explains", None):
            for item in basic.get("explains"):
                print(huepy.grey(" - ") + huepy.green(item))
        print()

        web = resp.get("web", None)
        if web and len(web):
            for i, item in enumerate(web):
                print(
                    huepy.grey(
                        " " + str(i + 1) + ". " + highlight(item.get("key"), words)
                    )
                )
                print("    " + huepy.cyan(", ".join(item.get("value"))))

    except Exception:
        print(" " + huepy.red(ERR_MSG))


def iciba_api(words):
    print()
    print(huepy.grey(" -------- "))
    print()
    url = "http://dict-co.iciba.com/api/dictionary.php?key={key}&w={w}&type={type}"
    try:
        resp = requests.get(url.format(key=ICIBA_KEY, w=words, type="xml"))
        resp.encoding = "utf8"

        dct = xmltodict.parse(resp.text).get("dict")
        ps = dct.get("ps") or ""
        print(" " + words + "  " + huepy.purple(ps) + huepy.grey("  ~  iciba.com"))
        print()

        pos = dct.get("pos")
        acceptation = dct.get("acceptation")
        if pos and acceptation:
            if not isinstance(pos, list) and not isinstance(acceptation, list):
                pos = [pos]
                acceptation = [acceptation]
            for p, a in zip([i for i in pos], [i for i in acceptation]):
                if a and p:
                    print(" - " + huepy.green(p + " " + a))
            print()

        index = 1
        sent = dct.get("sent")
        if not sent:
            return
        if not isinstance(sent, list):
            sent = [sent]
        for item in sent:
            for k, v in item.items():
                if k == "orig":
                    print(highlight(huepy.grey(" {}. ".format(index) + v), words))
                    index += 1
                elif k == "trans":
                    print(highlight(huepy.cyan("    " + v), words))

    except Exception:
        print(" " + huepy.red(ERR_MSG))


def highlight(text, keyword):
    return re.sub(
        keyword,
        "\33[0m" + "\33[93m" + keyword + "\33[0m" + "\33[37m",
        text,
        flags=re.IGNORECASE,
    )


def say(words):
    if sys.platform == "win32":
        try:
            from win32com.client import Dispatch

            speak = Dispatch("SAPI.SpVoice")
            speak.Speak(words)
        except:
            pass


if __name__ == "__main__":
    command_line_runner()
