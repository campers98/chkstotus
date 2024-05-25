import asyncio
from pyrogram import Client, filters, types
from pyrogram.errors import FloodWait
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import pytz
from ANNIEMUSIC.core.userbot import Userbot
from ANNIEMUSIC import app

load_dotenv()

userbot = Userbot()

app = Client(
    "botstatus_univ",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    session_string=os.getenv("STRING_SESSION")
)

TIME_ZONE = os.getenv("TIME_ZONE")
CHANNEL_ID = os.getenv("CHANNEL_ID")
MESSAGE_ID = int(os.getenv("MESSAGE_ID"))
BOT_ADMIN_IDS = [int(i.strip()) for i in os.getenv("BOT_ADMIN_IDS").split(' ')]
LOG_ID = os.getenv("LOG_ID")

# Dictionary to store bot owner and log group associations
BOT_OWNERS_AND_LOGS = {}

# Global variable to hold the status message
xxx_univ = ""

# Function to load bot owners and logs from a JSON file
def load_bot_owners_and_logs_from_file(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return {}

# Function to save bot owners and logs to a JSON file
def save_bot_owners_and_logs_to_file(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# Load BOT_OWNERS_AND_LOGS data from the JSON file
BOT_OWNERS_AND_LOGS_FILE = "bot_owners_and_logs.json"
BOT_OWNERS_AND_LOGS = load_bot_owners_and_logs_from_file(BOT_OWNERS_AND_LOGS_FILE)

# Function to update the status message and send it to the channel
async def update_and_send_status_message():
    global xxx_univ
    xxx_univ = "★ | ▄︻デ ᑗŇƗV€ŘŞ€ ✶ N͞e͞t͞w͞o͞r͞k͞s͞  ★ \n              | 【 Ⴆσƚs • ⃤• ƗŇ₣Ø 】 |"

    for bot in BOT_OWNERS_AND_LOGS:
        try:
            yyy_univ = await app.send_message(bot, "/start")
            aaa = yyy_univ.id
            await asyncio.sleep(5)

            async for ccc in app.get_chat_history(bot, limit=1):
                bbb = ccc.id

            if aaa == bbb:
                xxx_univ += f"\n\n🗯  @{bot}\n        ⇃➫ **─═ 🅒🅛🅞🅢🅔 ═─** 💔"
            else:
                xxx_univ += f"\n\n🗯  @{bot}\n        ⇃➫ **↬【 ƠƤЄƝ 】↫**  📂"
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception as e:
            print(f"Error checking bot status for {bot}: {e}")

    time = datetime.now(pytz.timezone(TIME_ZONE))
    last_update = time.strftime("%d %b %Y at %I:%M:%S %p")
    xxx_univ += f"\n\n🆗🧘‍♂️ Fi͠n͠a͠l͠ ͠Up͠d͠a͠t͠i͠o͠n͠ ͠oN͠ : {last_update} ({TIME_ZONE})\n\n**🥶 🇷‌🇪‌🇧‌🇴‌🇴‌🇹‌🇸‌ 🇪‌🇻‌🇪‌🇷‌🇾‌\n                  1̳2̳0̳  🇸‌🇪‌🇨**"

    try:
        channel_id_int = int(CHANNEL_ID)
        message_id_int = int(MESSAGE_ID)
        await app.edit_message_text(channel_id_int, message_id_int, xxx_univ)
        print(f"Last checked on: {last_update}")
    except Exception as e:
        print(f"Error updating status message: {e}")

async def send_message_to_chat(chat_id, message):
    if chat_id:
        try:
            await app.send_message(chat_id, message)
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")

# Add a command handler to dynamically add bots and their owner IDs and log group IDs
@app.on_message(filters.command("addbot") & filters.chat(int(LOG_ID)) & filters.group)
async def add_bot_handler(client: Client, message: types.Message):
    global xxx_univ

    if not message.from_user.id in BOT_ADMIN_IDS:
        await message.reply("You are not authorized to add bots.")
        return

    try:
        _, bot, owner_id, log_group_id = message.text.split(" ", 3)
        if bot in BOT_OWNERS_AND_LOGS:
            await message.reply(f"The bot '{bot}' already exists in the list.")
            return

        owner_id = int(owner_id)
        log_group_id = int(log_group_id)

        BOT_OWNERS_AND_LOGS[bot] = {"owner_id": owner_id, "log_group_id": log_group_id}
        save_bot_owners_and_logs_to_file(BOT_OWNERS_AND_LOGS_FILE, BOT_OWNERS_AND_LOGS)

        xxx_univ += f"\n\n🗯  @{bot}\n        ⇃➫ **─═ 🅒🅛🅞🅢🅔 ═─** 💔"
        await update_and_send_status_message()

        await message.reply(f"Added {bot} with owner ID: {owner_id} and log group ID: {log_group_id}")
    except ValueError:
        await message.reply("Invalid input. Use `/addbot bot_name owner_id log_group_id` format.\n\nExample: `/addbot Divu1_bot 5276467233 -1001686570489`")

# Add command handler to remove bots from the list
@app.on_message(filters.command("removebot") & filters.chat(int(LOG_ID)) & filters.group)
async def remove_bot_handler(client: Client, message: types.Message):
    if not message.from_user.id in BOT_ADMIN_IDS:
        await message.reply("You are not authorized to remove bots.")
        return

    try:
        _, bot = message.text.split(" ")
        if bot in BOT_OWNERS_AND_LOGS:
            BOT_OWNERS_AND_LOGS.pop(bot)
            save_bot_owners_and_logs_to_file(BOT_OWNERS_AND_LOGS_FILE, BOT_OWNERS_AND_LOGS)
            await update_and_send_status_message()
            await message.reply(f"Removed {bot} from the list.")
        else:
            await message.reply(f"The bot '{bot}' does not exist in the list.")
    except ValueError:
        await message.reply("Invalid input. Use `/removebot bot_name` format.\n\nExample: `/removebot Divu1_bot`")

# Command handler to list all the bots and their details
@app.on_message(filters.command("botslist") & filters.chat(int(LOG_ID)) & filters.group)
async def list_bots(client: Client, message: types.Message):
    if not message.from_user.id in BOT_ADMIN_IDS:
        await message.reply("You are not authorized to access the bots list.")
        return

    if not BOT_OWNERS_AND_LOGS:
        await message.reply("No bots have been added to the list yet.")
        return

    response = "**List of Bots and their Details:**\n"
    for bot, info in BOT_OWNERS_AND_LOGS.items():
        owner_id = info["owner_id"]
        log_group_id = info["log_group_id"]
        response += f"\nBot: @{bot}\nOwner ID: `{owner_id}`\nLog Group ID: `{log_group_id}`\n"

    await message.reply(response)

@app.on_message(filters.command("test"))
async def test_command(client: Client, message: types.Message):
    print(f"/test command invoked by user {message.from_user.id} in group {message.chat.id}")
    await message.reply("Test command received.")

# Command handler to check individual bot status
@app.on_message(filters.command("botschk") & filters.group)
async def check_bots_command(client: Client, message: types.Message):
    global last_checked_time
    try:
        await userbot.one.start()
        start_time = datetime.now()

        command_parts = message.command
        if len(command_parts) == 2:
            bot_username = command_parts[1]
            response = ""
            try:
                bot = await userbot.one.get_users(bot_username)
                bot_id = bot.id
                await asyncio.sleep(0.5)
                await userbot.one.send_message(bot_id, "/start")
                await asyncio.sleep(3)
                async for bot_message in userbot.one.get_chat_history(bot_id, limit=1):
                    if bot_message.from_user.id == bot_id:
                        response += f"╭⎋ {bot.mention}\n l\n╰⊚ **sᴛᴀᴛᴜs: ᴏɴʟɪɴᴇ ✨**\n\n"
                    else:
                        response += f"╭⎋ [{bot.mention}](tg://user?id={bot.id})\n l\n╰⊚ **sᴛᴀᴛᴜs: ᴏғғʟɪɴᴇ ❄**\n\n"
            except Exception:
                response += f"╭⎋ {bot_username}\n l\n╰⊚ **ᴇɪᴛʜᴇʀ ʏᴏᴜ ʜᴀᴠᴇ ɢɪᴠᴇɴ ᴡʀᴏɴɢ ᴜsᴇʀɴᴀᴍᴇ ᴏᴛʜᴇʀᴡɪsᴇ ɪ ᴀᴍ ᴜɴᴀʙʟᴇ ᴛᴏ ᴄʜᴇᴄᴋ ᴅᴜᴇ ᴛᴏ ʟɪᴍɪᴛᴀᴛɪᴏɴ. **\n\n"
            last_checked_time = start_time.strftime("%Y-%m-%d")
            await message.reply_text(f"{response}⏲️ ʟᴀsᴛ ᴄʜᴇᴄᴋ: {last_checked_time}")
        else:
            await message.reply_text("ɪɴᴠᴀʟɪᴅ ᴄᴏᴍᴍᴀɴᴅ ғᴏʀᴍᴀᴛ.\n\nᴘʟᴇᴀsᴇ ᴜsᴇ /botschk Bot_Username\n\nʟɪᴋᴇ :- `/botschk @Annie_X_music_bot`")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
        print(f"Error occurred during /botschk command: {e}")
    finally:
        await userbot.one.stop()

async def main_univ():
    global xxx_univ
    async with app:
        while True:
            await update_and_send_status_message()
            await asyncio.sleep(120)

app.run(main_univ())
