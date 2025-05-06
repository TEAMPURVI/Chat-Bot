import random
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from pyrogram.types import InlineKeyboardMarkup, Message

from config import MONGO_URL
from SonaliChat import app as Sonali
from SonaliChat.modules.helpers import CHATBOT_ON
from SonaliChat.database import is_admins


#Chatbot ON/OFF Command (Group Admins Only)
@Sonali.on_message(filters.command(["chatbot"]) & filters.group & ~filters.bot)
@is_admins
async def chaton_off(_, m: Message):
    await m.reply_text(
        f"Chat ID: {m.chat.id}\n**Enable or Disable Chatbot?**",
        reply_markup=InlineKeyboardMarkup(CHATBOT_ON),
    )


#Group Chatbot Handler (Text & Stickers)
@Sonali.on_message(
    (filters.text | filters.sticker) & filters.group & ~filters.bot
)
async def chatbot_group(client: Client, message: Message):
    if message.text and message.text.startswith(("!", "/", "?", "@", "#")):
        return

    chatdb = MongoClient(MONGO_URL)
    chatai = chatdb["Word"]["WordDb"]

    if not message.reply_to_message:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        responses = list(chatai.find({"word": message.text}))

        if responses:
            reply_data = random.choice(responses)
            if reply_data["check"] == "sticker":
                await message.reply_sticker(reply_data["text"])
            else:
                await message.reply_text(reply_data["text"])
    else:
        # If user replies to bot's message
        if message.reply_to_message.from_user.id == client.me.id:
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            responses = list(chatai.find({"word": message.text}))

            if responses:
                reply_data = random.choice(responses)
                if reply_data["check"] == "sticker":
                    await message.reply_sticker(reply_data["text"])
                else:
                    await message.reply_text(reply_data["text"])
        else:
            # Learn new words if user replies to someone else
            if message.sticker:
                chatai.insert_one({
                    "word": message.reply_to_message.text,
                    "text": message.sticker.file_id,
                    "check": "sticker"
                })
            elif message.text:
                chatai.insert_one({
                    "word": message.reply_to_message.text,
                    "text": message.text,
                    "check": "text"
                })


#Private Chatbot Handler (Text & Stickers)
@Sonali.on_message(filters.text & filters.private & ~filters.bot)
async def chatbot_private(client: Client, message: Message):
    if message.text.startswith(("!", "/", "?", "@", "#")):
        return

    chatdb = MongoClient(MONGO_URL)
    chatai = chatdb["Word"]["WordDb"]

    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    responses = list(chatai.find({"word": message.text}))

    if responses:
        reply_data = random.choice(responses)
        if reply_data["check"] == "sticker":
            await message.reply_sticker(reply_data["text"])
        else:
            await message.reply_text(reply_data["text"])


# Private Chatbot Sticker Handler
@Sonali.on_message(filters.sticker & filters.private & ~filters.bot)
async def chatbot_private_sticker(client: Client, message: Message):
    chatdb = MongoClient(MONGO_URL)
    chatai = chatdb["Word"]["WordDb"]

    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    responses = list(chatai.find({"word": message.sticker.file_unique_id}))

    if responses:
        reply_data = random.choice(responses)
        if reply_data["check"] == "text":
            await message.reply_text(reply_data["text"])
        else:
            await message.reply_sticker(reply_data["text"])
