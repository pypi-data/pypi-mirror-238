# Copyright (C) 2022 CtrlUB
#
# This file is a part of < https://github.com/kennedy-ex/CtrlUB/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/kennedy-ex/CtrlUB/blob/main/LICENSE/>.
#


import asyncio
import os
import re
import shlex
from datetime import datetime
from os.path import basename
from typing import Optional, Tuple

import aiofiles
import requests
import tracemoepy
from bs4 import BeautifulSoup
from gpytranslate import Translator
from pyrogram import Client, filters
from pyrogram.types import Message
from telegraph import Telegraph, upload_file

from Bdrl import *
from Bdrl.helpers.basic import edit_or_reply
from Bdrl.helpers.PyroHelpers import ReplyCheck
from Bdrl.helpers.tools import *
from Bdrl.utils import *
from Bdrl.utils import s_paste
from Bdrl.utils.pastebin import paste

telegraph = Telegraph()
r = telegraph.create_account(short_name="Kuntulmu")
auth_url = r["auth_url"]

pattern = re.compile(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$")


@Client.on_message(filters.command("paste", prefix) & filters.me)
async def paste_func(client: Client, message: Message):
    if not message.reply_to_message:
        return await eod(message, f"Reply To A Message With {prefix}paste")
    r = message.reply_to_message
    if not r.text and not r.document:
        return await eod(message, "Only text and documentsare supported.")
    m = await edit_or_reply(message, "`Pasting...`")
    if r.text:
        content = str(r.text)
    elif r.document:
        if r.document.file_size > 40000:
            return await eod(message, "You can only paste files smaller than 40KB.")
        if not pattern.search(r.document.mime_type):
            return await eod(message, "Only text files can be pasted.")
        doc = await message.reply_to_message.download()
        async with aiofiles.open(doc, mode="r") as f:
            content = await f.read()
        os.remove(doc)
    link = await paste(content)
    try:
        if m.from_user.is_bot:
            await message.reply_photo(
                photo=link,
                quote=False,
                reply_markup=kb,
            )
        else:
            await message.reply_photo(
                photo=link,
                quote=False,
                caption=f"**Paste Link:** [Here]({link})",
            )
        await m.delete()
    except Exception:
        await m.edit(f"[Here]({link}) your paste")


@Client.on_message(filters.command(["tg", "tgm", "telegraph"], prefix) & filters.me)
async def uptotelegraph(client: Client, message: Message):
    reply = message.reply_to_message
    filesize = 10948747
    await edit_or_reply(message, "`Processing...`")
    # if not replied
    if not reply:
        await eod(
            message,
            "`Please reply to the message, to get the link from the telegraph.`",
        )
    # replied to text
    elif reply.text:
        if len(reply.text) <= 4096:
            link = telegraph.create_page(
                client.me.first_name,
                html_content=(reply.text.html).replace("\n", "<br>"),
            )
            await message.edit(
                f"**Successfully uploaded to [Telegraph](https://telegra.ph/{link.get('path')})**",
                disable_web_page_preview=True,
            )
        else:
            await eod(message, "The length text exceeds 4096 characters")
    elif reply.media:
        if (
            reply.photo
            and reply.photo.file_size <= filesize
            or reply.video
            and reply.video.file_size <= filesize
            or reply.animation
            and reply.animation.file_size <= filesize
            or reply.sticker
            and reply.sticker.file_size <= filesize
            or reply.document
            and reply.document.file_size <= filesize
        ):
            if reply.animation or reply.sticker:
                loc = await client.download_media(reply, file_name=f"telegraph.png")
            else:
                loc = await client.download_media(reply)
            try:
                response = upload_file(loc)
            except Exception as e:
                return await eod(message, f"**ERROR:** `{e}`", time=20)
            await message.edit(
                f"**Successfully uploaded to [Telegraph](https://telegra.ph{response[0]})**",
                disable_web_page_preview=True,
            )
            if os.path.exists(loc):
                os.remove(loc)
        else:
            await eod(
                message,
                "Please check the file format or file size , it mustbe less than 10 mb . . .",
                time=20,
            )
    else:
        await eod(message, "Sorry, The File is not supported !")


@Client.on_message(filters.me & filters.command(["tr", "trt", "translate"], prefix))
async def translate(client: Client, message: Message):
    trl = Translator()
    if message.reply_to_message and (
        message.reply_to_message.text or message.reply_to_message.caption
    ):
        input_str = (
            message.text.split(None, 1)[1]
            if len(
                message.command,
            )
            != 1
            else None
        )
        target = input_str or "id"
        if message.reply_to_message.text:
            text = message.reply_to_message.text
        else:
            text = message.reply_to_message.caption
        try:
            tekstr = await trl(text, targetlang=target)
        except ValueError as err:
            await eod(
                message,
                f"**ERROR:** `{str(err)}`",
            )
            return
    else:
        input_str = (
            message.text.split(None, 2)[1]
            if len(
                message.command,
            )
            != 1
            else None
        )
        text = message.text.split(None, 2)[2]
        target = input_str or "id"
        try:
            tekstr = await trl(text, targetlang=target)
        except ValueError as err:
            await eod(message, "**ERROR:** `{}`".format(str(err)))
            return
    await edit_or_reply(
        message,
        f"**Detected language:** `{(await trl.detect(text))}` -> `{target}`\n\n```{tekstr.text}```",
    )


@Client.on_message(filters.command(["webshot", "webss"], prefix) & filters.me)
async def webshot(client: Client, message: Message):
    ok = await edit_or_reply(message, "`Processing...`")
    try:
        user_link = message.command[1]
        try:
            full_link = f"https://webshot.deam.io/{user_link}/?width=1920&height=1080?delay=2000?type=png"
            await client.send_photo(
                message.chat.id,
                full_link,
                caption=f"**Screenshot of the page ⟶** {user_link}",
            )
        except Exception as dontload:
            await eod(message, f"Error! {dontload}\nTrying again create screenshot...")
            full_link = f"https://mini.s-shot.ru/1920x1080/JPEG/1024/Z100/?{user_link}"
            await client.send_photo(
                message.chat.id,
                full_link,
                caption=f"**Screenshot of the page ⟶** {user_link}",
            )
        await ok.delete()
    except Exception as error:
        await ok.delete()
        await client.send_message(
            message.chat.id, f"**Something went wrong\nLog:{error}...**"
        )


@Client.on_message(filters.command("type", prefix) & filters.me)
async def types(client: Client, message: Message):
    orig_text = message.text.split(prefix + "type ", maxsplit=1)[1]
    text = orig_text
    tbp = ""
    typing_symbol = "▒"
    while tbp != orig_text:
        await message.edit(str(tbp + typing_symbol))
        await asyncio.sleep(0.10)
        tbp = tbp + text[0]
        text = text[1:]
        await message.edit(str(tbp))
        await asyncio.sleep(0.10)


@Client.on_message(filters.command(["directmessage", "dm"], prefix) & filters.me)
async def deem(client: Client, message: Message):
    ok = await edit_or_reply(message, "Usage:\n .dm @username Umm")
    quantity = 1
    inp = message.text.split(None, 2)[1]
    user = await client.get_chat(inp)
    spam_text = " ".join(message.command[2:])
    quantity = int(quantity)
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id
        for _ in range(quantity):
            await ok.edit("Message Sended Successfully ✅")
            await client.send_message(
                user.id, spam_text, reply_to_message_id=reply_to_id
            )
            await asyncio.sleep(0.15)
        return
    for _ in range(quantity):
        await client.send_message(user.id, spam_text)
        await ok.edit("Message Sended Successfully ✅")
        await asyncio.sleep(0.15)


@Client.on_message(filters.command("open", prefix) & filters.me)
async def open_file(client: Client, m: Message):
    xd = await edit_or_reply(m, "`Reading File!`")
    f = await client.download_media(m.reply_to_message)
    if f:
        _error = open(f, "r")
        _error_ = _error.read()
        _error.close()
        if len(_error_) >= 4096:
            await xd.edit("`Pasting to Spacebin!`")
            ext = "py"
            x = await s_paste(_error_, ext)
            s_link = x["url"]
            s_raw = x["raw"]
            pasted = f"**Pasted to Spacebin**\n**Link:** [Spacebin]({s_link})\n**Raw Link:** [Raw]({s_raw})"
            return await xd.edit(pasted, disable_web_page_preview=True)
        else:
            await xd.edit(f"**Output:**\n```{_error_}```")
    else:
        await eod(m, "Reply to a File to open it!")
        os.remove(f)


screen_shot = "Bdrl/plugins/cache/"


async def run_cmd(cmd: str) -> Tuple[str, str, int, int]:
    """run command in terminal"""
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


async def take_screen_shot(
    video_file: str, duration: int, path: str = ""
) -> Optional[str]:
    """take a screenshot"""
    ttl = duration // 2
    thumb_image_path = path or os.path.join(screen_shot, f"{basename(video_file)}.jpg")
    command = f"ffmpeg -ss {ttl} -i '{video_file}' -vframes 1 '{thumb_image_path}'"
    err = (await run_cmd(command))[1]
    if err:
        _LOG.error(err)
    return thumb_image_path if os.path.exists(thumb_image_path) else None


@Client.on_message(filters.me & filters.command(["reverse"], prefix))
async def google_rs(client: Client, message: Message):
    start = datetime.now()
    dis_loc = ""
    base_url = "http://www.google.com"
    out_str = "`Reply to an image`"
    if message.reply_to_message:
        message_ = message.reply_to_message
        if message_.sticker and message_.sticker.file_name.endswith(".tgs"):
            await message.delete()
            return
        if message_.photo or message_.animation or message_.sticker:
            dis = await client.download_media(message=message_, file_name=screen_shot)
            dis_loc = os.path.join(screen_shot, os.path.basename(dis))
        if message_.animation or message_.video:
            await message.edit("`Converting this Gif`")
            img_file = os.path.join(screen_shot, "grs.jpg")
            await take_screen_shot(dis_loc, 0, img_file)
            if not os.path.lexists(img_file):
                await message.edit("`Something went wrong in Conversion`")
                await asyncio.sleep(5)
                await message.delete()
                return
            dis_loc = img_file
        if dis_loc:
            search_url = "{}/searchbyimage/upload".format(base_url)
            multipart = {
                "encoded_image": (dis_loc, open(dis_loc, "rb")),
                "image_content": "",
            }
            google_rs_response = requests.post(
                search_url, files=multipart, allow_redirects=False
            )
            the_location = google_rs_response.headers.get("Location")
            os.remove(dis_loc)
        else:
            await message.delete()
            return
        await message.edit("`Found Google Result.`")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
        }
        response = requests.get(the_location, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        prs_div = soup.find_all("div", {"class": "r5a77d"})[0]
        prs_anchor_element = prs_div.find("a")
        prs_url = base_url + prs_anchor_element.get("href")
        prs_text = prs_anchor_element.text
        end = datetime.now()
        ms = (end - start).seconds
        out_str = f"""<b>Time Taken</b>: {ms} seconds
<b>Possible Related Search</b>: <a href="{prs_url}">{prs_text}</a>
<b>More Info</b>: Open this <a href="{the_location}">Link</a>
"""
    await message.edit(out_str, disable_web_page_preview=True)


@Client.on_message(filters.me & filters.command(["areverse"], prefix))
async def tracemoe_rs(client: Client, message: Message):
    dis_loc = ""
    if message.reply_to_message:
        message_ = message.reply_to_message
        if message_.sticker and message_.sticker.file_name.endswith(".tgs"):
            await message.delete()
            return
        if message_.photo or message_.animation or message_.sticker:
            dis = await client.download_media(message=message_, file_name=screen_shot)
            dis_loc = os.path.join(screen_shot, os.path.basename(dis))
        if message_.animation:
            await message.edit("`Converting this Gif`")
            img_file = os.path.join(screen_shot, "grs.jpg")
            await take_screen_shot(dis_loc, 0, img_file)
            if not os.path.lexists(img_file):
                await message.edit("`Something went wrong in Conversion`")
                await asyncio.sleep(5)
                await message.delete()
                return
            dis_loc = img_file
        if message_.video:
            nama = "video_{}-{}.mp4".format(
                message.reply_to_message.video.date,
                message.reply_to_message.video.file_size,
            )
            await client.download_media(
                message.reply_to_message.video, file_name="nana/downloads/" + nama
            )
            dis_loc = "handlers/cache/" + nama
            img_file = os.path.join(screen_shot, "grs.jpg")
            await take_screen_shot(dis_loc, 0, img_file)
            if not os.path.lexists(img_file):
                await message.edit("`Something went wrong in Conversion`")
                await asyncio.sleep(5)
                await message.delete()
                return
        if dis_loc:
            tracemoe = tracemoepy.async_trace.Async_Trace()
            if message_.video:
                search = await tracemoe.search(img_file, encode=True)
                os.remove(img_file)
                os.remove(dis_loc)
            else:
                search = await tracemoe.search(dis_loc, encode=True)
                os.remove(dis_loc)
            result = search["docs"][0]
            msg = (
                f"**Title**: {result['title_english']}"
                f"\n**Similarity**: {str(result['similarity'])[1:2]}"
                f"\n**Episode**: {result['episode']}"
            )
            preview = await tracemoe.video_preview(search)
            with open("preview.mp4", "wb") as f:
                f.write(preview)
            await message.delete()
            await client.send_video(
                message.chat.id,
                "preview.mp4",
                caption=msg,
                reply_to_message_id=ReplyCheck(message),
            )
            await asyncio.sleep(5)
            await message.delete()
            os.remove("preview.mp4")
        else:
            await message.delete()
            return
    else:
        await message.edit("`Reply to a message to proceed`")
        await asyncio.sleep(5)
        await message.delete()
        return


modules_help["misc"] = {
    "translate": f"or {prefix}tr Get translate of text you want.",
    f"telegraph | {prefix}tg | {prefix}tgm": "Upload a text or media to telegraph.",
    "webss": "Get a screenshoot of web.",
    "dm": "Send messages without open chatroom.",
    "open": "Open a file and see on space.bin.",
    "type": "Typewriter text types.",
    "patse": "Pasting a text or file to a web for easiest view.",
    "reverse": "Reply to a image",
    "areverse": "Reply to a text",
}
