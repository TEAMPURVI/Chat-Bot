from typing import Callable, Union

from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message, CallbackQuery

from SonaliChat import app  


def is_admins(func: Callable) -> Callable:
    async def non_admin(c: app, m: Union[Message, CallbackQuery]):
        if isinstance(m, CallbackQuery):
            admin = await c.get_chat_member(m.message.chat.id, m.from_user.id)
        else:
            admin = await c.get_chat_member(m.chat.id, m.from_user.id)
        if admin.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return await func(c, m)

    return non_admin
