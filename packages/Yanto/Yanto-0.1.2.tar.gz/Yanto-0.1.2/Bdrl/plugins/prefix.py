#
# Copyright (C) 2022 by kennedy-ez@Github, < https://github.com/kennedy-ex >.
#
# This file is part of < https://github.com/kennedy-ex/CtrlUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/kennedy-ex/CtrlUB/blob/main/LICENSE >
#
# All rights reserved.


from pyrogram import Client, filters
from pyrogram.types import Message

from Bdrl.helpers.sql.globals import addgvar
from Bdrl.helpers.tools import eod, get_arg
from Bdrl.utils import modules_help, prefix, restart


@Client.on_message(
    filters.command(["setprefix", "sethandler", "setcmd"], prefix) & filters.me
)
async def setprefix_(c: Client, m: Message):
    handle = get_arg(m)
    if not handle:
        return await eod(
            m,
            f"Set you prefix use `{prefix}setprefix [new_prefix]`\n • Current prefix is `{prefix}`",
            time=30,
        )
    else:
        addgvar("PREFIX", handle)
        await m.edit(f"☑️ **Prefix change to** [`{handle}`]")
        restart()


modules_help["prefix"] = {
    "setprefix": "Set your prefix handler.",
}
