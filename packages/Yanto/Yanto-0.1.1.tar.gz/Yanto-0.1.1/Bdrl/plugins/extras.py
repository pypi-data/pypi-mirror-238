# Copyright (C) 2022 CtrlUB
#
# This file is a part of < https://github.com/kennedy-ex/CtrlUB/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/kennedy-ex/CtrlUB-Userbot/blob/main/LICENSE/>.
#


import asyncio
import base64
import math
import os
import shutil
import time
import urllib

import wget
from pyrogram import Client, enums, filters
from pyrogram.errors import FloodWait, MessageNotModified, PeerIdInvalid
from pyrogram.errors.exceptions.bad_request_400 import YouBlockedUser
from pyrogram.types import Message
from requests import post
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL

from Bdrl.helpers.basic import eor
from Bdrl.helpers.tools import get_arg
from Bdrl.plugins.heroku import humanbytes
from Bdrl.utils import modules_help, prefix


async def progress(current, total, m, start, type_of_ps, file_name=None):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        if elapsed_time == 0:
            return
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            "".join("⬤" for i in range(math.floor(percentage / 10))),
            "".join("◯" for i in range(10 - math.floor(percentage / 10))),
            round(percentage, 2),
        )

        tmp = progress_str + "{0} \ {1}\nETA: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        if file_name:
            try:
                await m.edit(
                    "{}\n**File Name:** `{}`\n{}".format(type_of_ps, file_name, tmp)
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass
        else:
            try:
                await m.edit("{}\n{}".format(type_of_ps, tmp))
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass


def time_formatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " day(s), ") if days else "")
        + ((str(hours) + " hour(s), ") if hours else "")
        + ((str(minutes) + " minute(s), ") if minutes else "")
        + ((str(seconds) + " second(s), ") if seconds else "")
        + ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    )
    return tmp[:-2]


colour_code = {
    "aqua": "rgba(0, 255, 255, 100)",
    "red": "rgba(255, 0, 0, 100)",
    "blue": "rgba(0, 0, 255, 100)",
    "green": "rgba(0, 255, 0, 100)",
    "yellow": "rgba(255, 255, 0, 100)",
    "gold": "rgba(255, 215, 0, 100)",
    "orange": "rgba(255, 165, 0, 100)",
    "purple": "rgba(41, 5, 68, 100)",
    "black": "rgba(0, 0, 0, 100)",
    "white": "rgba(255, 255, 255, 100)",
    "lime": "rgba(0, 255, 0, 100)",
    "silver": "rgba(192, 192, 192, 100)",
    "maroon": "rgba(128, 0, 0, 100)",
    "olive": "rgba(128, 128, 0, 100)",
    "teal": "rgba(0, 128, 128, 100)",
    "navy": "rgba(0, 128, 128, 100)",
    "chocolate": "rgba(210, 105, 30, 100)",
}


@Client.on_message(filters.command(["song", "music"], prefix) & filters.me)
async def song(c: Client, m: Message):
    urlissed = get_arg(m)
    if not urlissed:
        return await eor(m, "`Invalid syntax, give me url or query to search...`")
    pablo = await eor(m, "`Downloading...`")
    search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    mo = mio[0]["link"]
    mio[0]["duration"]
    thum = mio[0]["title"]
    fridayz = mio[0]["id"]
    mio[0]["channel"]
    kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    sedlyf = wget.download(kekme)
    opts = {
        "format": "bestaudio",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "720",
            }
        ],
        "outtmpl": "%(id)s.mp3",
        "quiet": True,
        "logtostderr": False,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(mo, download=True)
    except Exception as e:
        await pablo.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    capy = f"**{thum}**"
    file_stark = f"{ytdl_data['id']}.mp3"
    await c.send_audio(
        m.chat.id,
        audio=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        title=str(ytdl_data["title"]),
        performer=str(ytdl_data["uploader"]),
        thumb=sedlyf,
        caption=capy,
        progress=progress,
        progress_args=(
            pablo,
            c_time,
            f"`Downloading {urlissed} ...`",
            file_stark,
        ),
    )
    await pablo.delete()
    for files in (sedlyf, file_stark):
        if files and os.path.exists(files):
            os.remove(files)


is_downloading = False


@Client.on_message(filters.command(["vsong", "video"], prefix) & filters.me)
async def vsong(c: Client, m: Message):
    urlissed = get_arg(m)

    pablo = await eor(m, "`Downloading...`")
    if not urlissed:
        return await pablo.edit("`Invalid syntax, give url or query to search...`")

    search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    mo = mio[0]["link"]
    thum = mio[0]["title"]
    fridayz = mio[0]["id"]
    mio[0]["channel"]
    kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    url = mo
    sedlyf = wget.download(kekme)
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        await pablo.edit(event, f"**Gagal Mengunduh** \n**Kesalahan :** `{str(e)}`")
        return
    c_time = time.time()
    file_stark = f"{ytdl_data['id']}.mp4"
    capy = f"**{thum}**"
    await c.send_video(
        m.chat.id,
        video=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        file_name=str(ytdl_data["title"]),
        thumb=sedlyf,
        caption=capy,
        supports_streaming=True,
        progress=progress,
        progress_args=(
            pablo,
            c_time,
            f"`Downloading {urlissed}`",
            file_stark,
        ),
    )
    await pablo.delete()
    for files in (sedlyf, file_stark):
        if files and os.path.exists(files):
            os.remove(files)


@Client.on_message(filters.command("encode", prefix) & filters.me)
async def encod(c: Client, m: Message):
    if m.reply_to_message:
        match = m.reply_to_message.text
    else:
        match = get_arg(m)
    if not match:
        k = await eor(m, "`Give me Something to Encode..`")
        await asyncio.sleep(8)
        await k.delete()
        return
    byt = match.encode("ascii")
    et = base64.b64encode(byt)
    atc = et.decode("ascii")
    await eor(m, f"**Encoded Text :** `{match}`\n\n**OUTPUT :**\n`{atc}`")


@Client.on_message(filters.command("decode", prefix) & filters.me)
async def decod(c: Client, m: Message):
    if m.reply_to_message:
        match = m.reply_to_message.text
    else:
        match = get_arg(m)
    if not match:
        k = await eor(m, "`Give me Something to Decode..`")
        await asyncio.sleep(8)
        await k.delete()
        return
    byt = match.encode("ascii")
    try:
        et = base64.b64decode(byt)
        atc = et.decode("ascii")
        await eor(m, f"**Decoded Text :** `{match}`\n\n**OUTPUT :**\n`{atc}`")
    except Exception as p:
        await eor(m, "**ERROR :** " + str(p))


@Client.on_message(filters.command(["carbon", "carb"], prefix) & filters.me)
async def carbon_handler(c: Client, m: Message):
    text = m.reply_to_message.text
    ok = get_arg(m)
    if not m.reply_to_message:
        return await m.edit(
            f"Usage:\n\n`{prefix}carbon [reply] [colour or none]`\n\n**Note:** Default colour is aqua"
        )
    await m.edit("`creating carbon . . .`")
    if ok and ok in colour_code:
        colour = ok
    else:
        colour = "aqua"
    await create_carbon(c, m, text=text, colour=colour)


@Client.on_message(filters.command("carbonlist", prefix) & filters.me)
async def carblist_handler(c: Client, m: Message):
    clist = [f"`{x}`" for x in list(colour_code.keys())]
    await m.edit("**SUPPORTED COLOURS:**\n\n" + "\n".join(clist))


async def create_carbon(c, m: Message, text, colour):
    reply = m.reply_to_message
    json = {
        "backgroundColor": f"{colour_code.get(colour)}",
        "theme": "Dracula",
        "exportSize": "4x",
    }
    json["code"] = urllib.parse.quote(text)
    json["language"] = "Auto"
    ApiUrl = "http://carbonnowsh.herokuapp.com"
    text = post(ApiUrl, json=json, stream=True)
    filename = "carbon_image.png"
    if text.status_code == 200:
        text.raw.decode_content = True
        with open(filename, "wb") as f:
            shutil.copyfileobj(text.raw, f)
            f.close()
        reply_msg_id = reply.id if reply else None
        await c.send_photo(
            m.chat.id,
            photo=filename,
            caption=f"**Carbon Made by:** {m.from_user.mention}",
            reply_to_message_id=reply_msg_id,
        )
        await m.delete()
        if os.path.exists(f"./{filename}"):
            os.remove(filename)
    else:
        await m.edit("`Image Couldn't be retreived.`")


@Client.on_message(filters.command("copy", prefix) & filters.me)
async def kkkk(c: Client, m: Message):
    rep = m.reply_to_message
    await m.delete()
    if not rep:
        return
    try:
        await rep.copy(m.chat.id)
    except:
        pass


@Client.on_message(filters.command("limit", prefix) & filters.me)
async def limit(client, message):
    yy = await message.edit_text("Processing")
    message.chat.id
    bot = "SpamBot"
    try:
        ok = await client.send_message(bot, "/start")
        await ok.delete()
    except YouBlockedUser:
        await client.unblock_user(bot)
        await yy.edit_text(f"@{bot} unblocked. Try `{prefix}limit` again.")
        return
    async for kontol in client.get_chat_history(bot, limit=1):
        if not kontol:
            await message.edit_text("Something went wrong.")
        elif kontol:
            oh = kontol.text
            await yy.edit(oh)
            await kontol.delete()


@Client.on_message(filters.command("json", prefix) & filters.me)
async def start(client, message):
    try:
        if message.reply_to_message:
            msg = message.reply_to_message
        else:
            msg = message
        msg_info = str(f"```{msg}```")
        if len(msg_info) > int("4096"):
            file = open("json.txt", "w+")
            file.write(msg_info)
            file.close()
            await client.send_document(
                message.chat.id,
                "json.txt",
                caption="Returned JSon",
            )
            os.remove("json.txt")
        else:
            await message.edit(msg_info)
    except Exception as e:
        await message.edit(f"```{e}```")


@Client.on_message(filters.command(["sg", "sa"], prefix) & filters.me)
async def sangmata(client, message):
    await message.edit_text("`Processing...`")
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        return await message.edit_text("`Pelase reply or give me a username/ID`")
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = (await client.get_users(cmd[1])).id
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        await client.get_users(get_user)
    except PeerIdInvalid:
        await message.edit_text("Can't fint histroy name.")
        return
    bot = "SangMata_BOT"
    message.chat.id
    try:
        y = await client.send_message(bot, f"/search_id {user.id}")
        await asyncio.sleep(1)
        await y.delete()
    except YouBlockedUser:
        await client.unblock_user(bot)
        y = await client.send_message(bot, f"/search_id {user.id}")
        await asyncio.sleep(1)
        await y.delete()
        return

    async for jembut in client.search_messages(bot, query="Name", limit=1):
        if not jembut:
            await message.edit_text("`Can't find histroy name of that user.`")
            return
        elif jembut:
            iss = jembut.text
            await y.delete()
            await message.edit(iss)
            await jembut.delete()

    async for jembut in client.search_messages(bot, query="Username", limit=1):
        if not jembut:
            return
        elif jembut:
            iss = jembut.text
            await y.delete()
            await message.reply(iss)
            await jembut.delete()


@Client.on_message(filters.command(["tt", "tiktok", "ig", "fb"], prefix) & filters.me)
async def sosmed(client, message):
    if message.reply_to_message:
        tetek = message.reply_to_message.text
    else:
        tetek = get_arg(message)
    if not tetek:
        return await message.edit("`Give me a link or reply to a link for download.`")
    uh = await message.edit("Processing")
    chat = message.chat.id
    pop = message.from_user.first_name
    ah = message.from_user.id
    bot = "thisvidbot"
    if tetek:
        try:
            y = await client.send_message(bot, tetek)
            await asyncio.sleep(5)
            await y.delete()
        except YouBlockedUser:
            await client.unblock_user(bot)
            y = await client.send_message(bot, tetek)
            await asyncio.sleep(5)
            await y.delete()
    async for oky in client.search_messages(
        bot, filter=enums.MessagesFilter.VIDEO, limit=1
    ):
        await client.send_video(
            chat,
            video=oky.video.file_id,
            caption=f"**Upload by:** [{pop}](tg://user?id={ah})",
        )
        await uh.delete()
        await oky.delete()
        await client.delete_messages(bot, 2)


modules_help["extras"] = {
    f"tiktok [link|reply]*": "Download video from tiktok, can use for download video ig or fb too.",
    "sg [id|reply]*": "Check history name of user",
    "json [reply]": "Show code of the text you replied",
    "limit": "Get your account limit info",
    "copy": "copy a message",
    "song": "download song from youtube",
    "video": "download video from youtube",
    "carbonlist": "list color of carbon",
    "carbon {color}": "create carbon text",
}
