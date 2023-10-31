import asyncio
import math
import os
import shutil
import socket
import sys
from os import remove

import dotenv
import heroku3
import psutil
import requests
import urllib3
from pyrogram import Client, filters
from pyrogram.types import Message

from Bdrl.config import *
from Bdrl.config import BOTLOG_CHATID
from Bdrl.helpers.basic import edit_or_reply
from Bdrl.helpers.misc import HAPP
from Bdrl.utils import *


def humanbytes(size):
    if not size:
        return "0 B"
    for unit in ["", "K", "M", "G", "T"]:
        if size < 1024:
            break
        size /= 1024
    if isinstance(size, int):
        size = f"{size}{unit}B"
    elif isinstance(size, float):
        size = f"{size:.2f}{unit}B"
    return size


@Client.on_message(filters.command("restart", prefix) & filters.me)
async def restart_bot(_, message: Message):
    k = await edit_or_reply(message, "`Restarting your userbot...`")
    await asyncio.sleep(2)
    await k.edit("`• Restarted successfully.`")
    restart()


@Client.on_message(filters.command("shutdown", prefix) & filters.me)
async def shutdown_bot(client: Client, message: Message):
    if BOTLOG_CHATID:
        await client.send_message(
            BOTLOG_CHATID,
            "**#SHUTDOWN** \n"
            "**Bdrl** is off!\nIf you want bot alive, turn on manual on heroku",
        )
    await edit_or_reply(message, "**[Bdrl] Shutting down.**")
    if HAPP is not None:
        HAPP.process_formation()["worker"].scale(0)
    else:
        sys.exit(0)


@Client.on_message(filters.command("logs", prefix) & filters.me)
async def logs_ubot(client: Client, message: Message):
    if HAPP is None:
        return await edit_or_reply(
            message,
            "Make sure `HEROKU_API_KEY` and `HEROKU_APP_NAME` is configured correctly in heroku.",
        )
    ok = await edit_or_reply(message, "`Getting your heroku logs...`")
    with open("Logs-Heroku.txt", "w") as log:
        log.write(HAPP.get_log())
    await client.send_document(
        message.chat.id,
        "Logs-Heroku.txt",
        caption="Bdrl heroku logs",
    )
    await ok.delete()
    remove("Logs-Heroku.txt")


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


async def is_heroku():
    return "heroku" in socket.getfqdn()


@Client.on_message(filters.command("setvar", prefix) & filters.me)
async def set_var(client: Client, message: Message):
    if len(message.command) < 3:
        return await edit_or_reply(
            message, f"<b>Usage:</b> {prefix}setvar [Var Name] [Var Value]"
        )
    ok = await edit_or_reply(message, "`Processing...`")
    to_set = message.text.split(None, 2)[1].strip()
    value = message.text.split(None, 2)[2].strip()
    if await is_heroku():
        if HAPP is None:
            return await ok.edit(
                "Make sure your HEROKU_API_KEY and HEROKU_APP_NAME are properly configured in heroku config vars"
            )
        heroku_config = HAPP.config()
        if to_set in heroku_config:
            await ok.edit(f"Successfully Changed var {to_set} to {value}")
        else:
            await ok.edit(f"Successfully Added var {to_set} to {value}")
        heroku_config[to_set] = value
    else:
        path = dotenv.find_dotenv(".env")
        if not path:
            return await ok.edit(".env file not found.")
        dotenv.set_key(path, to_set, value)
        if dotenv.get_key(path, to_set):
            await ok.edit(f"Successfully Changed var {to_set} to {value}")
        else:
            await ok.edit(f"Successfully Added var {to_set} to {value}")
        os.system(f"kill -9 {os.getpid()} && bash run")


@Client.on_message(filters.command("getvar", prefix) & filters.me)
async def varget_(client: Client, message: Message):
    if len(message.command) != 2:
        return await edit_or_reply(message, f"<b>Usage:</b> {prefix}getvar [Var Name]")
    ok = await edit_or_reply(message, "`Processing...`")
    check_var = message.text.split(None, 2)[1]
    if await is_heroku():
        if HAPP is None:
            return await ok.edit(
                "Make sure your HEROKU_API_KEY and HEROKU_APP_NAME are properly configured in heroku config vars"
            )
        heroku_config = HAPP.config()
        if check_var in heroku_config:
            return await ok.edit(
                f"<b>{check_var}:</b> <code>{heroku_config[check_var]}</code>"
            )
        else:
            return await ok.edit(f"Cannot find var {check_var}")
    else:
        path = dotenv.find_dotenv(".env")
        if not path:
            return await ok.edit(".env file not found.")
        output = dotenv.get_key(path, check_var)
        if not output:
            await ok.edit(f"Cannot find var {check_var}")
        else:
            return await ok.edit(f"<b>{check_var}:</b> <code>{str(output)}</code>")


@Client.on_message(filters.command("delvar", prefix) & filters.me)
async def vardel_(client: Client, message: Message):
    if len(message.command) != 2:
        return await message.edit(f"<b>Usage:</b> {prefix}delvar [Var Name]")
    ok = await edit_or_reply(message, "`Processing...`")
    check_var = message.text.split(None, 2)[1]
    if await is_heroku():
        if HAPP is None:
            return await ok.edit(
                "Make sure your HEROKU_API_KEY and HEROKU_APP_NAME are properly configured in heroku config vars"
            )
        heroku_config = HAPP.config()
        if check_var in heroku_config:
            await ok.edit(f"Successfully Removed var {check_var}")
            del heroku_config[check_var]
        else:
            return await ok.edit(f"Cannot find var {check_var}")
    else:
        path = dotenv.find_dotenv(".env")
        if not path:
            return await ok.edit(".env file not found.")
        output = dotenv.unset_key(path, check_var)
        if not output[0]:
            return await ok.edit(f"Cannot find var {check_var}")
        else:
            await ok.edit(f"Successfully Removed var {check_var}")
            os.system(f"kill -9 {os.getpid()} && bash run")


@Client.on_message(filters.command("usage", prefix) & filters.me)
async def usage_heroku(client: Client, message: Message):
    ### Credits CatUserbot
    total, used, free = shutil.disk_usage(".")
    cpuUsage = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    upload = humanbytes(psutil.net_io_counters().bytes_sent)
    down = humanbytes(psutil.net_io_counters().bytes_recv)
    TOTAL = humanbytes(total)
    USED = humanbytes(used)
    FREE = humanbytes(free)
    if await is_heroku():
        if HAPP is None:
            return await message.edit(
                "Make sure your HEROKU_API_KEY and HEROKU_APP_NAME are properly configured in heroku config vars"
            )
    else:
        return await edit_or_reply(
            message,
            f"<b>Total Disk Space:</b> <code>{TOTAL}</code>"
            f"\n<b>Used:</b> <code>{USED}</code>"
            f"\n<b>Free:</b> <code>{FREE}</code>"
            "\n\n🚀 <b>Data Usage</b> 🚀"
            f"\n<b>Upload:</b> <code>{upload}</code>"
            f"\n<b>Down:</b> <code>{down}</code>"
            f"\n\n<b>CPU:</b> <code>{cpuUsage}%</code>"
            f"\n<b>RAM:</b> <code>{memory}%</code>"
            f"\n<b>DISK:</b> <code>{disk}%</code>",
        )
    dyno = await edit_or_reply(message, "`Checking Heroku Usage. Please Wait...`")
    Heroku = heroku3.from_key(HEROKU_API_KEY)
    account_id = Heroku.account().id
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + account_id + "/actions/get-quota"
    r = requests.get("https://api.heroku.com" + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit("Unable to fetch.")
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    day = math.floor(hours / 24)
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    await asyncio.sleep(1.5)
    text = f"""
<b>Total Disk Space:</b> <code>{TOTAL}</code>
<b>Used:</b> <code>{USED}</code>
<b>Free:</b> <code>{FREE}</code>

🚀 <b>Data Usage</b> 🚀
<b>Upload:</b> <code>{upload}</code>
<b>Down:</b> <code>{down}</code>

<b>CPU:</b> <code>{cpuUsage}%</code>
<b>RAM:</b> <code>{memory}%</code>
<b>DISK:</b> <code>{disk}%</code>

• <b>Dyno usage for</b> <code>{HEROKU_APP_NAME}</code>:
 <code>{AppHours}</code>h - <code>{AppMinutes}</code>m [<code>{AppPercentage}%</code>]
• <b>Remaining dyno this month's</b>:
 <code>{hours}</code>h - <code>{minutes}</code>m [<code>{percentage}%</code>]

Estimate your bot dead is <code>{day}</code> day"""
    return await dyno.edit(text)
