# Copyright (C) 2022 CtrlUB
#
# This file is a part of < https://github.com/kennedy-ex/CtrlUB/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/kennedy-ex/CtrlUB/blob/main/LICENSE/>.
#

import requests
from pyrogram import Client, filters
from pyrogram.types import Message

from Bdrl.helpers.basic import edit_or_reply
from Bdrl.helpers.tools import get_arg
from Bdrl.utils import *

OPENAI = "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"


@Client.on_message(filters.command("create", prefix) & filters.me)
async def create(client: Client, message: Message):
    if len(message.command) < 3:
        return await edit_or_reply(
            message, f"**Type** `{prefix}help create` if you don't know how to use this"
        )
    group_type = message.command[1]
    split = message.command[2:]
    group_name = " ".join(split)
    ok = await edit_or_reply(message, "`Processing...`")
    desc = "Welcome To My " + ("Group" if group_type == "gc" else "Channel")
    if group_type == "gc" or group_type == "group":  # for supergroup
        _id = await client.create_supergroup(group_name, desc)
        link = await client.get_chat(_id.id)
        await ok.edit(
            f"""
**Create Group Chat:**
   **{group_name}**
      **ID**: `{link.id}`
      **Link:** {link.invite_link}
""",
            disable_web_page_preview=True,
        )
    elif group_type == "ch" or group_type == "channel":  # for channel
        _id = await client.create_channel(group_name, desc)
        link = await client.get_chat(_id.id)
        await ok.edit(
            f"""
**Create Channel:**
   **{group_name}**
      **ID**: `{link.id}`
      **Link:** {link.invite_link}
""",
            disable_web_page_preview=True,
        )
    else:
        return await ok.edit(
            "**Invalid type,** available type is [`group`, `channel`] only"
        )


@Client.on_message(filters.command("ai", prefix) & filters.me)
async def ask_openai(client, message):
    anu = get_arg(message)
    if not anu:
        return await message.reply("contoh : .ai What is love")
    afah = await message.reply("wait...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI}",
    }
    json_data = {
        "model": "text-davinci-003",
        "prompt": anu,
        "max_tokens": 200,
        "temperature": 0,
    }
    response = requests.post(
        "https://api.openai.com/v1/completions", headers=headers, json=json_data
    ).json()

    await afah.edit(response["choices"][0]["text"])


modules_help["create"] = {
    "create ch": "Create a channel telegram.",
    "create gc": "Create a group telegram.",
}
modules_help["openai"] = {
    "ai": "Ask ai bot.",
}
