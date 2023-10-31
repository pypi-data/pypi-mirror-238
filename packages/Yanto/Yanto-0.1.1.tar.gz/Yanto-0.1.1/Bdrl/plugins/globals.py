# Copyright (C) 2022 CtrlUB
#
# This file is a part of < https://github.com/kennedy-ex/CtrlUB/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/kennedy-ex/CtrlUB/blob/main/LICENSE/>.
#


from pyrogram import Client, errors, filters
from pyrogram.types import ChatPermissions, Message

from Bdrl import *
from Bdrl.helpers.adminHelpers import DEVS
from Bdrl.helpers.basic import eor
from Bdrl.helpers.PyroHelpers import get_ub_chats
from Bdrl.helpers.tools import eod
from Bdrl.utils import extract_user, extract_user_and_reason, modules_help, prefix


def globals_init():
    try:
        global sql, sql2
        from importlib import import_module

        sql = import_module("Bdrl.helpers.sql.gban_sql")
        sql2 = import_module("Bdrl.helpers.sql.gmute_sql")
    except Exception as e:
        sql = None
        sql2 = None
        LOGS.warn("Unable to run GBan and GMute command, no SQL connection found")
        raise e


globals_init()


@Client.on_message(
    filters.command("cgban", ["^", "."]) & filters.user(DEVS) & ~filters.via_bot
)
@Client.on_message(filters.command("gban", prefix) & filters.me)
async def gban_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    await eor(message, "`Gbanning...`")
    if not user_id:
        return await eod(message, "`I can't find that user.`")
    if user_id == client.me.id:
        return await eod(message, "`I can't gban myself.`")
    if user_id in DEVS:
        return await eod(message, "`I can't gban my developer!`")
    if user_id:
        try:
            user = await client.get_users(user_id)
        except Exception:
            return await eod(message, "`Please specify a valid user!`")
    if sql.is_gbanned(user.id):
        return await eod(
            message,
            f"[This user](tg://user?id={user.id}) **it's already on the gbanned list**",
        )
    f_chats = await get_ub_chats(client)
    if not f_chats:
        return await eod(message, "**You don't have a Group that you admin**")
    er = 0
    done = 0
    for gokid in f_chats:
        try:
            await client.ban_chat_member(chat_id=gokid, user_id=int(user.id))
            done += 1
        except BaseException:
            er += 1
    sql.gban(user.id)
    msg = (
        r"**\\#GBanned_User//**"
        f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})"
        f"\n**User ID:** `{user.id}`"
    )
    if reason:
        msg += f"\n**Reason:** `{reason}`"
    msg += f"\n**Affected To:** `{done}` **Chats**"
    await message.edit(msg)


@Client.on_message(
    filters.command("cungban", [".", "^"]) & filters.user(DEVS) & ~filters.via_bot
)
@Client.on_message(filters.command("ungban", prefix) & filters.me)
async def ungban_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    await eor(message, "`UnGbanning...`")
    if not user_id:
        return await eod(message, "`I can't find that user.`")
    if user_id == client.me.id:
        return await eod(message, "`I can't gban myself.`")
    if user_id in DEVS:
        return await eod(message, "`I can't gban my developer!`")
    if user_id:
        try:
            user = await client.get_users(user_id)
        except Exception:
            return await ok.edit("`Please specify a valid user!`")
    try:
        if not sql.is_gbanned(user.id):
            return await ok.edit("`User already ungban`")
        ung_chats = await get_ub_chats(client)
        if not ung_chats:
            return await eod(message, "**You don't have a Group that you admin**")
        er = 0
        done = 0
        for good_boi in ung_chats:
            try:
                await client.unban_chat_member(chat_id=good_boi, user_id=user.id)
                done += 1
            except BaseException:
                er += 1
        sql.ungban(user.id)
        msg = (
            r"**\\#UnGbanned_User//**"
            f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})"
            f"\n**User ID:** `{user.id}`"
        )
        if reason:
            msg += f"\n**Reason:** `{reason}`"
        msg += f"\n**Affected To:** `{done}` **Chats**"
        await message.edit(msg)
    except Exception as e:
        await eod(message, f"**ERROR:** `{e}`")
        return


@Client.on_message(filters.command("listgban", prefix) & filters.me)
async def gbanlist(client: Client, message: Message):
    users = sql.gbanned_users()
    if not users:
        return await eod(message, "`The Gbanlist is empty!`")
    gban_list = "**GBanned Users:**\n"
    count = 0
    for i in users:
        count += 1
        gban_list += f"**{count} -** `{i.sender}`\n"
    return await message.edit(gban_list)


@Client.on_message(filters.command("cgmute", ".") & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command("gmute", prefix) & filters.me)
async def gmute_user(client: Client, message: Message):
    args = await extract_user(message)
    reply = message.reply_to_message
    await eor(message, "`Processing...`")
    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            await eod(message, f"`Please specify a valid user!`")
            return
    elif reply:
        user_id = reply.from_user.id
        user = await client.get_users(user_id)
    else:
        await eod(message, f"`Please specify a valid user!`")
        return
    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return await eod(message, "`Calm down anybob, you can't gmute yourself.`")
    except BaseException:
        pass
    try:
        if sql2.is_gmuted(user.id):
            return await eod(message, "`User already gmuted`")
        sql2.gmute(user.id)
        await message.edit(
            f"[{user.first_name}](tg://user?id={user.id}) globally gmuted!"
        )
        try:
            common_chats = await client.get_common_chats(user.id)
            for i in common_chats:
                await i.restrict_member(user.id, ChatPermissions())
        except BaseException:
            pass
    except Exception as e:
        await eod(message, f"**ERROR:** `{e}`", time=30)
        return


@Client.on_message(filters.command("cugmute", ".") & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command("ungmute", prefix) & filters.me)
async def ungmute_user(client: Client, message: Message):
    args = await extract_user(message)
    reply = message.reply_to_message
    await eor(message, "`Processing...`")
    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            await ok.edit(f"`Please specify a valid user!`")
            return
    elif reply:
        user_id = reply.from_user.id
        user = await client.get_users(user_id)
    else:
        await eod(message, f"`Please specify a valid user!`")
        return
    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return await eod(message, "`Calm down anybob, you can't ungmute yourself.`")
    except BaseException:
        pass
    try:
        if not sql2.is_gmuted(user.id):
            return await eod(message, "`User already ungmuted`")
        sql2.ungmute(user.id)
        try:
            common_chats = await client.get_common_chats(user.id)
            for i in common_chats:
                await i.unban_member(user.id)
        except BaseException:
            pass
        await message.edit(
            f"[{user.first_name}](tg://user?id={user.id}) globally ungmuted!"
        )
    except Exception as e:
        await eod(message, f"**ERROR:** `{e}`", time=30)
        return


@Client.on_message(filters.command("listgmute", prefix) & filters.me)
async def gmutelist(client: Client, message: Message):
    users = sql2.gmuted_users()
    ok = await eor(message, "`Processing...`")
    if not users:
        return await eod(message, "`Gmutelist empty`")
    gmute_list = "**GMuted Users:**\n"
    count = 0
    for i in users:
        count += 1
        gmute_list += f"**{count} -** `{i.sender}`\n"
    return await ok.edit(gmute_list)


@Client.on_message(filters.incoming & filters.group)
async def globals_check(client: Client, message: Message):
    if not message:
        return
    if not message.from_user:
        return
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not user_id:
        return
    if sql.is_gbanned(user_id):
        try:
            await client.ban_chat_member(chat_id, user_id)
        except BaseException:
            pass
    if sql2.is_gmuted(user_id):
        try:
            await message.delete()
        except errors.RPCError:
            pass
        try:
            await client.restrict_chat_member(chat_id, user_id, ChatPermissions())
        except BaseException:
            pass
    message.continue_propagation()


modules_help["globals"] = {
    "gban <reply/username/userid>": "Doing Global Banned To All Groups Where You As Admin.",
    "ungban <reply/username/userid>": "Canceling Global Banned.",
    "listgban": "Get List Global Banned.",
    "gmute <reply/username/userid>": "Doing Global muted To All Groups Where You As Admin.",
    "ungmute <reply/username/userid>": "Canceling Global Muted.",
    "listgmute": "Get List Global Muted.",
}
