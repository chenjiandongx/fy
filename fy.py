import argparse
import datetime
import json
import os
import re
import sys
import threading

import huepy
import pangu
import requests
import xmltodict
from googletrans import Translator
from pony import orm

__version__ = "1.6.0"

HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
}

ERR_MSG = "Exception occurs, check your network or just try again later"


FY_CONF_PATH = os.path.join(os.path.expanduser("~"), ".fy.json")
FY_DB_PATH = os.path.join(os.path.expanduser("~"), ".fy.sqlite")
HERE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "words")

db = orm.Database()
db.bind(provider="sqlite", filename=FY_DB_PATH, create_db=True)


class Words(db.Entity):
    __table__ = "words"
    words = orm.PrimaryKey(str)
    count = orm.Required(int)
    date = orm.Required(datetime.datetime)


db.generate_mapping(create_tables=True)


@orm.db_session
def sql_update(words: str):
    query = Words.get(words=words)
    if query:
        query.count += 1
    else:
        Words(
            words=words,
            count=1,
            date=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        )
    db.commit()


def generate_config(is_force: bool = False):
    conf = {
        # query source, split by commas
        "query_source": "google,youdao,iciba",
        # youdao key: http://open.iciba.com/index.php?c=api
        "youdao_key": "1945325576",
        "youdao_key_from": "Youdao-dict-v21",
        # iciba key: http://open.iciba.com/index.php?c=api
        "iciba_key": "4B26F43688FA072E0B94F68FFCE224CF",
        "enable_sound": True,
    }

    def _write():
        with open(FY_CONF_PATH, "w+", encoding="utf8") as f:
            f.write(json.dumps(conf, indent=4))

    if is_force:
        _write()
        return

    if not os.path.exists(FY_CONF_PATH):
        _write()


def read_config() -> dict:
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


class Conf:
    def __init__(self, conf: dict):
        self.youdao_key = conf["youdao_key"]
        self.youdao_key_from = conf["youdao_key_from"]
        self.iciba_key = conf["iciba_key"]
        self.query_source = conf["query_source"]
        self.enable_sound = conf["enable_sound"]


# global configure
CONF = Conf(read_config())

# types
Parser = argparse.ArgumentParser


def get_parser() -> Parser:
    parser = argparse.ArgumentParser(description="Translate words via command line")
    parser.add_argument(
        "words", metavar="WORDS", type=str, nargs="*", help="the words to translate"
    )
    parser.add_argument(
        "-s", "--shell", action="store_true", help="spawn a query prompt shell."
    )
    parser.add_argument(
        "-r", "--records", action="store_true", help="spawn a records prompt shell."
    )
    parser.add_argument(
        "-R", "--reset", action="store_true", help="reset fy configuration."
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

    words = " ".join(args["words"])

    if args["version"]:
        print(huepy.cyan("fy " + __version__))
        return

    if args["reset"]:
        generate_config(True)
        return

    if args["shell"]:
        query_prompt_shell()
        return

    if args["records"]:
        records_prompt_shell()
        return

    if not args["words"]:
        parser.print_help()
        return

    run(words)


def translate(words: str):
    if "google" in CONF.query_source:
        google_api(words)

    if "youdao" in CONF.query_source:
        youdao_api(words)

    if "iciba" in CONF.query_source:
        iciba_api(words)

    if ("iciba" not in CONF.query_source) and ("youdao" not in CONF.query_source):
        youdao_api(words)
        iciba_api(words)


def run(words: str):
    threads = [
        threading.Thread(target=translate, args=(words,)),
        threading.Thread(target=sql_update, args=(words,)),
    ]

    if CONF.enable_sound:
        threads.append(threading.Thread(target=say, args=(words,)))

    for th in threads:
        th.start()
    for th in threads:
        th.join()


def google_api(words: str):
    print()

    def switch_language():
        for w in words:
            if "\u4e00" <= w <= "\u9fff":
                return "en"
        return "zh-cn"

    translator = Translator(service_urls=["translate.google.cn"])
    text = pangu.spacing_text(translator.translate(words, dest=switch_language()).text)
    print(" " + words + huepy.grey("  ~  translate.google.cn"))
    print()
    print(" - " + huepy.cyan(text))


def youdao_api(words: str):
    print()
    print(huepy.grey(" -------- "))
    print()
    url = (
        "http://fanyi.youdao.com/openapi.do?keyfrom={}&key={}&"
        "type=data&doctype=json&version=1.1&q={}"
    )
    try:
        resp = requests.get(
            url.format(CONF.youdao_key_from, CONF.youdao_key, words), headers=HEADERS
        ).json()

        phonetic = ""
        basic = resp.get("basic", None)
        if basic and resp.get("basic").get("phonetic"):
            phonetic += huepy.purple("  [ " + basic.get("phonetic") + " ]")

        print(" " + words + phonetic + huepy.grey("  ~  fanyi.youdao.com"))
        print()

        translation = resp.get("translation", [])
        if len(translation) > 0:
            print(" - " + pangu.spacing_text(huepy.green(translation[0])))

        if basic and basic.get("explains", None):
            for item in basic.get("explains"):
                print(huepy.grey(" - ") + pangu.spacing_text(huepy.green(item)))
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

    except:
        print(" " + huepy.red(ERR_MSG))


def iciba_api(words: str):
    print()
    print(huepy.grey(" -------- "))
    print()
    url = "http://dict-co.iciba.com/api/dictionary.php?key={key}&w={w}&type={type}"
    try:
        resp = requests.get(url.format(key=CONF.iciba_key, w=words, type="xml"))
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
        print()
    except:
        print(" " + huepy.red(ERR_MSG))


def query_prompt_shell():
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


def records_prompt_shell():
    try:
        from litecli.main import LiteCli

        litecli = LiteCli(prompt="Type quit to exit shell.\nPrompt: ")
        litecli.connect(database=FY_DB_PATH)
        litecli.run_cli()
    except:
        print(huepy.red("sorry, it can't spawn records prompt shell."))


def highlight(text: str, keyword: str):
    text = pangu.spacing_text(text)
    return re.sub(
        keyword,
        "\33[0m" + "\33[93m" + keyword + "\33[0m" + "\33[37m",
        text,
        flags=re.IGNORECASE,
    )


def say(words: str):
    if sys.platform == "win32":
        try:
            from win32com.client import Dispatch

            speak = Dispatch("SAPI.SpVoice")
            speak.Speak(words)
        except:
            pass


if __name__ == "__main__":
    command_line_runner()
