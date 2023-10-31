import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from Bdrl.helpers.basic import eor
from Bdrl.utils import *


@Client.on_message(
    filters.command(["kntl", "kontil", "kuntul", "kontol"], prefix) & filters.me
)
async def kontol_(c: Client, m: Message):
    await eor(
        m,
        """
⣠⡶⠚⠛⠲⢄⡀
⣼⠁ ⠀⠀⠀ ⠳⢤⣄
⢿⠀⢧⡀⠀⠀⠀⠀⠀⢈⡇
⠈⠳⣼⡙⠒⠶⠶⠖⠚⠉⠳⣄
⠀⠀⠈⣇⠀⠀⠀⠀⠀⠀⠀⠈⠳⣄
⠀⠀⠀⠘⣆ ⠀⠀⠀⠀ ⠀⠈⠓⢦⣀
⠀⠀⠀⠀⠈⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠲⢤
⠀⠀⠀⠀⠀⠀⠙⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢧
⠀⠀⠀⠀⠀⠀⠀⡴⠋⠓⠦⣤⡀⠀⠀⠀⠀⠀⠀⠀⠈⣇
⠀⠀⠀⠀⠀⠀⣸⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡄
⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇
⠀⠀⠀⠀⠀⠀⢹⡄⠀⠀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃
⠀⠀⠀⠀⠀⠀⠀⠙⢦⣀⣳⡀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠏
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⢦⣀⣀⣀⣀⣠⡴⠚⠉
        """,
    )


@Client.on_message(filters.command("p", prefix) & filters.me)
async def assa(c: Client, m: Message):
    text = "<b>Assalamualaikum warahmatullahi wabarokatuh.</b>"
    await m.delete()
    if m.reply_to_message:
        await c.send_message(m.chat.id, text, reply_to_message_id=m.reply_to_message.id)
    else:
        await c.send_message(m.chat.id, text)


@Client.on_message(filters.command("l", prefix) & filters.me)
async def wassa(c: Client, m: Message):
    text = "<b>Waalaikumussalam warahmatullahi wabarokatuh.</b>"
    await m.delete()
    if m.reply_to_message:
        await c.send_message(m.chat.id, text, reply_to_message_id=m.reply_to_message.id)
    else:
        await c.send_message(m.chat.id, text)


@Client.on_message(filters.command(["otak", "brain"], prefix) & filters.me)
async def otakmu(c: Client, m: Message):
    y = await eor(m, "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠         <(^_^ <)🗑")
    await asyncio.sleep(0.2)
    await y.edit("YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠       <(^_^ <)  🗑")
    await asyncio.sleep(0.2)
    await y.edit("YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠     <(^_^ <)    🗑")
    await asyncio.sleep(0.2)
    await y.edit("YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠   <(^_^ <)      🗑")
    await asyncio.sleep(0.2)
    await y.edit("YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠 <(^_^ <)        🗑")
    await asyncio.sleep(0.2)
    await y.edit("YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠<(^_^ <)         🗑")
    await asyncio.sleep(0.2)
    await y.edit("YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n(> ^_^)>🧠         🗑")
    await asyncio.sleep(0.2)
    await y.edit("YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n  (> ^_^)>🧠       🗑")
    await asyncio.sleep(0.2)
    await y.edit("YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n    (> ^_^)>🧠     🗑")
    await asyncio.sleep(0.2)
    await y.edit("YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n      (> ^_^)>🧠   🗑")
    await asyncio.sleep(0.2)
    await y.edit("YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n        (> ^_^)>🧠 🗑")
    await asyncio.sleep(0.2)
    await y.edit("YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n          (> ^_^)>🧠🗑")
    await asyncio.sleep(0.2)
    await y.edit("YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n           (> ^_^)>🗑")
    await asyncio.sleep(0.2)
    await y.edit("YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n           <(^_^ <)🗑")


@Client.on_message(filters.command(["awokawok", "awkwk"], prefix) & filters.me)
async def awkkw(c: Client, m: Message):
    await m.edit(
        "────██──────▀▀▀██\n"
        "──▄▀█▄▄▄─────▄▀█▄▄▄\n"
        "▄▀──█▄▄──────█─█▄▄\n"
        "─▄▄▄▀──▀▄───▄▄▄▀──▀▄\n"
        "─▀───────▀▀─▀───────▀▀\n`Awkwokwokwok..`",
    )


@Client.on_message(filters.command(["babi", "pig"], prefix) & filters.me)
async def babii(c: Client, m: Message):
    await m.edit(
        "┈┈┏━╮╭━┓┈╭━━━━╮\n"
        "┈┈┃┏┗┛┓┃╭┫Ngok ┃\n"
        "┈┈╰┓▋▋┏╯╯╰━━━━╯\n"
        "┈╭━┻╮╲┗━━━━╮╭╮┈\n"
        "┈┃▎▎┃╲╲╲╲╲╲┣━╯┈\n"
        "┈╰━┳┻▅╯╲╲╲╲┃┈┈┈\n"
        "┈┈┈╰━┳┓┏┳┓┏╯┈┈┈\n"
        "┈┈┈┈┈┗┻┛┗┻┛┈┈┈┈\n",
    )


modules_help["animation"] = {
    "babi": "Chrck it yourself",
    "kntl": "Check it yourself",
    "otak": "Check it yourself",
    "awkwk": "Check it yourself",
}
