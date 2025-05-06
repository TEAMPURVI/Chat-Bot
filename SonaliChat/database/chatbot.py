from . import chatsdb

async def is_SonaliChat_enabled(chat_id: int) -> bool:
    """Checks if SonaliChat is enabled for a group."""
    chat = await chatsdb.find_one({"chat_id": chat_id})
    return chat is None

async def enable_SonaliChat(chat_id: int):
    """Enables SonaliChat for a group."""
    await chatsdb.delete_one({"chat_id": chat_id})

async def disable_SonaliChat(chat_id: int):
    """Disables SonaliChat for a group."""
    if not await chatsdb.find_one({"chat_id": chat_id}):
        await chatsdb.insert_one({"chat_id": chat_id})

async def get_enabled_chats() -> list:
    """Returns a list of chat IDs where SonaliChat is enabled."""
    chats = await chatsdb.find({}, {"chat_id": 1, "_id": 0}).to_list(length=None)
    return [chat["chat_id"] for chat in chats]
