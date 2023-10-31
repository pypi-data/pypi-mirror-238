# Copyright (C) 2022 CtrlUB
#
# This file is a part of < https://github.com/kennedy-ex/CtrlUB/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/kennedy-ex/CtrlUB/blob/main/LICENSE/>.
#


from pyrogram import Client, filters
from pyrogram.types import *

from Bdrl.helpers.basic import edit_or_reply
from Bdrl.helpers.tools import get_arg
from Bdrl.utils import *

flood = {}


@Client.on_message(filters.command(["block"], prefix) & filters.me)
async def block_user_func(client: Client, message: Message):
    meki = get_arg(message)
    rep = message.reply_to_message
    if not rep:
        user_id = (await client.get_users(meki)).id
    else:
        user_id = message.reply_to_message.from_user.id
    if not rep and not meki:
        return await message.edit("`I can't don't that's user!`")
    try:
        await edit_or_reply(message, f"Successfully blocked [`{user_id}`]")
        await client.block_user(user_id)
    except Exception as k:
        return await message.edit(f"ERROR\n`{k}`")


@Client.on_message(filters.command(["unblock"], prefix) & filters.me)
async def unblock_user_func(client, message):
    meki = get_arg(message)
    rep = message.reply_to_message
    if not rep:
        user_id = (await client.get_users(meki)).id
    else:
        user_id = message.reply_to_message.from_user.id
    if not rep and not meki:
        return await message.edit("`I Can't find that user!`")
    try:
        await edit_or_reply(message, f"Successfully unblocked [`{user_id}`]")
        await client.unblock_user(user_id)
    except Exception as k:
        return await message.edit(f"ERROR\n`{k}`")


@Client.on_message(filters.command(["setpfp"], prefix) & filters.me)
async def set_pfp(client, message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await edit_or_reply(message, "Reply to a photo.")
    photo = await message.reply_to_message.download()
    ok = await edit_or_reply(message, "`Processing...`")
    try:
        await client.set_profile_photo(photo=photo)
        await ok.edit("Successfully Changed PFP.")
    except Exception as e:
        await ok.edit(f"**ERROR:** `{e}`")


@Client.on_message(filters.command(["bio"], prefix) & filters.me)
async def set_bio(client, message):
    ok = await edit_or_reply(message, "`Processing...`")
    if len(message.command) == 1:
        return await ok.edit("Give some text to set as bio.")
    elif len(message.command) > 1:
        bio = message.text.split(None, 1)[1]
        try:
            await client.update_profile(bio=bio)
            await ok.edit("Changed Bio.")
        except Exception as e:
            await ok.edit(f"**ERROR:** `{e}`")
    else:
        return await ok.edit("Give some text to set as bio.")


@Client.on_message(filters.command(["setname"], prefix) & filters.me)
async def setname(client, message):
    ok = await edit_or_reply(message, "`Processing...`")
    if len(message.command) == 1:
        return await ok.edit("Give some text to set as nickname.")
    elif len(message.command) > 1:
        name = message.text.split(None, 1)[1]
        try:
            await client.update_profile(first_name=name)
            await ok.edit("Changed Bio.")
        except Exception as e:
            await ok.edit(f"**ERROR:** `{e}`")
    else:
        return await ok.edit("Give some text to set as nickname.")


modules_help["profile"] = {
    "bio": "Set your Bio Message.",
    "setname": "Set your nickname",
    "setpfp": "Reply to any photo to set as pfp.",
}
