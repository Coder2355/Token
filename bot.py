from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from unit import generate_token, get_verify_shorted_link, verify_token, save_verification, is_verified

API_ID = "28015531"
API_HASH = "2ab4ba37fd5d9ebf1353328fc915ad28"
BOT_TOKEN = "7800807621:AAHctirzl9smHyCPXZbtSBkTlyT6vVgKbVE"
BOT_USERNAME = "Hshdgdvdv23bot"

app = Client("group_verification_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

TOKENS = {}

@app.on_message(filters.group)
async def handle_group_messages(client, message):
    """
    Restrict unverified users in the group and guide them to verify.
    """
    if not await is_verified(message.from_user.id):
        # Restrict the user from sending messages
        await app.restrict_chat_member(
            message.chat.id,
            message.from_user.id,
            ChatPermissions(can_send_messages=False)
        )
        token = await generate_token()
        TOKENS[message.from_user.id] = {"token": token, "expiry": datetime.now() + timedelta(days=1)}
        verify_link = f"https://t.me/{BOT_USERNAME}?start=verify-{message.from_user.id}-{token}"
        shortened_link = await get_verify_shorted_link(verify_link)
        await message.reply(
            f"🚫 {message.from_user.mention}, you are not verified!\nClick the button below to verify yourself:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Verify Now", url=shortened_link)]])
        )
        return

@app.on_message(filters.command("start") & filters.private)
async def verify_user(client, message):
    """
    Handle verification process through the link.
    """
    if len(message.command) > 1:
        data = message.command[1].split("-")
        if len(data) == 3 and data[0] == "verify":
            user_id, token = int(data[1]), data[2]
            if await verify_token(user_id, token):
                await save_verification(user_id)
                await message.reply_text("✅ You are successfully verified! You can now message in the group.")
                return
            else:
                await message.reply_text("❌ Invalid or expired token!")
                return
    await message.reply_text("⚠️ Invalid usage. Please use the verification link provided in the group.")

@app.on_message(filters.command("reset") & filters.group)
async def reset_verification(client, message):
    """
    Admin command to reset a user's verification status.
    """
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        if user_id in VERIFIED_USERS:
            del VERIFIED_USERS[user_id]
        await app.restrict_chat_member(
            message.chat.id,
            user_id,
            ChatPermissions(can_send_messages=False)
        )
        await message.reply_text(f"🔄 Verification reset for {message.reply_to_message.from_user.mention}.")
    else:
        await message.reply_text("⚠️ Reply to a user's message to reset their verification.")

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
