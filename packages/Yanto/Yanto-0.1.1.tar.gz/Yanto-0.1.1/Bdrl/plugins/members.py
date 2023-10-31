# Copyright (C) 2022 CtrlUB
#
# This file is a part of < https://github.com/kennedy-ex/CtrlUB/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/kennedy-ex/CtrlUB-Userbot/blob/main/LICENSE/>.
#


import asyncio

from pyrogram import Client, enums, filters
from pyrogram.errors import FloodWait, UserAlreadyParticipant, UserPrivacyRestricted
from pyrogram.types import Message

from Bdrl.config import BLACKLIST_CHAT, BOTLOG_CHATID
from Bdrl.helpers.basic import edit_or_reply
from Bdrl.helpers.tools import edit_delete, get_arg
from Bdrl.utils import *


@Client.on_message(filters.command("join", prefix) & filters.me)
async def join(client: Client, message: Message):
    ok = message.command[1] if len(message.command) > 1 else message.chat.id
    xxnx = await edit_or_reply(message, "`Processing...`")
    try:
        await xxnx.edit(f"Joined to [`{ok}`]")
        await client.join_chat(ok)
    except Exception as ex:
        await xxnx.edit(f"**ERROR:** \n\n`{str(ex)}`")


@Client.on_message(
    filters.command(["leave", "kickme"], prefix) & filters.me & ~filters.private
)
async def leave(client: Client, message: Message):
    ok = message.command[1] if len(message.command) > 1 else message.chat.id
    xxnx = await edit_or_reply(message, "`Processing...`")
    if message.chat.id in BLACKLIST_CHAT:
        return await edit_delete(message, "`This command is forbidden in this chat.`")
    try:
        await xxnx.edit_text(f"`I left this group, bye!!`")
        await client.leave_chat(ok)
    except Exception as ex:
        await edit_delete(message, f"**ERROR:** \n\n`{str(ex)}`")


@Client.on_message(filters.command(["gleaveall"], prefix) & filters.me)
async def kickmeall(client: Client, message: Message):
    ok = await edit_or_reply(message, "`Global Leave from group chats...`")
    er = 0
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            chat = dialog.chat.id
            try:
                done += 1
                await client.leave_chat(chat)
            except BaseException:
                er += 1
    await ok.edit(
        f"**Successfully Exit from `{done}` Group, Failed to Leave `{er}` Group**"
    )


@Client.on_message(filters.command(["chleaveall"], prefix) & filters.me)
async def chleaveall(client: Client, message: Message):
    ok = await edit_or_reply(message, "`Global Leave from group chats...`")
    er = 0
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.CHANNEL):
            chat = dialog.chat.id
            try:
                done += 1
                await client.leave_chat(chat)
            except BaseException:
                er += 1
    await ok.edit(
        f"**Successfully Exit from `{done}` Channel, Failed to Leave `{er}` Channel**"
    )


@Client.on_message(filters.command("invite", prefix) & filters.me & ~filters.private)
async def invite(client, message):
    reply = message.reply_to_message
    if reply:
        user = reply.from_user.id
    else:
        user = get_arg(message)
        if not user:
            await message.edit("`Who i should invite?`")
            return
    get_user = await client.get_users(user)
    try:
        await client.add_chat_members(message.chat.id, get_user.id)
        await message.edit(f"`{get_user.first_name}` Added to this group.")
    except Exception as e:
        await message.edit(f"{e}")


@Client.on_message(filters.command("inviteall", prefix) & filters.me & ~filters.private)
async def inviteall(client: Client, message: Message):
    text = get_arg(message)
    if text:
        await message.edit_text(f"`Processing...`")
    else:
        return await message.edit_text(f"`Give me username or id of group`")
    chat = await client.get_chat(text)
    om = 0
    am = 0
    usn = f"@{chat.username}" if chat.username else f"`{chat.id}`"
    k = await message.edit(f"📩 **Adding member from** [{usn}]")
    async for member in client.get_chat_members(chat.id):
        user = member.user
        stats = [
            enums.UserStatus.ONLINE,
            enums.UserStatus.OFFLINE,
            enums.UserStatus.RECENTLY,
            enums.UserStatus.LAST_WEEK,
        ]
        if user.status in stats:
            try:
                await client.add_chat_members(
                    message.chat.id, user.id, forward_limit=60
                )
                om += 1
                await asyncio.sleep(1.5)
            except UserAlreadyParticipant:
                pass
            except UserPrivacyRestricted:
                am += 1
            except FloodWait as e:
                mg = await client.send_message(BOTLOG_CHATID, f"error- `{e}`")
                am += 1
                await asyncio.sleep(0.3)
                await mg.delete()
    await k.edit(f"📩 **Inviteall Members:**\n\n**Succes:** `{om}`\n**Failed:** `{am}`")


@Client.on_message(filters.command("zombies", prefix) & filters.me & ~filters.private)
async def zombies(client, message):
    kk = get_arg(message)
    chat = message.chat.id
    ok = 0
    sip = 0
    if kk and kk == "clean":
        await message.edit("🗑️ `Starting cleaning this group...`")
        async for ah in client.get_chat_members(chat):
            if ah.user.is_deleted:
                try:
                    await client.ban_chat_member(chat, ah.user.id)
                    ok += 1
                except Exception:
                    sip += 1
            if ok < 1:
                msg = "`Group clean, deleted account not found.`"
            else:
                msg = f"🚷 **Kicked** `{ok}` **deleted account.**"
            if sip > 0:
                msg += f"\n • **Failed kick:** `{sip}`"
        await message.edit(msg)
    else:
        await message.edit("`Searching deleted account...`")
        async for klayen in client.get_chat_members(chat):
            if klayen.user.is_deleted:
                ok += 1
            if ok < 1:
                msg = "`Group clean, deleted account not found.`"
            else:
                msg = f"👻 **Found** `{ok}` **deleted account. Use** `{prefix}zombies clean` **to kick that all.**"
        await message.edit(msg)


modules_help["members"] = {
    "invite [username/user_id]": "To invite a user or bot to the chat.",
    "inviteall [chat_username/chat_id]": "To inviting multiple member from chat you want.",
    "zombies": "To checks chat have deleted account member or not.",
    "leave or kickme": "Leave from a group",
    "join [id/username group]": "For joining to a chat",
    "gleaveall": "For leave all yours group",
    "chleaveall": "Leave from all channel you joined",
}
