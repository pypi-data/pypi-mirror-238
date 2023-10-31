# Copyright (C) 2022 CtrlUB
#
# This file is a part of < https://github.com/kennedy-ex/CtrlUB/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/kennedy-ex/CtrlUB/blob/main/LICENSE/>.
#


from asyncio import sleep

from pyrogram import Client, enums, filters
from pyrogram.raw import functions
from pyrogram.types import Message

from Bdrl.utils import modules_help, prefix

commands = {
    "ftyping": enums.ChatAction.TYPING,
    "fvideo": enums.ChatAction.RECORD_VIDEO,
    "faudio": enums.ChatAction.RECORD_AUDIO,
    "fround": enums.ChatAction.RECORD_VIDEO_NOTE,
    "fphoto": enums.ChatAction.UPLOAD_PHOTO,
    "fuaudio": enums.ChatAction.UPLOAD_AUDIO,
    "fuvideo": enums.ChatAction.UPLOAD_VIDEO,
    "fudocument": enums.ChatAction.UPLOAD_DOCUMENT,
    "fsticker": enums.ChatAction.CHOOSE_STICKER,
    "flocation": enums.ChatAction.FIND_LOCATION,
    "fgame": enums.ChatAction.PLAYING,
    "fcontact": enums.ChatAction.CHOOSE_CONTACT,
    "fstop": enums.ChatAction.CANCEL,
    "fuvideo": enums.ChatAction.UPLOAD_VIDEO_NOTE,
    "fspeaking": enums.ChatAction.SPEAKING,
}


@Client.on_message(filters.command(list(commands), prefix) & filters.me)
async def fakeactions_handler(client: Client, message: Message):
    cmd = message.command[0]
    try:
        sec = int(message.command[1])
        if sec > 60:
            sec = 60
    except:
        sec = None
    await message.delete()
    action = commands[cmd]
    try:
        if action != enums.ChatAction.CANCEL:
            if sec and action != enums.ChatAction.CANCEL:
                await client.send_chat_action(chat_id=message.chat.id, action=action)
                await sleep(sec)
            else:
                return await client.send_chat_action(
                    chat_id=message.chat.id, action=action
                )
        else:
            for _ in range(sec if sec else 1):
                await client.send(
                    functions.messages.SendScreenshotNotification(
                        peer=await client.resolve_peer(message.chat.id),
                        reply_to_msg_id=0,
                        random_id=client.rnd_id(),
                    )
                )
                await sleep(0.1)
    except Exception as e:
        return await client.send_message(message.chat.id, f"**ERROR:** `{e}`")


modules_help["fakeaction"] = {
    "ftyping [time]": "Fake typing in chats",
    "fvideo [time]": "Fake recording video",
    "faudio [time]": "Fake recording audio",
    "frevideo [time]": "Fake recording video",
    "fphoto [time]": "Fake upload photos",
    "fuaudio [time]": "Fake upload audio",
    "fuvideo [time]": "Fake upload video",
    "fudocument [time]": "Fake upload document",
    "fsticker [time]": "Fake choosing a sticker",
    "flocation [time]": "Fake finding location",
    "fgame [time]": "Fake playing game",
    "fcontact [time]": "Fake choosing contact",
    "fuvideonote [time]": "Fake upload video note",
    "fspeaking [time]": "Fake speaking on the video calls"
    f"\n\nNOTE: stop fake action with [`{prefix}fstop`]",
}
