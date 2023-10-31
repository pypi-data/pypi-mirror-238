# Copyright (C) 2022 by mrismanaziz@Github, < https://github.com/mrismanaziz >.
#
# This file is part of < https://github.com/mrismanaziz/Pyroman > project,
# and is released under the "GNU Affero v3.0 License Agreement".
# Please see < https://github.com/mrismanaziz/PyroMan/blob/main/LICENSE >
#
# Recode by kennedy-ex@Github.com/kennedy-ex/CtrlUB
# All rights reserved.


import asyncio

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from Bdrl.config import BOTLOG_CHATID
from Bdrl.helpers.sql import no_log_pms_sql
from Bdrl.helpers.sql.globals import addgvar, gvarstatus
from Bdrl.helpers.tools import eod, get_arg
from Bdrl.utils import *


class LOG_CHATS:
    def __init__(self):
        self.RECENT_USER = None
        self.NEWPM = None
        self.COUNT = 0


LOG_CHATS_ = LOG_CHATS()


@Client.on_message(
    filters.private & filters.incoming & ~filters.service & ~filters.me & ~filters.bot
)
async def monito_p_m_s(client: Client, message: Message):
    if not message.from_user.last_name:
        mention = f"{message.from_user.mention}"
    else:
        mention = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name} {message.from_user.last_name}</a>"
    if BOTLOG_CHATID == -100:
        return
    if gvarstatus("PM_LOGGER") and gvarstatus("PM_LOGGER") == "off":
        return
    if not no_log_pms_sql.is_approved(message.chat.id) and message.chat.id != 777000:
        if LOG_CHATS_.RECENT_USER != message.chat.id:
            LOG_CHATS_.RECENT_USER = message.chat.id
            if LOG_CHATS_.NEWPM:
                await LOG_CHATS_.NEWPM.edit(
                    LOG_CHATS_.NEWPM.text.replace(
                        "**💌 #NEW_MESSAGE**",
                        f" • `{LOG_CHATS_.COUNT}` **Messages**",
                    )
                )
                LOG_CHATS_.COUNT = 0
            LOG_CHATS_.NEWPM = await client.send_message(
                BOTLOG_CHATID,
                f"💌 <b>#FORWARDING #NEW_MESSAGES</b>\n<b> • From :</b> {mention}\n<b> • User ID :</b> <code>{message.from_user.id}</code>",
            )
        try:
            async for pmlog in client.search_messages(message.chat.id, limit=1):
                await pmlog.forward(BOTLOG_CHATID)
            LOG_CHATS_.COUNT += 1
        except BaseException:
            pass


@Client.on_message(filters.group & filters.mentioned & filters.incoming)
async def log_tagged_messages(client: Client, message: Message):
    if not message.from_user.last_name:
        mention = f"{message.from_user.mention}"
    else:
        mention = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name} {message.from_user.last_name}</a>"
    if BOTLOG_CHATID == -100:
        return
    if gvarstatus("GROUP_LOGGER") and gvarstatus("GROUP_LOGGER") == "off":
        return
    if (no_log_pms_sql.is_approved(message.chat.id)) or (BOTLOG_CHATID == -100):
        return
    result = "<b>📨 #TAGS #MESSAGE</b>"
    result += f"\n<b> • 👤 Dari : </b>{mention}"
    result += f"\n<b> • 👥 Group : </b>{message.chat.title}"
    result += f"\n<b> • 👀 </b><a href = '{message.link}'>See Messages</a>"
    await asyncio.sleep(0.3)
    await client.send_message(
        BOTLOG_CHATID,
        result,
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )


@Client.on_message(filters.command("log", prefix) & filters.me)
async def set_log_p_m(client: Client, message: Message):
    if BOTLOG_CHATID != -100:
        if no_log_pms_sql.is_approved(message.chat.id):
            no_log_pms_sql.disapprove(message.chat.id)
            await message.edit("**Log in this chat is activated!**")


@Client.on_message(filters.command("nolog", prefix) & filters.me)
async def set_no_log_p_m(client: Client, message: Message):
    if BOTLOG_CHATID != -100:
        if not no_log_pms_sql.is_approved(message.chat.id):
            no_log_pms_sql.approve(message.chat.id)
            await message.edit("**Log from this group is deactivated!**")


@Client.on_message(filters.command(["pmlog", "pmlogger"], prefix) & filters.me)
async def pmlogger(c: Client, m: Message):
    if BOTLOG_CHATID == -100:
        return await eod(
            m,
            "**For using this feature, you must set** `BOTLOG_CHATID` **in Config.**",
            time=30,
        )
    toggle = get_arg(m)
    if not toggle:
        return await eod(m, "I only understand `on` or `off` only...")
    if toggle == "off" or toggle == "OFF":
        k = toggle.replace(toggle, "off")
        addgvar("PM_LOGGER", k)
        await m.edit("☑️ **PM LOGGER** has been truned `off`")
    elif toggle == "on" or toggle == "ON":
        k = toggle.replace(toggle, "on")
        addgvar("PM_LOGGER", k)
        await m.edit("✅ **PM LOGGER** has been turned `on`")
    else:
        await eod(m, "`I only understard {on} or {off} only!`")


@Client.on_message(
    filters.command(["gruplog", "grouplog", "gclog"], prefix) & filters.me
)
async def group_logger(c: Client, m: Message):
    if BOTLOG_CHATID == -100:
        return await eod(
            m,
            "**For using this feature, you must set** `BOTLOG_CHATID` **in Config.**",
            time=30,
        )
    toggle = get_arg(m)
    if not toggle:
        return await eod(m, "I only understand `on` or `off` only...")
    if toggle == "off" or toggle == "OFF":
        k = toggle.replace(toggle, "off")
        addgvar("GROUP_LOGGER", k)
        await m.edit("☑️ **GROUP LOGGER** has been turned `off`")
    elif toggle == "on" or toggle == "ON":
        k = toggle.replace(toggle, "on")
        addgvar("GROUP_LOGGER", k)
        await m.edit("✅ **GROUP LOGGER** has been turned `on`")
    else:
        await eod(m, "`I only understand {on} or {off} only!`")


modules_help["logger"] = {
    "pmlog": "Logger if a user pm you, you can see message without open pm.",
    "gruplog": "Logger if a user mentioned you in a group.",
}
