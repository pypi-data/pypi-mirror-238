from asyncio import gather
from random import choice

from pyrogram import Client, enums, filters
from pyrogram.types import *

from Bdrl.utils import modules_help, prefix


@Client.on_message(filters.command("asupan", prefix) & filters.me)
async def asupan(client: Client, message: Message):
    await gather(
        client.send_video(
            message.chat.id,
            choice(
                [
                    asupan.video.file_id
                    async for asupan in client.search_messages(
                        "punyakenkan", filter=enums.MessagesFilter.VIDEO
                    )
                ]
            ),
            reply_to_message_id=message.id,
        ),
    )


modules_help["asupan"] = {
    "asupan": "View the intake video",
}
