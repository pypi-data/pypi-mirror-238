# Copyright (C) 2022 CtrlUB
#
# This file is a part of < https://github.com/kennedy-ex/CtrlUB/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/kennedy-ex/CtrlUB-Userbot/blob/main/LICENSE/>.
#


from base64 import b64decode as kk
from os import getenv

import requests
from dotenv import load_dotenv

load_dotenv(".env")

API_HASH = getenv("API_HASH")
API_ID = int(getenv("API_ID", ""))

while 0 < 6:
    _BLACKLIST_CHAT = requests.get(
        "https://raw.githubusercontent.com/Yansaii/idk/master/blgcast.json"
    )
    if _BLACKLIST_CHAT.status_code != 200:
        if 0 != 5:
            continue
        BLACKLIST_CHAT = [
            -1001473548283,
            -1001390552926,
            -1001606516367,
            -1001704645461,
        ]
        break
    BLACKLIST_CHAT = _BLACKLIST_CHAT.json()
    break

del _BLACKLIST_CHAT

BOTLOG_CHATID = int(getenv("BOTLOG_CHATID", "0"))
BLACKLIST_GCAST = {int(x) for x in getenv("BLACKLIST_GCAST", "").split()}
BRANCH = getenv("BRANCH", "main")
DB_URL = getenv("DATABASE_URL", "")
BOT_TOKEN = getenv("BOT_TOKEN", None)
TOKEN = getenv(
    "TOKEN",
    kk("Z2hwX2tuT0ZSNlpBWGd2UWRaNXUwSnhoSzAyMmJ6bkVYUDJGM0ROeQ==").decode("utf-8"),
)
HEROKU_API_KEY = getenv("HEROKU_API_KEY", None)
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", None)
STRING_SESSION = getenv("STRING_SESSION", "")
STRING_SESSION2 = getenv("STRING_SESSION2", "")
STRING_SESSION3 = getenv("STRING_SESSION3", "")
STRING_SESSION4 = getenv("STRING_SESSION4", "")
STRING_SESSION5 = getenv("STRING_SESSION5", "")
