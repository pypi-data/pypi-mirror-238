#  Copyright (C) 2022-present Bdrl
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.


import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from Bdrl.helpers.tools import eod
from Bdrl.utils import *


@Client.on_message(filters.command("help", prefix) & filters.me)
async def help_cmd(c: Client, m: Message):
    if len(m.command) == 1:
        msg_edited = False
        text = (
            "• <b>Help for Bdrl</b>"
            f"\n• <b>Total modules:</b> <code>{len(modules_help)}</code>\n"
            f"\n• <b>Try Type</b> <code>{prefix}help [module]</code> to see description of the modules/command.\n\n"
        )
        for module_name, module_commands in modules_help.items():
            text += "<code>{} </code>".format(module_name.title())
            if len(text) >= 2048:
                text += ""
                if msg_edited:
                    await eod(m, text, time=70)
                else:
                    await eod(m, text, time=70)
                    msg_edited = True
                text = ""
        text += f"\n\n©️ 2022-present Bdrl"

        if msg_edited:
            await eod(m, text, time=70)
        else:
            await eod(m, text, time=70)
    elif m.command[1].lower() in modules_help:
        await m.edit(format_module_help(m.command[1].lower()))
    else:
        # TODO: refactor this cringe
        command_name = m.command[1].lower()
        for name, commands in modules_help.items():
            for command in commands.keys():
                if command.split()[0] == command_name:
                    cmd = command.split(maxsplit=1)
                    cmd_desc = commands[command]
                    return await eod(
                        m,
                        f"<b>Help for command <code>{prefix}{command_name}</code>\n"
                        f"Module: {name} (<code>{prefix}help {name}</code>)</b>\n\n"
                        f"<code>{prefix}{cmd[0]}</code>"
                        f"{' <code>' + cmd[1] + '</code>' if len(cmd) > 1 else ''}"
                        f" — <i>{cmd_desc}</i>"
                        "\n\n©️ 2022-present Bdrl",
                        time=70,
                    )
        ok = await eod(m, f"<b>Module</b> <code>{command_name}</code> <b>not found</b>")
        await asyncio.sleep(10)
        await ok.delete()
