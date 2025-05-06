from functools import wraps
from pyrogram.types import Message

async def is_user_admin(chat, user_id, client):
    member = await client.get_chat_member(chat.id, user_id)
    return member.status in ("administrator", "creator")

def is_admins(func):
    @wraps(func)
    async def wrapper(client, message: Message):
        if await is_user_admin(message.chat, message.from_user.id, client):
            return await func(client, message)
        else:
            return await message.reply("Only group admins can use this command.")
    return wrapper
