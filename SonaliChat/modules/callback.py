from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.types import CallbackQuery
from Sonali import app as Sonali  
from Sonali.database import vick

@Sonali.on_callback_query()
async def chatbot_toggle_handler(_, query: CallbackQuery):
    user_id = query.from_user.id
    user_status = (await query.message.chat.get_member(user_id)).status

    if query.data == "addchat":
        if user_status not in [CMS.OWNER, CMS.ADMINISTRATOR]:
            return await query.answer(
                "ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴇᴠᴇɴ ᴀɴ ᴀᴅᴍɪɴ, ᴅᴏɴ'ᴛ ᴛʀʏ ᴛʜɪs ᴇxᴘʟᴏsɪᴠᴇ sʜɪᴛ!",
                show_alert=True,
            )
        is_vick = vick.find_one({"chat_id": query.message.chat.id})
        if not is_vick:
            await query.edit_message_text("**ᴄʜᴀᴛ-ʙᴏᴛ ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ.**")
        else:
            vick.delete_one({"chat_id": query.message.chat.id})
            await query.edit_message_text(
                f"**ᴄʜᴀᴛ-ʙᴏᴛ ᴇɴᴀʙʟᴇᴅ ʙʏ** {query.from_user.mention}."
            )

    elif query.data == "rmchat":
        if user_status not in [CMS.OWNER, CMS.ADMINISTRATOR]:
            return await query.answer(
                "ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴇᴠᴇɴ ᴀɴ ᴀᴅᴍɪɴ, ᴅᴏɴ'ᴛ ᴛʀʏ ᴛʜɪs ᴇxᴘʟᴏsɪᴠᴇ sʜɪᴛ!",
                show_alert=True,
            )
        is_vick = vick.find_one({"chat_id": query.message.chat.id})
        if not is_vick:
            vick.insert_one({"chat_id": query.message.chat.id})
            await query.edit_message_text(
                f"**ᴄʜᴀᴛ-ʙᴏᴛ ᴅɪsᴀʙʟᴇᴅ ʙʏ** {query.from_user.mention}."
            )
        else:
            await query.edit_message_text("**ᴄʜᴀᴛ-ʙᴏᴛ ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ.**")
