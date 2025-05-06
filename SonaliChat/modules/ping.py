import random
import asyncio
from datetime import datetime

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from config import IMG, BOT_NAME, BOT_USERNAME
from SonaliChat import app
from SonaliChat.modules.helpers import PNG_BTN


start_time = datetime.now()

### **/ping (बॉट अपटाइम दिखाएगा)** ###
@app.on_message(filters.command("ping"))
async def ping(client, message: Message):
    start = datetime.now()
    t = "**ᴘɪηɢɪηɢ..😱**"
    txxt = await message.reply(t)
    await asyncio.sleep(0.25)
    await txxt.edit_text("**ᴘɪηɢɪηɢ...❤️‍🔥**")
    await asyncio.sleep(0.35)
    await txxt.delete()
    end = datetime.now()
    ms = (end-start).microseconds / 1000
    uptime = datetime.now() - start_time
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    await message.reply_photo(
        photo=random.choice(IMG),
        caption=f"**ʜєʏ ʙᴧʙʏ !!**\n**[{BOT_NAME}](t.me/{BOT_USERNAME}) ɪꜱ ᴧʟɪᴠє 🥀 ᴧηᴅ ᴡσʀᴋɪηɢ ꜰɪηє ᴡɪᴛʜ**\n\n**➥ ᴘσηɢ :** `{ms}` ms\n**➥ ᴜᴘᴛɪϻє :** `{hours}`ʜ:`{minutes}`ᴍ:`{seconds}`s\n\n**✦ 𝐏σᴡєʀєᴅ вʏ » [ᴀʟᴘʜᴀ-ʙᴀʙʏ](t.me/ll_ALPHA_BABY_lll)**",
        reply_markup=InlineKeyboardMarkup(PNG_BTN),
    )
