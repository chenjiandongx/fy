import io
import json
import os
from contextlib import redirect_stdout

from fy import translate


def _test_output(word, word_output):
    f = io.StringIO()
    with redirect_stdout(f):
        translate(word)
    out = f.getvalue()

    print(out)

    for w in word_output:
        assert w in out


def test_hello():
    word_output = [
        "喂，咦，喂，喂。我一点也听不清.",
    ]
    _test_output("hello", word_output)


def test_sentence():
    word_output = ["什么他妈的", "什么是他妈的", "~  fanyi.youdao.com", "~  iciba.com"]
    _test_output("what the fuck", word_output)


def test_chinese_to_english():
    word_output = ["Only the strong survive", "~  fanyi.youdao.com", "~  iciba.com"]
    _test_output("只有强者才能生存", word_output)


def test_configure():
    conf_path = os.path.join(os.path.expanduser("~"), ".fy.json")
    with open(conf_path, "r", encoding="utf8") as f:
        conf = json.load(f)
        assert conf == {
            "query_source": "google,youdao,iciba",
            "youdao_key": "1945325576",
            "youdao_key_from": "Youdao-dict-v21",
            "iciba_key": "4B26F43688FA072E0B94F68FFCE224CF",
            "enable_sound": True,
        }


def test_database():
    assert os.path.exists(os.path.join(os.path.expanduser("~"), ".fy.sqlite")) is True
