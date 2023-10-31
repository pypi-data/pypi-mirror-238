# Copyright (C) 2022 CtrlUB
#
# This file is a part of < https://github.com/kennedy-ex/CtrlUB/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/kennedy-ex/CtrlUB-Userbot/blob/main/LICENSE/>.
#

import asyncio

import dotenv
from pyrogram import Client, enums, filters
from pyrogram.types import Message

from Bdrl.config import BLACKLIST_CHAT, BLACKLIST_GCAST
from Bdrl.helpers.basic import edit_or_reply
from Bdrl.helpers.misc import HAPP, in_heroku
from Bdrl.helpers.tools import eod, get_arg
from Bdrl.utils import modules_help, prefix
from Bdrl.utils.misc import restart


@Client.on_message(filters.command("gcast", prefix) & filters.me)
async def gcast(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        await message.edit("`Globally Broadcasting . . .`")
    else:
        return await eod(
            message, "`Reply to a message or give a text to broadcast it!`"
        )
    sent = 0
    failed = 0
    async for dialog in client.get_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [
            enums.ChatType.GROUP,
            enums.ChatType.SUPERGROUP,
        ]:
            if message.reply_to_message:
                msg = message.reply_to_message
            elif get_arg:
                msg = get_arg(message)
            chat = dialog.chat.id
            if chat not in BLACKLIST_CHAT and chat not in BLACKLIST_GCAST:
                try:
                    if message.reply_to_message:
                        await msg.copy(chat)
                    elif get_arg:
                        await client.send_message(chat, msg)
                    sent += 1
                    await asyncio.sleep(0.1)
                except:
                    failed += 1
                    await asyncio.sleep(0.1)
    await message.edit_text(
        f"Broadcast done in `{sent}` chats, error in `{failed}` chat(s)"
    )


@Client.on_message(filters.command("gucast", prefix) & filters.me)
async def gucast(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        await message.edit("`Globally Broadcasting . . .`")
    else:
        return await eod(
            message, "`Reply to a message or give a text to broadcast it!`"
        )
    sent = 0
    failed = 0
    async for dialog in client.get_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [
            enums.ChatType.PRIVATE,
        ]:
            if message.reply_to_message:
                msg = message.reply_to_message
            elif get_arg:
                msg = get_arg(message)
            chat = dialog.chat.id
            try:
                if message.reply_to_message:
                    await msg.copy(chat)
                elif get_arg:
                    await client.send_message(chat, msg)
                sent += 1
                await asyncio.sleep(0.1)
            except:
                failed += 1
                await asyncio.sleep(0.1)
    await message.edit_text(
        f"Broadcast done in `{sent}` users, error in `{failed}` user(s)"
    )


@Client.on_message(filters.command("blchat", prefix) & filters.me)
async def blchatgcast(client: Client, message: Message):
    blacklistgc = "True" if BLACKLIST_GCAST else "False"

    list = blchat.replace(" ", "\n» ")
    if blacklistgc == "True":
        await edit_or_reply(
            message,
            f"🔮 Blacklist Gcast: Enabled\n\n📚 Blacklist Group:\n» {list}\n\nKetik {prefix}addblacklist di grup yang ingin anda tambahkan ke daftar blacklist gcast.",
        )
    else:
        await edit_or_reply(message, "🔮 Blacklist Gcast: Disabled")


@Client.on_message(filters.command("addblacklist", prefix) & filters.me)
async def addblacklist(client: Client, message: Message):
    yanto = await edit_or_reply(message, "Processing...")
    if HAPP is None:
        return await yanto.edit(
            "Silahkan Tambahkan Var HEROKU_APP_NAME untuk menambahkan blacklist",
        )
    blgc = f"{BLACKLIST_GCAST} {message.chat.id}"
    blacklistgrup = (
        blgc.replace("{", "")
        .replace("}", "")
        .replace(",", "")
        .replace("[", "")
        .replace("]", "")
        .replace("set() ", "")
    )
    await yanto.edit(
        f"Berhasil Menambahkan {message.chat.id} ke daftar blacklist gcast.\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan."
    )
    if await in_heroku():
        heroku_var = HAPP.config()
        heroku_var["BLACKLIST_GCAST"] = blacklistgrup
    else:
        path = dotenv.find_dotenv("config.env")
        dotenv.set_key(path, "BLACKLIST_GCAST", blacklistgrup)
    restart()


@Client.on_message(filters.command("delblacklist", prefix) & filters.me)
async def delblacklist(client: Client, message: Message):
    yanto = await edit_or_reply(message, "Processing...")
    if HAPP is None:
        return await yanto.edit(
            "Silahkan Tambahkan Var HEROKU_APP_NAME untuk menambahkan blacklist",
        )
    gett = str(message.chat.id)
    if gett in blchat:
        blacklistgrup = blchat.replace(gett, "")
        await yanto.edit(
            f"Berhasil Menghapus {message.chat.id} dari daftar blacklist gcast.\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan."
        )
        if await in_heroku():
            heroku_var = HAPP.config()
            heroku_var["BLACKLIST_GCAST"] = blacklistgrup
        else:
            path = dotenv.find_dotenv("config.env")
            dotenv.set_key(path, "BLACKLIST_GCAST", blacklistgrup)
        restart()
    else:
        await yanto.edit("Grup ini tidak ada dalam daftar blacklist gcast.")


modules_help["broadcast"] = {
    "gcast [input/reply]": "To broadcasting a message to your all groups",
    "gucast [input/reply]": "To broadcasting a message to users you have text with them.",
    "addblacklist [input/replay]": "To Add the group to the gcast blacklist",
    "delblacklist [input/replay]": f"To remove the group from the gcast blacklist.\n\n • Note: Type the command {prefix}addblacklist and {prefix}delblacklist in the group you are blacklisting",
}
