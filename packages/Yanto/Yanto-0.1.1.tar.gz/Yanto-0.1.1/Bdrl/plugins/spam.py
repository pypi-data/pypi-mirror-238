# Copyright (C) 2022 CtrlUB
#
# This file is a part of < https://github.com/kennedy-ex/CtrlUB/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/kennedy-ex/CtrlUB-Userbot/blob/main/LICENSE/>.
#


import asyncio
from threading import Event

from pyrogram import Client, enums, filters
from pyrogram.errors.exceptions.bad_request_400 import (
    MessageIdInvalid,
    ReactionEmpty,
    ReactionInvalid,
)
from pyrogram.types import Message

from Bdrl.config import BLACKLIST_CHAT, BOTLOG_CHATID
from Bdrl.helpers.basic import edit_or_reply
from Bdrl.utils import modules_help, prefix
from Bdrl.utils.misc import extract_args

emojis = [
    "👍",
    "👎",
    "❤️",
    "🔥",
    "🥰",
    "👏",
    "😁",
    "🤔",
    "🤯",
    "😱",
    "🤬",
    "😢",
    "🎉",
    "🤩",
    "🤮",
    "💩",
    "🐳",
    "👌",
    "🕊️",
    "🤡",
    "🌚",
    "🤣",
    "🥱",
    "🥴",
    "🌭",
]


@Client.on_message(filters.command("spamreact", prefix) & filters.me)
async def reactspam(c: Client, m: Message):
    if m.chat.id == BLACKLIST_CHAT:
        return await m.edit("<code>Thats command is not allowed in this chat!`")
    if len(m.command) < 3:
        return await edit_or_reply(
            m, f"**Format:** `{prefix}spamreact [total] [emoji]`"
        )
    amount = int(m.command[1])
    reaction = " ".join(m.command[2:])
    await m.edit(f"`Here we go!!!`")
    for i in range(amount):
        if reaction in emojis:
            try:
                await c.send_reaction(m.chat.id, m.id - i, reaction)
            except ReactionInvalid:
                return await m.edit("`Reaction isn't allowed in this chat`")
            except ReactionEmpty:
                return await m.edit("`Reaction isn't allowed in this chat`")
            except MessageIdInvalid:
                pass
        else:
            return await m.edit(
                f"You can only use `[👍, 👎, ❤️, 🔥, 🥰, 👏, 😁, 🤔, 🤯, 😱, 🤬, 😢, 🎉, 🤩, 🤮, 💩]`"
            )
    await m.edit(f"`Done doing spam reaction`")


commands = ["spam", "statspam", "slowspam", "fastspam"]
SPAM_COUNT = [0]


def increment_spam_count():
    SPAM_COUNT[0] += 1
    return spam_allowed()


def spam_allowed():
    return SPAM_COUNT[0] < 50


@Client.on_message(filters.me & filters.command(["dspam", "delayspam"], prefix))
async def delayspam(client: Client, message: Message):
    if message.chat.id in BLACKLIST_CHAT:
        return await edit_or_reply(
            message, "**This command is forbidden to use in this group**"
        )
    delayspam = await extract_args(message)
    arr = delayspam.split()
    if len(arr) < 3 or not arr[0].isdigit() or not arr[1].isdigit():
        await message.edit(f"`Usage: {prefix}delayspam (time) (count) (text).`")
        return
    delay = int(arr[0])
    count = int(arr[1])
    spam_message = delayspam.replace(arr[0], "", 1)
    spam_message = spam_message.replace(arr[1], "", 1).strip()
    await message.delete()
    if not spam_allowed():
        return
    delaySpamEvent = Event()
    for i in range(0, count):
        if i != 0:
            delaySpamEvent.wait(delay)
        await message.reply(spam_message)
        limit = increment_spam_count()
        if not limit:
            break
    await client.send_message(
        BOTLOG_CHATID, "**#DELAYSPAM**\nDelaySpam was executed successfully"
    )


@Client.on_message(filters.command(commands, prefix) & filters.me)
async def sspam(client: Client, message: Message):
    if message.chat.id in BLACKLIST_CHAT:
        return await edit_or_reply(
            message, "**This command is forbidden to use in this group**"
        )
    try:
        amount = int(message.command[1])
        if message.reply_to_message:
            text = message.reply_to_message.text
        else:
            text = " ".join(message.command[2:])
    except IndexError:
        return await edit_or_reply(message, "`Give me a count and text to spam.`")
    cooldown = {"spam": 0.15, "statspam": 0.1, "slowspam": 0.9, "fastspam": 0}
    for msg in range(amount):
        await message.delete()
        if message.reply_to_message:
            sent = await client.send_message(message.chat.id, text)
        else:
            sent = await client.send_message(message.chat.id, text)
        if message.command[0] == "statspam":
            await asyncio.sleep(0.1)
            await sent.delete()
        await asyncio.sleep(cooldown[message.command[0]])


@Client.on_message(
    filters.me & filters.command(["sspam", "stkspam", "spamstk", "stickerspam"], prefix)
)
async def spam_stick(client: Client, message: Message):
    if message.reply_to_message and message.reply_to_message.sticker:
        i = 0
        if message.chat.id == BLACKLIST_CHAT:
            return await message.edit("<code>Can't use spam command in there!</code>")
        try:
            times = message.command[1]
        except IndexError:
            return await message.edit("`Give me amount to spam!`")
        if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            for i in range(int(times)):
                await message.delete()
                sticker = message.reply_to_message.sticker.file_id
                await client.send_sticker(
                    message.chat.id,
                    sticker,
                )
                await asyncio.sleep(0.10)
        if message.chat.type == enums.ChatType.PRIVATE:
            for i in range(int(times)):
                await message.delete()
                sticker = message.reply_to_message.sticker.file_id
                await client.send_sticker(message.chat.id, sticker)
                await asyncio.sleep(0.10)
    else:
        return await edit_or_reply(
            message, "**reply to a sticker with amount you want to spam**"
        )


modules_help["spam"] = {
    "spam {total} {text}": "Spam text in chat!!",
    "spamreact {total} {emoji}": "Spam reaction",
    "delayspam {second} {total} {text}": "Sending spam texts with a specified delay!",
    f"sspam or {prefix}stickerspam [reply sticker]": "To spam with sticker"
    "\nNOTE: spam at your own risk!",
}
