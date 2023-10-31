# Copyright (C) 2022 by kennedy-ex|@Github, < https://github.com/kennedy-ex >.
#
# This file is part of < https://github.com/kennedy-ex/CtrlUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/kennedy-ex/CtrlUB/blob/main/LICENSE >
#
# All rights reserved.


import asyncio
import os
import textwrap
from random import choice

import cv2
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, emoji, filters
from pyrogram.errors import StickersetInvalid, YouBlockedUser
from pyrogram.raw.functions.messages import GetStickerSet
from pyrogram.raw.types import InputStickerSetShortName
from pyrogram.types import Message

from Bdrl.helpers.tools import *
from Bdrl.utils import *


@Client.on_message(filters.command(["stkrinfo", "stickerinfo"], prefix) & filters.me)
async def packinfo(c: Client, m: Message):
    rep = await m.edit_text("`Processing...`")
    if not m.reply_to_message:
        await rep.edit("`Reply to a sticker...`")
        return
    if not m.reply_to_message.sticker:
        await rep.edit("`Reply to a sticker...`")
        return
    if not m.reply_to_message.sticker.set_name:
        await rep.edit("`Maybe this not a package sticker.`")
        return
    stickerset = await c.invoke(
        GetStickerSet(
            stickerset=InputStickerSetShortName(
                short_name=m.reply_to_message.sticker.set_name
            ),
            hash=0,
        )
    )
    emojis = []
    for stucker in stickerset.packs:
        if stucker.emoticon not in emojis:
            emojis.append(stucker.emoticon)
    output = f"""**Sticker Pack Title **: `{stickerset.set.title}`
**Sticker Pack Short Name **: `{stickerset.set.short_name}`
**Stickers Count **: `{stickerset.set.count}`
**Archived **: `{stickerset.set.archived}`
**Official **: `{stickerset.set.official}`
**Masks **: `{stickerset.set.masks}`
**Animated **: `{stickerset.set.animated}`
**Emojis In Pack **: `{' '.join(emojis)}`
"""
    await rep.edit(output)


@Client.on_message(filters.command("kang", prefix) & filters.me)
async def kang(c: Client, m: Message):
    user = c.me
    replied = m.reply_to_message
    ok = await m.edit(f"`{choice(KANGING_STR)}`")
    media_ = None
    emoji_ = None
    is_anim = False
    is_video = False
    resize = False
    ff_vid = False
    if replied and replied.media:
        if replied.photo:
            resize = True
        elif replied.document and "image" in replied.document.mime_type:
            resize = True
            replied.document.file_name
        elif replied.document and "tgsticker" in replied.document.mime_type:
            is_anim = True
            replied.document.file_name
        elif replied.document and "video" in replied.document.mime_type:
            resize = True
            is_video = True
            ff_vid = True
        elif replied.animation:
            resize = True
            is_video = True
            ff_vid = True
        elif replied.video:
            resize = True
            is_video = True
            ff_vid = True
        elif replied.sticker:
            if not replied.sticker.file_name:
                await ok.edit("**This sticker doesn't have name!**")
                return
            emoji_ = replied.sticker.emoji
            is_anim = replied.sticker.is_animated
            is_video = replied.sticker.is_video
            if not (
                replied.sticker.file_name.endswith(".tgs")
                or replied.sticker.file_name.endswith(".webm")
            ):
                resize = True
                ff_vid = True
        else:
            await ok.edit("**File not supported**")
            return
        media_ = await c.download_media(replied, file_name="bdrl/resources/")
    else:
        await ok.edit("`Please reply to media/stickers...`")
        return
    if media_:
        args = get_arg(m)
        pack = 1
        if len(args) == 2:
            emoji_, pack = args
        elif len(args) == 1:
            if args[0].isnumeric():
                pack = int(args[0])
            else:
                emoji_ = args[0]
        if emoji_ and emoji_ not in (
            getattr(emoji, _) for _ in dir(emoji) if not _.startswith("_")
        ):
            emoji_ = None
        if not emoji_:
            emoji_ = "🐳"
        usn = user.username
        u_name = "@" + usn if usn else user.first_name or user.id
        packname = f"Sticker_u{user.id}_v{pack}"
        custom_packnick = f"{u_name} Sticker Pack"
        packnick = f"{custom_packnick} Vol.{pack}"
        cmd = "/newpack"
        if resize:
            media_ = await resize_media(media_, is_video, ff_vid)
        if is_anim:
            packname += "_animated"
            packnick += " (Animated)"
            cmd = "/newanimated"
        if is_video:
            packname += "_video"
            packnick += " (Video)"
            cmd = "/newvideo"
        exist = False
        while True:
            try:
                exist = await c.invoke(
                    GetStickerSet(
                        stickerset=InputStickerSetShortName(short_name=packname), hash=0
                    )
                )
            except StickersetInvalid:
                exist = False
                break
            limit = 50 if (is_video or is_anim) else 120
            if exist.set.count >= limit:
                pack += 1
                packname = f"a{user.id}_by_Bdrl_{pack}"
                packnick = f"{custom_packnick} Vol.{pack}"
                if is_anim:
                    packname += f"_anim{pack}"
                    packnick += f" (Animated){pack}"
                if is_video:
                    packname += f"_video{pack}"
                    packnick += f" (Video){pack}"
                await ok.edit(f"`Creating new pack because {pack} is full...`")
                continue
            break
        if exist is not False:
            try:
                await c.send_message("stickers", "/addsticker")
            except YouBlockedUser:
                await c.unblock_user("stickers")
                await c.send_message("stickers", "/addsticker")
            except Exception as e:
                return await ok.edit(f"**ERROR:** `{e}`")
            await asyncio.sleep(2)
            await c.send_message("stickers", packname)
            await asyncio.sleep(2)
            limit = "50" if is_anim else "120"
            while limit in await get_response(m, c):
                pack += 1
                packname = f"a{user.id}_by_{user.username}_{pack}"
                packnick = f"{custom_packnick} vol.{pack}"
                if is_anim:
                    packname += "_anim"
                    packnick += " (Animated)"
                if is_video:
                    packname += "_video"
                    packnick += " (Video)"
                await ok.edit(
                    "`Creating a new pack because " + str(pack) + " is full...`"
                )
                await c.send_message("stickers", packname)
                await asyncio.sleep(2)
                if await get_response(m, c) == "Invalid pack selected.":
                    await c.send_message("stickers", cmd)
                    await asyncio.sleep(2)
                    await c.send_message("stickers", packnick)
                    await asyncio.sleep(2)
                    await c.send_document("stickers", media_)
                    await asyncio.sleep(2)
                    await c.send_message("Stickers", emoji_)
                    await asyncio.sleep(2)
                    await c.send_message("Stickers", "/publish")
                    await asyncio.sleep(2)
                    if is_anim:
                        await c.send_message(
                            "Stickers", f"<{packnick}>", parse_mode=ParseMode.MARKDOWN
                        )
                        await asyncio.sleep(2)
                    await c.send_message("Stickers", "/skip")
                    await asyncio.sleep(2)
                    await c.send_message("Stickers", packname)
                    await asyncio.sleep(2)
                    await ok.edit(
                        f"<b>Sticker <a href='https://t.me/addstickers/{packname}'>kanged!</a></b>"
                        f"\n<b>Emoji:</b> {emoji_}",
                        disable_web_page_preview=True,
                    )
                    return
            await c.send_document("stickers", media_)
            await asyncio.sleep(2)
            if await get_response(m, c) == "Sorry, the file type is invalid.":
                await ok.edit("**Failed to adding stickers, try manually.**")
                return
            await c.send_message("Stickers", emoji_)
            await asyncio.sleep(2)
            await c.send_message("Stickers", "/done")
        else:
            await ok.edit("`Brewing new pack`")
            try:
                await c.send_message("Stickers", cmd)
            except YouBlockedUser:
                await c.unblock_user("stickers")
                await c.send_message("stickers", "/addsticker")
            await asyncio.sleep(2)
            await c.send_message("Stickers", packnick)
            await asyncio.sleep(2)
            await c.send_document("stickers", media_)
            await asyncio.sleep(2)
            if await get_response(m, c) == "Sorry, the file type is invalid.":
                await ok.edit("Failed adding sticker, try manually!")
                return
            await c.send_message("Stickers", emoji_)
            await asyncio.sleep(2)
            await c.send_message("Stickers", "/publish")
            await asyncio.sleep(2)
            if is_anim:
                await c.send_message("Stickers", f"<{packnick}>")
                await asyncio.sleep(2)
            await c.send_message("Stickers", "/skip")
            await asyncio.sleep(2)
            await c.send_message("Stickers", packname)
            await asyncio.sleep(2)
        await ok.edit(
            f"<b>Sticker <a href='https://t.me/addstickers/{packname}'>kanged!</a></b>"
            f"\n<b>Emoji:</b> {emoji_}",
            disable_web_page_preview=True,
        )
        if os.path.exists(str(media_)):
            os.remove(media_)


async def get_response(m, c):
    return [x async for x in c.get_chat_history("Stickers", limit=1)][0].text


@Client.on_message(filters.command(["getsticker", "mtoi"], prefix) & filters.me)
async def getsticker(client: Client, message: Message):
    replied = message.reply_to_message
    chat = message.chat.id
    if not replied or not replied.sticker:
        return await message.edit("`Reply to a sticker...`")
    xx = await message.edit("`Converting....`")
    cool = await convert_to_image(message, client)
    file_name = resize_image(cool)
    await client.send_photo(chat, photo=file_name, reply_to_message_id=replied.id)
    await xx.delete()


@Client.on_message(filters.command("tiny", prefix) & filters.me)
async def tinying(c: Client, m: Message):
    reply = m.reply_to_message
    if not (reply and (reply.media)):
        return await m.edit("`Please reply to a sticker`")
    kontol = await m.edit("`Processing tiny...`")
    ik = await c.download_media(reply)
    im1 = Image.open("Bdrl/utils/core/bdrl.png")
    if ik.endswith(".tgs"):
        await c.download_media(reply, "bdrl.tgs")
        os.system("lottie_convert.py bdrl.tgs json.json")
        json = open("json.json", "r")
        jsn = json.read()
        jsn = jsn.replace("512", "2000")
        ("json.json", "w").write(jsn)
        os.system("lottie_convert.py json.json bdrl.tgs")
        file = "bdrl.tgs"
        os.remove("json.json")
    elif ik.endswith((".gif", ".mp4")):
        iik = cv2.VideoCapture(ik)
        busy = iik.read()
        cv2.imwrite("i.png", busy)
        fil = "i.png"
        im = Image.open(fil)
        z, d = im.size
        if z == d:
            xxx, yyy = 200, 200
        else:
            t = z + d
            a = z / t
            b = d / t
            aa = (a * 100) - 50
            bb = (b * 100) - 50
            xxx = 200 + 5 * aa
            yyy = 200 + 5 * bb
        k = im.resize((int(xxx), int(yyy)))
        k.save("k.png", format="PNG", optimize=True)
        im2 = Image.open("k.png")
        back_im = im1.copy()
        back_im.paste(im2, (150, 0))
        back_im.save("o.webp", "WEBP", quality=95)
        file = "o.webp"
        os.remove(fil)
        os.remove("k.png")
    else:
        im = Image.open(ik)
        z, d = im.size
        if z == d:
            xxx, yyy = 200, 200
        else:
            t = z + d
            a = z / t
            b = d / t
            aa = (a * 100) - 50
            bb = (b * 100) - 50
            xxx = 200 + 5 * aa
            yyy = 200 + 5 * bb
        k = im.resize((int(xxx), int(yyy)))
        k.save("k.png", format="PNG", optimize=True)
        im2 = Image.open("k.png")
        back_im = im1.copy()
        back_im.paste(im2, (150, 0))
        back_im.save("o.webp", "WEBP", quality=95)
        file = "o.webp"
        os.remove("k.png")
    await c.send_sticker(m.chat.id, sticker=file, reply_to_message_id=reply.id)
    await kontol.delete()
    os.remove(file)
    os.remove(ik)


@Client.on_message(filters.command(["mmf", "memify"], prefix) & filters.me)
async def memify(c: Client, m: Message):
    if not m.reply_to_message_id:
        await m.edit("`Provide Some Text To Draw! And Reply To Image/Stickers`")
        return
    reply_message = m.reply_to_message
    if not reply_message.media:
        await m.edit("```Reply to a image/sticker.```")
        return
    file = await c.download_media(reply_message)
    msg = await m.edit("```Memifying this image! (」ﾟﾛﾟ)｣ ```")
    text = get_arg(m)
    if len(text) < 1:
        return await msg.edit(f"You might want to try `{prefix}mmf text`")
    meme = await drawText(file, text)
    await c.send_sticker(m.chat.id, sticker=meme, reply_to_message_id=reply_message.id)
    await msg.delete()
    os.remove(meme)


# Taken from https://github.com/UsergeTeam/Userge-Plugins/blob/master/plugins/memify.py#L64
# Maybe replyed to suit the needs of this module


async def drawText(image_path, text):
    img = Image.open(image_path)
    os.remove(image_path)
    i_width, i_height = img.size
    fnt = "Bdrl/utils/core/default.ttf"
    m_font = ImageFont.truetype(fnt, int((70 / 640) * i_width))
    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""
    draw = ImageDraw.Draw(img)
    current_h, pad = 10, 5
    if upper_text:
        for u_text in textwrap.wrap(upper_text, width=15):
            u_width, u_height = draw.textsize(u_text, font=m_font)
            draw.text(
                xy=(((i_width - u_width) / 2) - 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(((i_width - u_width) / 2) + 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=((i_width - u_width) / 2, int(((current_h / 640) * i_width)) - 2),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(((i_width - u_width) / 2), int(((current_h / 640) * i_width)) + 2),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=((i_width - u_width) / 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(255, 255, 255),
            )
            current_h += u_height + pad
    if lower_text:
        for l_text in textwrap.wrap(lower_text, width=15):
            u_width, u_height = draw.textsize(l_text, font=m_font)
            draw.text(
                xy=(
                    ((i_width - u_width) / 2) - 2,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    ((i_width - u_width) / 2) + 2,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    (i_height - u_height - int((20 / 640) * i_width)) - 2,
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    (i_height - u_height - int((20 / 640) * i_width)) + 2,
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(255, 255, 255),
            )
            current_h += u_height + pad
    image_name = "memify.webp"
    webp_file = os.path.join(image_name)
    img.save(webp_file, "webp")
    return webp_file


@Client.on_message(filters.command("q", prefix) & filters.me)
async def quotly(c: Client, m: Message):
    ok = get_arg(m)
    if not m.reply_to_message and not memek:
        await m.edit("`Reply to any users text message`")
        return
    bot = "QuotLyBot"
    m.chat.id
    if m.reply_to_message:
        await m.edit("`Making a Quote . . .`")
        await c.unblock_user(bot)
        if ok:
            await c.send_message(bot, f"/qcolor {ok}")
            await asyncio.sleep(1)
        else:
            pass
        await m.reply_to_message.forward(bot)
        await asyncio.sleep(5)
        async for pepek in c.search_messages(bot, limit=1):
            if pepek:
                await m.delete()
                await m.reply_sticker(
                    sticker=pepek.sticker.file_id,
                    reply_to_message_id=m.reply_to_message.id
                    if m.reply_to_message
                    else None,
                )
            else:
                return await m.edit_text("`Something went wrong . . .`")


KANGING_STR = (
    "Using Witchery to kang this sticker...",
    "Plagiarising hehe...",
    "Inviting this sticker over to my pack...",
    "Kanging this sticker...",
    "Hey that's a nice sticker!\nMind if I kang?!...",
    "Hehe me stel ur stikér\nhehe.",
    "Ay look over there (☉｡☉)!→\nWhile I kang this...",
    "Roses are red violets are blue, kanging this sticker so my pacc looks cool",
    "Imprisoning this sticker...",
    "Mr.Steal Your Sticker is stealing this sticker... ",
)


modules_help["sticker"] = {
    "kang": "Inviting a sticker to you sticker pack.",
    f"stkrinfo or {prefix}stickerinfo": "Get info about a pack.",
    "mtoi": "Get a convert from sticker to image.",
    "tiny": "Create a small sticker with reply.",
    "mmf": "memifying a image or sticker.",
    "q {color} or None": "generate a quote sticker",
}
