# Copyright (C) 2022 CtrlUB
#
# This file is a part of < https://github.com/kennedy-ex/CtrlUB/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/kennedy-ex/CtrlUB-Userbot/blob/main/LICENSE/>.
#

from datetime import datetime
from platform import python_version as yy
from time import time

import speedtest
from pyrogram import Client
from pyrogram import __version__ as k
from pyrogram import filters
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid, UsernameInvalid
from pyrogram.raw import functions
from pyrogram.types import Message
from pytgcalls import __version__ as tv

import Bdrl.helpers.sql.globals as sql
from Bdrl import StartTime
from Bdrl.helpers.adminHelpers import DEVS
from Bdrl.helpers.basic import edit_or_reply
from Bdrl.helpers.expand import expand_url
from Bdrl.helpers.PyroHelpers import SpeedConvert
from Bdrl.helpers.tools import get_arg
from Bdrl.utils import *
from Bdrl.utils.tools import get_readable_time
from Bdrl.version import __version__ as botver

ALIVE_TEXT = """{}

• <b>Uptime:</b> <code>{}</code>
• <b>Python:</b> <code>{}</code>
• <b>PyTgcalls:</b> <code>{}</code>
• <b>Pyrogram:</b> <code>{}</code>
• <b>Version:</b> <code>{}</code>
• <b>UserMode:</b> {}
"""


@Client.on_message(filters.command("id", prefix) & filters.me)
async def getids(client: Client, message: Message):
    out_str = f"👥 **Chat ID:** `{message.chat.id}`\n💌 **Message ID**: `{message.id}`"
    input = get_arg(message)
    msg = message.reply_to_message
    if input:
        try:
            ok = await client.get_users(input)
            out_str = f"🔗 **Name:** {ok.mention}\n👤 **User ID:** `{ok.id}`"
        except IndexError:
            ok = await client.get_chat(input)
            out_str = f"🔗 **Title:** {ok.title}\n👥 **Chat ID:** `{ok.id}`"
        except UsernameInvalid:
            out_str = "`Cant find that user/chat...`"
        except PeerIdInvalid:
            out_str = "`Cant find that user/chat...`"
    elif msg:
        out_str = f"👥 **Chat ID** : `{(msg.chat).id}`\n"
        out_str += f"💌 **Message ID** : `{msg.id}`\n"
        if msg.from_user:
            out_str += f"🔗 **From User ID** : `{msg.from_user.id}`\n"
        if msg.sender_chat:
            out_str += f"👥 **Channel ID** : `{msg.sender_chat.id}`\n"
        file_id = None
        if msg and msg.audio:
            type_ = "audio"
            file_id = msg.audio.file_id
        elif msg and msg.animation:
            type_ = "animation"
            file_id = msg.animation.file_id
        elif msg and msg.document:
            type_ = "document"
            file_id = msg.document.file_id
        elif msg and msg.photo:
            type_ = "photo"
            file_id = msg.photo.file_id
        elif msg and msg.sticker:
            type_ = "sticker"
            file_id = msg.sticker.file_id
        elif msg and msg.voice:
            type_ = "voice"
            file_id = msg.voice.file_id
        elif msg and msg.video_note:
            type_ = "video_note"
            file_id = msg.video_note.file_id
        elif msg and msg.video:
            type_ = "video"
            file_id = msg.video.file_id
        if file_id != None:
            out_str += f"📄 **Media Type:** `{type_}`\n"
            out_str += f"📄 **File ID:** `{file_id}`"
    await message.edit(out_str)


@Client.on_message(filters.command(["speed", "speedtest"], prefix) & filters.me)
async def speed_test(client: Client, message: Message):
    new_msg = await edit_or_reply(message, "`Running speed test . . .`")
    spd = speedtest.Speedtest()
    new_msg = await message.edit(
        f"`{new_msg.text}`\n" "`Getting best server based on ping . . .`"
    )
    spd.get_best_server()
    new_msg = await message.edit(f"`{new_msg.text}`\n" "`Testing download speed . . .`")
    spd.download()
    new_msg = await message.edit(f"`{new_msg.text}`\n" "`Testing upload speed . . .`")
    spd.upload()
    new_msg = await new_msg.edit(
        f"`{new_msg.text}`\n" "`Getting results and preparing formatting . . .`"
    )
    results = spd.results.dict()
    SpeedTest = (
        "Speedtest started at `{start}`\n\n"
        "Ping:\n{ping} ms\n\n"
        "Download:\n{download}\n\n"
        "Upload:\n{upload}\n\n"
        "ISP:\n__{isp}__"
    )
    await message.edit(
        SpeedTest.format(
            start=results["timestamp"],
            ping=results["ping"],
            download=SpeedConvert(results["download"]),
            upload=SpeedConvert(results["upload"]),
            isp=results["client"]["isp"],
        )
    )


@Client.on_message(filters.command("dc", prefix) & filters.me)
async def nearest_dc(client: Client, message: Message):
    dc = await client.invoke(functions.help.GetNearestDc())
    NearestDC = "Country: `{}`\n" "Nearest Datacenter: `{}`\n" "ThisDatacenter: `{}`"
    await edit_or_reply(
        message, NearestDC.format(dc.country, dc.nearest_dc, dc.this_dc)
    )


@Client.on_message(filters.command("cping", ".") & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command("ping", prefix) & filters.me)
async def pingme(client: Client, message: Message):
    start = datetime.now()
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await message.reply_text(f"🏓 **Pong!**\n" f"`%sms`" % (duration))


@Client.on_message(filters.command("bdrl", ".") & filters.user(DEVS) & ~filters.me)
async def kontol(c: Client, m: Message):
    await edit_or_reply(m, "mwah 😘")


@Client.on_message(filters.command("expand", prefix) & filters.me)
async def expand(client: Client, message: Message):
    if message.reply_to_message:
        url = message.reply_to_message.text or message.reply_to_message.caption
    elif len(message.command) > 1:
        url = message.command[1]
    else:
        url = None
    if url:
        expanded = await expand_url(url)
        if expanded:
            await message.edit(
                f"<b>Shortened URL</b>: {url}\n<b>Expanded URL</b>: {expanded}",
                disable_web_page_preview=True,
            )
        else:
            await message.edit("No bro that's not what I do")
    else:
        await message.edit("Nothing to expand")


@Client.on_message(filters.command(["alive", "on"], prefix) & filters.me)
async def alive(c: Client, m: Message):
    uptime = await get_readable_time((time() - StartTime))
    full = f"{c.me.first_name}" + f"{c.me.last_name}"
    if c.me.last_name:
        fullname = f"<a href='tg://user?id={c.me.id}'>{full}</a>"
    else:
        fullname = f"<a href='tg://user?id={c.me.id}'>{c.me.first_name}</a>"
    if sql.gvarstatus("ALIVE_LOGO") and sql.gvarstatus("ALIVE_LOGO").endswith(".jpg"):
        await c.send_photo(
            m.chat.id,
            photo=sql.gvarstatus("ALIVE_LOGO"),
            caption=ALIVE_TEXT.format(
                sql.gvarstatus("ALIVE_CUSTOM")
                if sql.gvarstatus("ALIVE_CUSTOM") != None
                else "<b><a href='https://t.me/metahoe'>Bdrl</a> is Up and Running!</b>",
                uptime,
                yy(),
                tv,
                k,
                botver,
                fullname,
            ),
        )
        await m.delete()
    elif sql.gvarstatus("ALIVE_LOGO") and sql.gvarstatus("ALIVE_LOGO").endswith(".mp4"):
        await c.send_video(
            m.chat.id,
            video=sql.gvarstatus("ALIVE_LOGO"),
            caption=ALIVE_TEXT.format(
                sql.gvarstatus("ALIVE_CUSTOM")
                if sql.gvarstatus("ALIVE_CUSTOM") != None
                else "<b><a href='https://t.me/metahoe'>Bdrl</a> is Up and Running!</b>",
                uptime,
                yy(),
                tv,
                k,
                botver,
                fullname,
            ),
        )
        await m.delete()
    else:
        return await m.edit(
            ALIVE_TEXT.format(
                sql.gvarstatus("ALIVE_CUSTOM")
                if sql.gvarstatus("ALIVE_CUSTOM") != None
                else "<b><a href='https://t.me/metahoe'>Bdrl</a> is Up and Running!</b>",
                uptime,
                yy(),
                tv,
                k,
                botver,
                fullname,
            ),
            disable_web_page_preview=True,
        )


@Client.on_message(
    filters.command(["setalivepic", "setalivelogo"], prefix) & filters.me
)
async def alive_pic(client: Client, m: Message):
    if len(m.command) != 2:
        return await m.edit("Give me a link telegra.ph media or status `off`.")
    logo = m.text.split(None, 1)[1]
    if logo.endswith(".mp4"):
        type = "Video"
        sql.addgvar("ALIVE_LOGO", logo)
        ok = await m.edit("`Processing...`")
        await ok.edit(f"✅ <b>Alive media has been set to use</b> <code>{type}</code>")
    elif logo.endswith(".jpg") or logo.endswith(".png"):
        type = "Photo"
        sql.addgvar("ALIVE_LOGO", logo)
        ok = await m.edit("`Processing...`")
        await ok.edit(f"✅ <b>Alive media has been set to use</b> <code>{type}</code>")
    elif logo == "off" or logo == "OFF":
        type = "No media"
        sql.delgvar("ALIVE_LOGO")
        ok = await m.edit("`Processing...`")
        await ok.edit("✅ <b>Alive media has been</b> <code>disabled.</code>")
    else:
        return await m.edit(
            f"👀 <b>What are you looking for?</b>\n\n• Current alive media is <code>{type}</code>"
        )


@Client.on_message(filters.command("setalivetext", prefix) & filters.me)
async def set_alive_text(client: Client, m: Message):
    k = get_arg(m)
    teks = f"{k[:700]}"
    if teks:
        sql.addgvar("ALIVE_CUSTOM", teks)
        ok = await m.edit("`Processing...`")
        await ok.edit(
            f"✅ **Alive custom text has been saved!**\n\n• new alive_text: `{teks}`"
        )
    else:
        return await m.edit(
            f"Wrong usage command, check `{prefix}help alive` to know more."
        )


@Client.on_message(filters.command("resetalivetext", prefix) & filters.me)
async def reset_alive_text(c: Client, m: Message):
    teks = "<b><a href='https://t.me/metahoe'>Bdrl</a> is Up and Running!</b>"
    sql.addgvar("ALIVE_CUSTOM", teks)
    ok = await m.edit("`Processing...`")
    await ok.edit(
        f"✅ <b>Alive custom text has been reset!</b>\n\n• current text: <code>{teks}</code>"
    )


@Client.on_message(
    filters.command(["rmalivetext", "removealivetext"], prefix) & filters.me
)
async def rm_alive_text(c: Client, m: Message):
    sql.addgvar("ALIVE_CUSTOM", "")
    ok = await m.edit("`Processing...`")
    await ok.edit(f"✅ <b>Alive custom text has been set up to empty.</b>")


@Client.on_message(filters.command("alivetext", prefix) & filters.me)
async def alivetext(c: Client, m: Message):
    await m.edit(
        "👀 Your current custom alive text is\n\n• `{}`".format(
            sql.gvarstatus("ALIVE_CUSTOM")
            if sql.gvarstatus("ALIVE_CUSTOM") != None
            else "<b><a href='https://t.me/metahoe'>Bdrl</a> is Up and Running!</b>"
        ),
        disable_web_page_preview=True,
    )


@Client.on_message(filters.command(["repo"], prefix) & filters.me)
async def repos(c: Client, m: Message):
    await m.edit(
        "👀 <b>Hey I am using Bdrl</b>"
        "\n\n📶 <b>Bot version:</b> <code>{}</code>"
        "\n🐍 <b>Python version:</b> <code>{}</code>"
        "\n🔥 <b>Pyrogram version:</b> <code>{}</code>"
        "\n🎧 <b>PyTgcalls version:</b> <code>{}</code>"
        "\n📡 <b>Deploy by click:</b> <a href='https://heroku.com/deploy?template=https://github.com/Yansaii/Bdrl-Userbot'>Here</a>".format(
            botver, yy(), k, tv
        ),
        disable_web_page_preview=True,
    )


@Client.on_message(filters.command("deploy", prefix) & filters.me)
async def deployy(c: Client, m: Message):
    await m.edit(
        "🔥 **Make your own Bdrl!**"
        "\n\n👥 Support Chat: [Here](https://telegram.dog/metahoe)"
        "\n🔗 Deploy link: [Here](https://heroku.com/deploy?template=https://github.com/Yansaii/Bdrl-Userbot)"
        "\n💌 String Generator: [Here Choose pyroV2](https://telegram.dog/Bdrlstringbot)",
        disable_web_page_preview=True,
    )


modules_help["system"] = {
    "ping": "Calculates ping time between you and Telegram.",
    "alive": "Get alive bot",
    "repo": "Show link repository of Bdrl",
    "dc": "Get's your Telegram DC.",
    "id": "Get User/Chat ID",
    f"speedtest `or` {prefix}speed": "Runs a speedtest on the server this userbot is hosted..Flex on them haters. With an in "
    "Telegram Speedtest of your server..",
}


modules_help["alive"] = {
    "alive": "To get your userbot status alive.",
    "setalivetext": "To set custom text in alive. Can use HTML formatting.",
    "resetalivetext": "Reset your alive text to default.",
    "alivetext": "Show current alive text",
    "rmalivetext": "Remove alive text custom",
    "setalivepic {link telegram.ph or off}": "Set your alive media, give link telegram.ph or send status OFF do disable media.",
}
