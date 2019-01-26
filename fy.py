#!/usr/bin/env python
# coding=utf-8

import argparse
import json
import os
import threading
import re
import sys

import huepy
import requests
import xmltodict

__version__ = "1.2.0"

HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
}

ERR_MSG = (
    "something wrong, may be you should check your network or just try again later"
)

FY_CONF_PATH = os.path.join(os.path.expanduser("~"), ".fy.json")
HERE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "words")


def generate_config(is_force=False):
    conf = {
        # query source, split by comma
        "query_source": "youdao,iciba",
        # youdao key: http://open.iciba.com/index.php?c=api
        "youdao_key": "1945325576",
        "youdao_key_from": "Youdao-dict-v21",
        # iciba key: http://open.iciba.com/index.php?c=api
        "iciba_key": "4B26F43688FA072E0B94F68FFCE224CF",
    }

    def _write():
        with open(FY_CONF_PATH, "w+", encoding="utf8") as f:
            f.write(json.dumps(conf, indent=4))

    if is_force:
        _write()
        return

    if not os.path.exists(FY_CONF_PATH):
        _write()


def read_config():
    generate_config()

    def _read():
        with open(FY_CONF_PATH, "r", encoding="utf8") as f:
            return json.load(f)

    try:
        conf = _read()
    except:
        generate_config(True)
        conf = _read()

    return conf


CONF = read_config()
YOUDAO_KEY = CONF["youdao_key"]
YOUDAO_KEY_FROM = CONF["youdao_key_from"]
ICIBA_KEY = CONF["iciba_key"]
QUERY_SOURCE = CONF["query_source"]


def get_parser():
    parser = argparse.ArgumentParser(description="Translate words via command line")
    parser.add_argument(
        "words", metavar="WORDS", type=str, nargs="*", help="the words to translate"
    )
    parser.add_argument(
        "-s", "--shell", action="store_true", help="whether to spawn the prompt shell"
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

    if args["shell"]:
        prompt_shell()
        return

    if not args["words"]:
        parser.print_help()
        return

    words = " ".join(args["words"])
    run(words)


def translate(words):
    if "youdao" in QUERY_SOURCE:
        youdao_api(words)

    if "iciba" in QUERY_SOURCE:
        iciba_api(words)

    if ("iciba" not in QUERY_SOURCE) and ("youdao" not in QUERY_SOURCE):
        youdao_api(words)
        iciba_api(words)


def run(words):
    threads = [
        threading.Thread(target=translate, args=(words,)),
        threading.Thread(target=say, args=(words,)),
    ]

    for th in threads:
        th.start()
    for th in threads:
        th.join()


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


def prompt_shell():
    try:
        from prompt_toolkit import prompt
        from prompt_toolkit.completion import WordCompleter

        with open(os.path.join(HERE, "words.txt"), "r", encoding="utf-8") as f:
            words = [w.replace("\n", "") for w in f.readlines()]
        while True:
            run(
                prompt(
                    "Press <Ctrl+C> to exit shell.\nEnter words: ",
                    completer=WordCompleter(words),
                    complete_in_thread=True,
                )
            )
            print()
    except KeyboardInterrupt:
        print(huepy.green("GoodBye!"))


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
