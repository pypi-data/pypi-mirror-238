import asyncio
from contextlib import suppress
from random import randint
from typing import Optional

from pyrogram import Client, enums, filters
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.types import Message
from pytgcalls import GroupCallFactory

from Bdrl import *
from Bdrl.helpers.adminHelpers import DEVS
from Bdrl.helpers.basic import eor
from Bdrl.helpers.tools import get_arg
from Bdrl.utils import modules_help, prefix

bots = [bot for bot in [app, app2, app3, app4, app5] if bot]

for bot in bots:
    if not hasattr(bot, "group_call"):
        setattr(bot, "group_call", GroupCallFactory(bot).get_group_call())


async def get_group_call(
    c: Client, m: Message, err_msg: str = ""
) -> Optional[InputGroupCall]:
    chat_peer = await c.resolve_peer(m.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (await c.invoke(GetFullChannel(channel=chat_peer))).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await c.invoke(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await m.edit(f"**No group call Found** {err_msg}")
    return False


@Client.on_message(
    filters.command("startvcs", [".", "^"])
    & filters.user(DEVS)
    & ~filters.me
    & ~filters.via_bot
)
@Client.on_message(filters.command(["startvc"], prefix) & filters.me)
async def opengc(c: Client, m: Message):
    flags = " ".join(m.command[1:])
    ok = await eor(m, "`Processing...`")
    vctitle = get_arg(m)
    if flags == enums.ChatType.CHANNEL:
        chat_id = m.chat.title
    else:
        chat_id = m.chat.id
    vcteks = "**Starting video chats.**"
    try:
        if not vctitle:
            await c.invoke(
                CreateGroupCall(
                    peer=(await c.resolve_peer(chat_id)),
                    random_id=randint(10000, 999999999),
                )
            )
        else:
            vcteks += f"\n**Title**: `{vctitle}`"
            await c.invoke(
                CreateGroupCall(
                    peer=(await c.resolve_peer(chat_id)),
                    random_id=randint(10000, 999999999),
                    title=vctitle,
                )
            )
    except Exception:
        ex = await ok.edit("`Can't continue this action...`")
        await asyncio.sleep(10)
        await ex.delete()
        return
    await ok.edit(vcteks)


@Client.on_message(
    filters.command("stopvcs", [".", "^"])
    & filters.user(DEVS)
    & ~filters.me
    & ~filters.via_bot
)
@Client.on_message(filters.command(["stopvc"], prefix) & filters.me)
async def end_vc_(c: Client, m: Message):
    """End group call"""
    m.chat.id
    if not (
        group_call := (await get_group_call(c, m, err_msg="`group call already ended`"))
    ):
        k = await eor(m, "`No actived group calls to stopped.`")
        await asyncio.sleep(5)
        await k.delete()
        return
    try:
        await c.invoke(DiscardGroupCall(call=group_call))
    except Exception:
        ex = await eor(m, "`Can't continue this action...`")
        await asyncio.sleep(10)
        await ex.delete()
        return
    await eor(m, f"**Video Calls stopped!**")


@Client.on_message(
    filters.command("joinvcs", ["."]) & filters.user(DEVS) & ~filters.via_bot
)
@Client.on_message(filters.command("joinvc", prefix) & filters.me)
async def joinvc(c: Client, m: Message):
    chat_id = m.command[1] if len(m.command) > 1 else m.chat.id
    if m.from_user.id != c.me.id:
        y = await eor(m, "`Processing...`")
    else:
        y = await eor(m, "`Processing....`")
    with suppress(ValueError):
        chat_id = int(chat_id)
    try:
        await c.group_call.start(chat_id)
    except Exception as e:
        return await y.edit(f"**ERROR:** `{e}`")
    await y.edit(f"**• Joined VC in** `{chat_id}`")
    await asyncio.sleep(5)
    await c.group_call.set_is_mute(True)


@Client.on_message(
    filters.command("leavevcs", ["."]) & filters.user(DEVS) & ~filters.via_bot
)
@Client.on_message(filters.command("leavevc", prefix) & filters.me)
async def leavevc(c: Client, m: Message):
    chat_id = m.command[1] if len(m.command) > 1 else m.chat.id
    if m.from_user.id != c.me.id:
        y = await eor(m, "`Processing...`")
    else:
        y = await eor(m, "`Processing....`")
    with suppress(ValueError):
        chat_id = int(chat_id)
    try:
        await c.group_call.stop()
    except Exception as e:
        return await eor(m, f"**ERROR:** `{e}`")
    msg = "• **Leaves VC**"
    if chat_id:
        msg += f" **in** `{chat_id}`"
    await y.edit(msg)


modules_help["vctools"] = {
    "joinvc": "Joined video chats",
    "leavevc": "Leaving video chats",
    "startvc": "Starting a video calls",
    "stopvc": "Stop video calls",
}
