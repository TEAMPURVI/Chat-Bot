from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from SonaliChat import app
from SonaliChat.database import get_chats


@app.on_message(filters.command("stats"))
async def stats(client: app, message: Message):
    data = await get_chats()
    total_users = len(data["users"])
    total_chats = len(data["chats"])

    await message.reply_text(
        f"""**✮ {(await client.get_me()).first_name}  ʙᴏᴛ sᴛᴀᴛs :**\n
**:⧽ ᴜsᴇʀs :** {total_users}
**:⧽ ɢʀᴏᴜᴘs :** {total_chats}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ", url="https://t.me/SonaliSonaliChat?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users"),
                    InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/PURVI_SUPPORT"),
                ]
            ]
        )
    )
