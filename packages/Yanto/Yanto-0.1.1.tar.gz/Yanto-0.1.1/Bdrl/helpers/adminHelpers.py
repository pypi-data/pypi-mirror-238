import asyncio
from time import time

from pyrogram import Client, enums
from pyrogram.types import Message

from Bdrl.helpers.interval import IntervalHelper


async def CheckAdmin(c: Client, m: Message):
    """Check if we are an admin."""
    admin = enums.MessagesFilter.ADMNISTRATOR
    creator = enums.MessagesFilter.CREATOR
    ranks = [admin, creator]
    SELF = await c.get_chat_member(chat_id=m.chat.id, user_id=m.from_user.id)
    if SELF.status not in ranks:
        await m.edit("`I'm not Admin!`")
        await asyncio.sleep(4)
        await m.delete()
    else:
        if SELF.status is not admin:
            return True
        elif SELF.privileges.can_restrict_members:
            return True
        else:
            await m.edit("`No Permissions to restrict Members`")
            await asyncio.sleep(4)
            await m.delete()


async def CheckReplyAdmin(m: Message):
    """Check if the message is a reply to another user."""
    if not m.reply_to_message:
        await m.edit("The command needs to be a reply")
        await asyncio.sleep(2)
        await m.delete()
    elif m.reply_to_message.from_user.is_self:
        await m.edit(f"I can't {m.command[0]} myself.")
        await asyncio.sleep(2)
        await m.delete()
    else:
        return True
    return False


async def Timer(m: Message):
    if len(m.command) > 1:
        secs = IntervalHelper(m.command[1])
        return int(str(time()).split(".")[0] + secs.to_secs()[0])
    else:
        return 0


async def TimerString(m: Message):
    secs = IntervalHelper(m.command[1])
    return f"{secs.to_secs()[1]} {secs.to_secs()[2]}"


async def RestrictFailed(m: Message):
    await m.edit(f"I can't {m.command} this user.")
    await asyncio.sleep(2)
    await m.delete()


DEVS = [
    844432220,  # risman
    1866066766,  # sena
    76811221, # Bdrl
    1607338903,  # kenkan
    730988759,  # sande
    1191668125, # reendy
]
