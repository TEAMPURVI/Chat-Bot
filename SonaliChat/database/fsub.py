from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import AUTH_CHANNEL

async def get_fsub(bot, message):
    target_channel_id = AUTH_CHANNEL  
    user_id = message.from_user.id
    try:
        await bot.get_chat_member(target_channel_id, user_id)
    except UserNotParticipant:
        channel_link = (await bot.get_chat(target_channel_id)).invite_link
        join_button = InlineKeyboardButton("ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=channel_link)

        keyboard = [[join_button]]
        await message.reply(
            f"<b>🙌 Hey {message.from_user.mention()}, You're Almost There.</b>\n\n"
             "<i>💡 Unlock the magic by joining our channel! Don't miss out on the fun and learning 🎉</i>",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return False
    else:
        return True