from pyrogram.types import Message


def get_user(m: Message, text: str) -> [int, str, None]:
    """Get User From Message"""
    if text is None:
        asplit = None
    else:
        asplit = text.split(" ", 1)
    user_s = None
    reason_ = None
    if m.reply_to_message:
        user_s = m.reply_to_message.from_user.id
        reason_ = text if text else None
    elif asplit is None:
        return None, None
    elif len(asplit[0]) > 0:
        if m.entities:
            if len(m.entities) == 1:
                required_entity = m.entities[0]
                if required_entity.type == "text_mention":
                    user_s = int(required_entity.user.id)
                else:
                    user_s = int(asplit[0]) if asplit[0].isdigit() else asplit[0]
        else:
            user_s = int(asplit[0]) if asplit[0].isdigit() else asplit[0]
        if len(asplit) == 2:
            reason_ = asplit[1]
    return user_s, reason_


def get_text(m: Message) -> [None, str]:
    """Extract Text From Commands"""
    text_to_return = m.text
    if m.text is None:
        return None
    if " " in text_to_return:
        try:
            return m.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


async def edit_or_reply(m: Message, *args, **kwargs) -> Message:
    k = (
        m.edit_text
        if bool(m.from_user and m.from_user.is_self or m.outgoing)
        else (m.reply_to_message or m).reply_text
    )
    return await k(*args, **kwargs)


eor = edit_or_reply
