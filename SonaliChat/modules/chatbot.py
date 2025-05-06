import random
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    CallbackQuery,
)

from config import MONGO_URL
from SonaliChat import app as Sonali
from SonaliChat.database import is_admins

# MongoDB setup
mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo["VickDb"]
chatbot_col = db["chatbot"]       # For enable/disable status
word_col = db["WordDb"]           # For chatbot word replies

# Inline keyboard
CHATBOT_ON = [
    [InlineKeyboardButton("Enable", callback_data="chatbot_enable")],
    [InlineKeyboardButton("Disable", callback_data="chatbot_disable")]
]


# Enable/Disable command
@Sonali.on_message(filters.command(["chatbot"]) & filters.group & ~filters.bot)
@is_admins
async def chatbot_toggle_command(_, m: Message):
    await m.reply_text(
        f"Chat ID: {m.chat.id}\n**Enable or Disable Chatbot?**",
        reply_markup=InlineKeyboardMarkup(CHATBOT_ON),
    )


# Callback Handler
@Sonali.on_callback_query(filters.regex("chatbot_(enable|disable)"))
async def chatbot_toggle_callback(_, query: CallbackQuery):
    status = query.data.split("_")[1]
    chat_id = query.message.chat.id

    if status == "enable":
        await chatbot_col.update_one(
            {"chat_id": chat_id}, {"$set": {"chatbot": True}}, upsert=True
        )
        await query.answer("Chatbot Enabled")
        await query.message.edit_text("**Chatbot has been Enabled.**")
    else:
        await chatbot_col.update_one(
            {"chat_id": chat_id}, {"$set": {"chatbot": False}}, upsert=True
        )
        await query.answer("Chatbot Disabled")
        await query.message.edit_text("**Chatbot has been Disabled.**")


# Group Handler
@Sonali.on_message((filters.text | filters.sticker) & filters.group & ~filters.bot)
async def chatbot_group(client: Client, message: Message):
    if message.text and message.text.startswith(("!", "/", "?", "@", "#")):
        return

    status = await chatbot_col.find_one({"chat_id": message.chat.id})
    if not status or not status.get("chatbot", False):
        return  # chatbot disabled

    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    responses = list(await word_col.find({"word": message.text}).to_list(length=50))

    if not message.reply_to_message:
        if responses:
            reply_data = random.choice(responses)
            if reply_data["check"] == "sticker":
                await message.reply_sticker(reply_data["text"])
            else:
                await message.reply_text(reply_data["text"])
    else:
        if message.reply_to_message.from_user.id == client.me.id:
            if responses:
                reply_data = random.choice(responses)
                if reply_data["check"] == "sticker":
                    await message.reply_sticker(reply_data["text"])
                else:
                    await message.reply_text(reply_data["text"])
        else:
            # Learn new word
            if message.sticker:
                await word_col.insert_one({
                    "word": message.reply_to_message.text,
                    "text": message.sticker.file_id,
                    "check": "sticker"
                })
            elif message.text:
                await word_col.insert_one({
                    "word": message.reply_to_message.text,
                    "text": message.text,
                    "check": "text"
                })


# Private Chat - Text
@Sonali.on_message(filters.text & filters.private & ~filters.bot)
async def chatbot_private(client: Client, message: Message):
    if message.text.startswith(("!", "/", "?", "@", "#")):
        return

    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    responses = list(await word_col.find({"word": message.text}).to_list(length=50))

    if responses:
        reply_data = random.choice(responses)
        if reply_data["check"] == "sticker":
            await message.reply_sticker(reply_data["text"])
        else:
            await message.reply_text(reply_data["text"])


# Private Chat - Sticker
@Sonali.on_message(filters.sticker & filters.private & ~filters.bot)
async def chatbot_private_sticker(client: Client, message: Message):
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    responses = list(await word_col.find({"word": message.sticker.file_unique_id}).to_list(length=50))

    if responses:
        reply_data = random.choice(responses)
        if reply_data["check"] == "text":
            await message.reply_text(reply_data["text"])
        else:
            await message.reply_sticker(reply_data["text"])
