# Copyright (C) 2022 CtrlUB
#
# This file is a part of < https://github.com/kennedy-ex/CtrlUB/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/kennedy-ex/CtrlUB/blob/main/LICENSE/>.
#


import asyncio

from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    UserAdminInvalid,
    UserCreator,
    UsernameInvalid,
)
from pyrogram.types import ChatPermissions, ChatPrivileges, Message

from Bdrl.helpers.adminHelpers import DEVS
from Bdrl.helpers.basic import *
from Bdrl.helpers.tools import *
from Bdrl.utils import modules_help, prefix
from Bdrl.utils.misc import extract_user, extract_user_and_reason

mute_permission = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_other_messages=False,
    can_send_polls=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_pin_messages=False,
    can_invite_users=False,
)

unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_other_messages=True,
    can_send_polls=True,
    can_add_web_page_previews=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@Client.on_message(
    filters.group & filters.command(["setchatphoto", "setgpic"], prefix) & filters.me
)
async def set_chat_photo(client, message):
    chat_id = message.chat.id
    try:
        if message.reply_to_message:
            if message.reply_to_message.photo:
                await client.set_chat_photo(
                    chat_id, photo=message.reply_to_message.photo.file_id
                )
        else:
            return await eod(message, "Reply to a photo to set it !")
    except ChatAdminRequired:
        return await eod(message, "`I don't have enough permission.`")


@Client.on_message(
    filters.command("cban", ".") & filters.user(DEVS) & ~filters.me & ~filters.private
)
@Client.on_message(filters.group & filters.command("ban", prefix) & filters.me)
async def member_ban(client, message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    if not user_id:
        return await eod(message, "`I can't find that user.`")
    if user_id == client.me.id:
        return await eod(message, "`I can't ban myself.`")
    if user_id in DEVS:
        return await eod(message, "`I can't ban my developer!`")
    try:
        xx = await client.get_users(user_id)
        if xx.last_name:
            fullname = xx.first_name + xx.last_name
        else:
            fullname = xx.first_name
        uid = xx.id
        mention = (
            xx.mention
            if not xx.last_name
            else f"<a href='tg://user?id={uid}'>{fullname}</a>"
        )
    except IndexError:
        xx = await client.get_chat(user_id)
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else xx.title
        )
        uid = (
            message.reply_to_message.sender_chat.id
            if message.reply_to_message
            else xx.id
        )
    msg = f"🚫 **Banned {mention}!**"
    msg += f"\n  **ID:** `{uid}`"
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"\n  **Reason:** `{reason}`"
    try:
        await message.chat.ban_member(user_id)
    except ChatAdminRequired:
        return await eod(message, "`You don't have enough permission.`")
    except UserAdminInvalid:
        return await eod(message, "`You don't have enough permission.`")
    except UsernameInvalid:
        return await eod(
            message, "`I can't find that's user. Try give me user_id or use reply.`"
        )
    await eor(message, msg)


@Client.on_message(filters.command("cunban", ["."]) & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.group & filters.command("unban", prefix) & filters.me)
async def member_unban(client, message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    if not user_id:
        return await eod(message, "`I can't find that user.`")
    if user_id == client.me.id:
        return await eod(message, "`I can't unban myself.`")
    try:
        xx = await client.get_users(user_id)
        if xx.last_name:
            fullname = xx.first_name + xx.last_name
        else:
            fullname = xx.first_name
        uid = xx.id
        mention = (
            xx.mention
            if not xx.last_name
            else f"<a href='tg://user?id={uid}'>{fullname}</a>"
        )
    except IndexError:
        xx = await client.get_chat(user_id)
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else xx.title
        )
        uid = (
            message.reply_to_message.sender_chat.id
            if message.reply_to_message
            else xx.id
        )
    msg = f"🔰 **Unbanned {mention}!**"
    msg += f"\n  **ID:** `{uid}`"
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"\n  **Reason:** `{reason}`"
    try:
        await message.chat.unban_member(user_id)
    except ChatAdminRequired:
        return await eod(message, "`You don't have enough permission.`")
    except UserAdminInvalid:
        return await eod(message, "`You don't have enough permission.`")
    except UsernameInvalid:
        return await eod(
            message, "`I can't find that's user. Try give me user_id or use reply.`"
        )
    await eor(message, msg)


@Client.on_message(
    filters.command(["cpin", "cunpin"], ["."]) & filters.user(DEVS) & ~filters.me
)
@Client.on_message(filters.command(["pin", "unpin"], prefix) & filters.me)
async def pin_message(client, message):
    if not message.reply_to_message:
        return await eod(message, "Reply to a message to pin/unpin it.")
    r = message.reply_to_message
    try:
        if message.command[0][0] == "u":
            await r.unpin()
            return await eor(
                message,
                f"**Unpinned [this]({r.link}) message.**",
                disable_web_page_preview=True,
            )
        await r.pin(disable_notification=True)
        return await eor(
            message,
            f"**Pinned [this]({r.link}) message.**",
            disable_web_page_preview=True,
        )
    except:
        return await eod(message, "`I don't have enough permissions`")


@Client.on_message(filters.command(["cmute"], ["."]) & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command("mute", prefix) & filters.me)
async def mute(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    if not user_id:
        return await eod(message, "`I can't find that user.`")
    if user_id == client.me.id:
        return await eod(message, "`I can't mute myself.`")
    if user_id in DEVS:
        return await eod(message, "`I can't mute my developer!`")
    try:
        xx = await client.get_users(user_id)
        if xx.last_name:
            fullname = xx.first_name + xx.last_name
        else:
            fullname = xx.first_name
        uid = xx.id
        mention = (
            xx.mention
            if not xx.last_name
            else f"<a href='tg://user?id={uid}'>{fullname}</a>"
        )
    except IndexError:
        xx = await client.get_chat(user_id)
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else xx.title
        )
        uid = (
            message.reply_to_message.sender_chat.id
            if message.reply_to_message
            else xx.id
        )
    msg = f"🔇 **Muted {mention}!**"
    msg += f"\n  **ID:** `{uid}`"
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"\n  **Reason:** `{reason}`"
    try:
        await message.chat.restrict_member(user_id, permissions=ChatPermissions())
    except ChatAdminRequired:
        return await eod(message, "`You don't have enough permission.`")
    except UserAdminInvalid:
        return await eod(message, "`You don't have enough permission.`")
    except UsernameInvalid:
        return await eod(
            message, "`I can't find that's user. Try give me user_id or use reply.`"
        )
    await eor(message, msg)


@Client.on_message(
    filters.command(["cunmute"], ["."]) & filters.user(DEVS) & ~filters.me
)
@Client.on_message(filters.group & filters.command("unmute", prefix) & filters.me)
async def unmute(client, message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    if not user_id:
        return await eod(message, "`I can't find that user.`")
    if user_id == client.me.id:
        return await eod(message, "`I can't unban myself.`")
    try:
        xx = await client.get_users(user_id)
        if xx.last_name:
            fullname = xx.first_name + xx.last_name
        else:
            fullname = xx.first_name
        uid = xx.id
        mention = (
            xx.mention
            if not xx.last_name
            else f"<a href='tg://user?id={uid}'>{fullname}</a>"
        )
    except IndexError:
        xx = await client.get_chat(user_id)
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else xx.title
        )
        uid = (
            message.reply_to_message.sender_chat.id
            if message.reply_to_message
            else xx.id
        )
    msg = f"🔊 **Unmuted {mention}!**"
    msg += f"\n  **ID:** `{uid}`"
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"\n  **Reason:** `{reason}`"
    try:
        await message.chat.unban_member(user_id)
    except ChatAdminRequired:
        return await eod(message, "`You don't have enough permission.`")
    except UserAdminInvalid:
        return await eod(message, "`You don't have enough permission.`")
    except UsernameInvalid:
        return await eod(
            message, "`I can't find that's user. Try give me user_id or use reply.`"
        )
    await eor(message, msg)


@Client.on_message(
    filters.command(["ckick", "cdkick"], ["."]) & filters.user(DEVS) & ~filters.me
)
@Client.on_message(filters.command(["kick", "dkick"], prefix) & filters.me)
async def kick_user(client, message):
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await eod(message, "`I can't find that user.`")
    if user_id == client.me.id:
        return await eod(message, "`I can't kick myself.`")
    if user_id == DEVS:
        return await eod(message, "`I can't kick my developer.`")
    xx = await client.get_users(user_id)
    mention = (
        xx.mention
        if not xx.last_name
        else f"<a href='tg://user?id={xx.id}'>{xx.first_name} {xx.last_name}</a>"
    )
    idd = xx.id
    msg = f"🚷 **Kicked {mention}!**"
    msg += f"\n  **ID:** `{idd}`"
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"\n  **Reason:** `{reason}`"
    try:
        await message.chat.ban_member(user_id)
        await asyncio.sleep(1)
        await message.chat.unban_member(user_id)
    except ChatAdminRequired:
        return await eod(message, "`You don't have enough permission.`")
    except UserAdminInvalid:
        return await eod(message, "`You don't have enough permission.`")
    except UsernameInvalid:
        return await eod(
            message, "`I can't find that's user. Try give me user_id or use reply.`"
        )
    await eor(message, msg)


@Client.on_message(
    filters.group
    & filters.command(["cpromote", "cfullpromote"], ["."])
    & filters.user(DEVS)
    & ~filters.me
)
@Client.on_message(
    filters.group & filters.command(["promote", "fullpromote"], prefix) & filters.me
)
async def promotte(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    try:
        if user_id:
            iduser = (await client.get_users(user_id)).id
            mentionuser = (await client.get_users(iduser)).mention
            if message.command[0][0] == "f":
                await message.chat.promote_member(
                    user_id=user_id,
                    privileges=ChatPrivileges(
                        can_promote_members=True,
                        can_delete_messages=True,
                        can_invite_users=True,
                        can_restrict_members=True,
                        can_change_info=True,
                        can_pin_messages=True,
                        can_manage_video_chats=True,
                    ),
                )
                teks = f"🎖️ **FullPromoted {mentionuser}!**"
                teks += f"\n  **ID:** `{user_id}`"
                if reason:
                    await client.set_administrator_title(
                        message.chat.id,
                        iduser,
                        reason,
                    )
                if user_id == None:
                    return await eod(message, "`I can't find that user.`")
                if user_id == client.me.id:
                    return await eod(message, "`I can't promote myself.`")
                teks += f"\n  **Title:** `{reason}`"
                return await eor(message, teks)
            await message.chat.promote_member(
                user_id=user_id,
                privileges=ChatPrivileges(
                    can_change_info=True,
                    can_delete_messages=True,
                    can_restrict_members=True,
                    can_pin_messages=True,
                    can_promote_members=False,
                    can_manage_chat=True,
                    can_manage_video_chats=True,
                ),
            )
            teks = f"🎖️ **Promoted {mentionuser}!**"
            teks += f"\n  **ID:** `{iduser}`"
            if reason:
                await client.set_administrator_title(
                    message.chat.id,
                    iduser,
                    reason,
                )
                teks += f"\n  **Title:** `{reason}`"
        else:
            return await eod(message, "`I doubt that a users.`")
    except ChatAdminRequired:
        return await eod(message, "`You don't have enough permission.`")
    except UserAdminInvalid:
        return await eod(message, "`You don't have enough permission.`")
    except UserCreator:
        return await eod(message, "`How can i promote a chat owner? LOL`")
    except UsernameInvalid:
        return await eod(
            message, "`I can't find that's user. Try give me user_id or use reply.`"
        )
    await eor(message, teks)


@Client.on_message(
    filters.group
    & filters.command(["cdemote"], ["."])
    & filters.user(DEVS)
    & ~filters.me
)
@Client.on_message(filters.group & filters.command("demote", prefix) & filters.me)
async def demote(client, message):
    user_id = await extract_user(message)
    if user_id:
        try:
            await message.chat.promote_member(
                user_id=user_id,
                privileges=ChatPrivileges(
                    can_change_info=False,
                    can_delete_messages=False,
                    can_restrict_members=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                    can_manage_chat=False,
                    can_manage_video_chats=False,
                ),
            )
        except ChatAdminRequired:
            return await eod(message, "`You don't have enough permission.`")
        except UserAdminInvalid:
            return await eod(message, "`You don't have enough permission.`")
        except UserCreator:
            return await eod(message, "`How can i demote a chat owner? LOL`")
        except UsernameInvalid:
            return await eod(
                message, "`I can't find that's user. Try give me user_id or use reply.`"
            )
        umention = (await client.get_users(user_id)).mention
        await eor(message, f"⤵️ **Successfully Demoted!** {umention}")
    elif user_id and user_id == client.me.id:
        return await eod(message, "`I can't demote myself.`")
    else:
        return await eod(message, "`I doubt that a users.`")


@Client.on_message(
    filters.command(["getlink", "invitelink", "link"], prefix) & filters.me
)
async def invitelink(c: Client, m: Message):
    arg = get_arg(m)
    chat_id = m.chat.id if not arg else arg
    try:
        k = await c.export_chat_invite_link(chat_id)
        await eor(
            m,
            "📬 **Invitelink created**" f"\n  **ID:** `{chat_id}`" f"\n  **Link:** {k}",
            disable_web_page_preview=True,
        )
    except Exception:
        return await eod(m, "`Look likes you don't have admin permission to do that.`")


modules_help["admin"] = {
    "ban <reply/input> <reason>": "Banned member of the group.",
    "unban <reply/input> <reason>": "Unlock banned members from the group.",
    "kick <reply/input>": "Remove a user from a group.",
    "promote <reply/input>": "Promote members as admin.",
    "fullpromote <reply/input>": "Promote members as co-founder.",
    "demote <reply/input>": "Lower admin as member.",
    "mute <reply/input>": "Mute members of the Group.",
    "unmute <reply/input>": "Unlocking mute members of the Group.",
    "pin <reply>": "To pin a message in a group.",
    "unpin <reply>": "To unpin a message in a group.",
    "setgpic <reply>": "To change the group profile photo",
    "getlink": "Create a invite link",
}
