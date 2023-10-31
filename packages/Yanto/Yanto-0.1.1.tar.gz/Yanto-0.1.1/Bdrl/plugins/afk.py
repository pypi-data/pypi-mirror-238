# Copyright (C) 2022 CtrlUB
#
# This file is a part of < https://github.com/kennedy-ex/CtrlUB/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/kennedy-ex/CtrlUB/blob/main/LICENSE/>.
#


import asyncio
import time

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from Bdrl.config import BOTLOG_CHATID
from Bdrl.helpers.msg_types import get_message_type
from Bdrl.helpers.parser import escape_markdown, mention_markdown
from Bdrl.helpers.sql.afk_sql import get_afk, set_afk
from Bdrl.helpers.tools import eod
from Bdrl.utils import modules_help, prefix

# Set priority to 11 and 12


MENTIONED = []
AFK_RESTIRECT = {}
DELAY_TIME = 3  # seconds


@Client.on_message(filters.me & filters.command("afk", prefix))
async def afk(client: Client, message: Message):
    if len(message.text.split()) >= 2:
        set_afk(True, message.text.split(None, 1)[1])
        await eod(
            message,
            "{} <b>go AFK!</b>\n<b>reason:</b> <code>{}</code>".format(
                mention_markdown(message.from_user.id, message.from_user.first_name),
                message.text.split(None, 1)[1],
            ),
            time=7,
        )
    else:
        set_afk(True, "")
        await eod(
            message,
            "{} <b>has been AFK</b>".format(
                mention_markdown(message.from_user.id, message.from_user.first_name)
            ),
            time=7,
        )
    await message.stop_propagation()


@Client.on_message(filters.mentioned & ~filters.bot, group=11)
async def afk_mentioned(client: Client, message: Message):
    global MENTIONED
    get = get_afk()
    if get and get["afk"]:
        if "-" in str(message.chat.id):
            cid = str(message.chat.id)[4:]
        else:
            cid = str(message.chat.id)
        if cid in list(AFK_RESTIRECT):
            if int(AFK_RESTIRECT[cid]) >= int(time.time()):
                return
        AFK_RESTIRECT[cid] = int(time.time()) + DELAY_TIME
        if get["reason"]:
            await message.reply(
                "{} <b>is AFK!</b>\n<b>reason:</b> <code>{}</code>".format(
                    client.me.mention, get["reason"]
                )
            )
        else:
            await message.reply(f"<b>Sorry</b> {client.me.first_name} <b>is AFK!</b>")
        _, message_type = get_message_type(message)
        if message_type == enums.MessagesFilter.TEXT:
            if message.text:
                text = message.text
            else:
                text = message.caption
        else:
            text = message_type.name
        MENTIONED.append(
            {
                "user": message.from_user.first_name,
                "user_id": message.from_user.id,
                "chat": message.chat.title,
                "chat_id": cid,
                "text": text,
                "message_id": message.message_id,
            }
        )
        await client.send_message(
            BOTLOG_CHATID,
            "<b>#MENTION\n • From :</b> {}\n • <b>Group :</b> {} <code>[{}]</code>\n • <b>Messages :</b> <code>{}</code>".format(
                message.from_user.mention,
                message.chat.title,
                message.chat.id,
                text[:3500],
            ),
        )


@Client.on_message(filters.me & filters.group, group=12)
async def no_longer_afk(client: Client, message: Message):
    global MENTIONED
    get = get_afk()
    if get and get["afk"]:
        k = await client.send_message(message.chat.id, "I am back from AFK!")
        set_afk(False, "")
        await asyncio.sleep(5)
        await k.delete()
        text = "<b>Total {} Mention from being AFK</b>\n".format(len(MENTIONED))
        for x in MENTIONED:
            msg_text = x["text"]
            if len(msg_text) >= 11:
                msg_text = "{}...".format(x["text"])
            text += "- [{}](https://t.me/c/{}/{}) ({}): {}\n".format(
                escape_markdown(x["user"]),
                x["chat_id"],
                x["message.id"],
                x["chat"],
                msg_text,
            )
        await client.send_message(BOTLOG_CHATID, text)
        MENTIONED = []


modules_help["afk"] = {
    "afk <reason>": "Notify the person who tagged or replied to one of your messages or dm's when you're afk",
}
