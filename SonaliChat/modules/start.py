import asyncio
import random

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.enums import ChatType

from config import STICKER, FSUB, IMG, LOGGER_GROUP_ID, BOT_USERNAME
from SonaliChat import app
from SonaliChat.database import add_user, add_chat, get_fsub, chatsdb
from SonaliChat.modules.helpers import (
    STBUTTON,
    HELP_BACK,
    ABOUT_BUTTON,
    START,
    HELP_READ,
    HELP_ABOUT,
)


@app.on_message(filters.command(["start", "aistart"]) & ~filters.bot)
async def start(client, m: Message):
    if FSUB and not await get_fsub(client, m):
        return

    bot_name = app.name

    if m.chat.type == ChatType.PRIVATE:
        user_id = m.from_user.id
        await add_user(user_id, m.from_user.username or None)

        if STICKER and isinstance(STICKER, list):
            sticker_to_send = random.choice(STICKER)
            umm = await m.reply_sticker(sticker=sticker_to_send)
            await asyncio.sleep(1)
            await umm.delete()

        # लॉगर ग्रुप में भेजें
        log_msg = f"**✦ ηєᴡ ᴜsєʀ sᴛᴧʀᴛєᴅ ᴛʜє ʙσᴛ**\n\n**➻ ᴜsєʀ :** [{m.from_user.first_name}](tg://user?id={user_id})\n**➻ ɪᴅ :** `{user_id}`"
        await client.send_message(LOGGER_GROUP_ID, log_msg)


        accha = await m.reply_text(text="**ꜱᴛᴧʀᴛɪηɢ....🥀**")
        await asyncio.sleep(1)
        await accha.edit("**ᴘɪηɢ ᴘσηɢ...🍫**")
        await asyncio.sleep(0.5)
        await accha.edit("**ꜱᴛᴧʀᴛєᴅ.....😱**")
        await asyncio.sleep(0.5)
        await accha.delete()

        # ✅ Ensure `START_IMG` and `START` variables exist
        await m.reply_photo(
        photo=random.choice(IMG),
        caption=START,
        reply_markup=InlineKeyboardMarkup(STBUTTON),
    )



### **जब बॉट को किसी ग्रुप में ऐड किया जाए** ###
@app.on_message(filters.new_chat_members)
async def on_new_chat_members(client: Client, message: Message):
    if (await client.get_me()).id in [user.id for user in message.new_chat_members]:
        chat_id = message.chat.id
        chat_title = message.chat.title
        added_by = message.from_user.mention if message.from_user else "Unknown User"
        chatusername = f"@{message.chat.username}" if message.chat.username else "Private Chat"

        # इन्वाइट लिंक प्राप्त करें
        try:
            invite_link = await client.export_chat_invite_link(chat_id)
        except Exception:
            invite_link = "Not Available"

        # सही तरीके से ग्रुप को डेटाबेस में सेव करें
        await add_chat(chat_id, chat_title)

        # ग्रुप में संदेश भेजे
        await message.reply_photo(
            photo=random.choice(IMG),
            caption=START,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("ᴧᴅᴅ ϻє ʙᴧʙʏ", url=f"https://t.me/{BOT_USERNAME}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users"),
                    InlineKeyboardButton("ᴊσɪη sᴜᴘᴘσʀᴛ", url="https://t.me/purvi_support")
                ]
            ])
        )

        # लॉग ग्रुप में जानकारी भेजें
        log_msg = (
            f"<b>✦ ʙᴏᴛ #ᴀᴅᴅᴇᴅ ɪɴ ᴀ ɢʀᴏᴜᴘ</b>\n\n"
            f"**⚘ ɢʀᴏᴜᴘ ɴᴀᴍᴇ :** {chat_title}\n"
            f"**⚘ ɢʀᴏᴜᴘ ɪᴅ :** {chat_id}\n"
            f"**⚘ ᴜsᴇʀɴᴀᴍᴇ :** {chatusername}\n"
            f"**⚘ ɢʀᴏᴜᴘ ʟɪɴᴋ : [ᴛᴀᴘ ʜᴇʀᴇ]({invite_link})**\n"
            f"**⚘ ᴀᴅᴅᴇᴅ ʙʏ :** {added_by}"
        )

        await app.send_photo(
            LOGGER_GROUP_ID,
            photo=random.choice(IMG),
            caption=log_msg,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ɢʀᴏᴜᴘ ʟɪɴᴋ", url=invite_link if invite_link != "Not Available" else "https://t.me/purvi_support")]
            ])
        )
        
@app.on_message(filters.left_chat_member)
async def on_left_chat_member(client: Client, message: Message):
    if (await client.get_me()).id == message.left_chat_member.id:
        chat_id = message.chat.id
        chat_title = message.chat.title
        remove_by = message.from_user.mention if message.from_user else "Unknown User"
       
         # डेटाबेस से ग्रुप हटाएं
        await chatsdb.delete_one({"chat_id": chat_id})
        
        left_msg = (
            f"<b>✦ ʙᴏᴛ #ʟᴇғᴛ ᴀ ɢʀᴏᴜᴘ</b>\n\n"
            f"**⚘ ɢʀᴏᴜᴘ ɴᴀᴍᴇ :** {chat_title}\n"
            f"**⚘ ɢʀᴏᴜᴘ ɪᴅ :** {chat_id}\n"
            f"**⚘ ʀᴇᴍᴏᴠᴇᴅ ʙʏ :** {remove_by}"
        )
        
        await app.send_photo(
            LOGGER_GROUP_ID,
            photo=random.choice(IMG),
            caption=left_msg,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("sᴇᴇ ɢʀᴏᴜᴘ", url=f"https://t.me/{message.chat.username}" if message.chat.username else "https://t.me/purvi_support")]
            ])
        )



# Help command for displaying instructions
@app.on_message(filters.command("help"))
async def help_command(client, message):
    hmm = await message.reply_photo(
        photo=random.choice(IMG),
        caption=HELP_READ,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", url=f"https://t.me/{client.me.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users"),
                InlineKeyboardButton("ᴊᴏɪɴ sᴜᴘᴘᴏʀᴛ", url="https://t.me/purvi_support")
            ]
        ])
    )
    


# Help बटन के लिए callback handler
@app.on_callback_query(filters.regex('help'))
async def help_button(client, callback_query):
    help_text=HELP_READ
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ʙᴀᴄᴋ ᴛᴏ ʜᴏᴍᴇ", callback_data="back"),
            InlineKeyboardButton("ᴊᴏɪɴ sᴜᴘᴘᴏʀᴛ", url="https://t.me/purvi_support")
        ]
    ])
    await callback_query.answer()
    await callback_query.message.edit_text(help_text, reply_markup=keyboard)

# Back to Menu बटन के लिए callback handler
@app.on_callback_query(filters.regex('back'))
async def back_to_menu(client, callback_query):
    
    # Back to Menu के लिए केवल बटन के साथ मेनू अपडेट करें
    await callback_query.message.edit_text(
        text=START,
        reply_markup=InlineKeyboardMarkup(STBUTTON),
    )



# ✅ About Section के लिए Callback Handler
@app.on_callback_query(filters.regex('ABOUT'))
async def about_section(client, callback_query):
    about_text = HELP_ABOUT  # About Section का टेक्स्ट
    
    keyboard = InlineKeyboardMarkup(ABOUT_BUTTON)  # About Section का बटन
    
    await callback_query.answer()
    await callback_query.message.edit_text(about_text, reply_markup=keyboard)




# ✅ Help से वापस Home जाने के लिए Callback Handler
@app.on_callback_query(filters.regex('HELP_BACK'))
async def help_back(client, callback_query):
    await callback_query.message.edit_text(
        text=START,
        reply_markup=InlineKeyboardMarkup(STBUTTON)
    )
