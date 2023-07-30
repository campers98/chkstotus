from pyrogram import Client, filters, types
from pyrogram.errors import FloodWait
import asyncio
import datetime
import pytz
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = Client(
    name = "botstatus_pratheek",
    api_id = int(os.getenv("API_ID")),
    api_hash = os.getenv("API_HASH"),
    session_string = os.getenv("STRING_SESSION")
)
TIME_ZONE = os.getenv("TIME_ZONE")
BOT_LIST = [i.strip() for i in os.getenv("BOT_LIST").split(' ')]
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
MESSAGE_ID = int(os.getenv("MESSAGE_ID"))
BOT_ADMIN_IDS = [int(i.strip()) for i in os.getenv("BOT_ADMIN_IDS").split(' ')]
LOG_ID = int(os.getenv("LOG_ID"))

# Dictionary to store bot owner and log group associations
BOT_OWNERS_AND_LOGS = {
    "Divu1_bot": {"owner_id": 5276467211, "log_group_id": -1001686570455}, # Add more bots and their corresponding owner_id and log_group_id
    "Isai_mazhai_bot": {"owner_id": 655594746, "log_group_id": -1001975251757}, # Add more bots and their corresponding owner_id and log_group_id
    "common": {"log_group_id": -1001600523208},  # Add the common log group ID here
    
}

# Global variable to hold the status message
xxx_pratheek = ""

# Function to update the status message and send it to the channel
async def update_and_send_status_message():
    global xxx_pratheek
    xxx_pratheek = "📊 | 𝗟𝗜𝗩𝗘 𝗕𝗢𝗧 𝗦𝗧𝗔𝗧𝗨𝗦"

    for bot in BOT_LIST:
        try:
            ok = await app.get_users(f"@{bot}")
            yyy_pratheek = await app.send_message(bot, "/help")
            aaa = yyy_pratheek.id
            await asyncio.sleep(2)
            async for ccc in app.get_chat_history(bot, limit=1):
                bbb = ccc.id
            if aaa == bbb:
                xxx_pratheek += f"\n\n🤖  @{bot}\n        └ **Down** ❌"
            else:
                xxx_pratheek += f"\n\n🤖  @{bot}\n        └ **Alive** ✅"
        except FloodWait as e:
            await asyncio.sleep(e.x)

    time = datetime.datetime.now(pytz.timezone(f"{TIME_ZONE}"))
    last_update = time.strftime(f"%d %b %Y at %I:%M %p")
    xxx_pratheek += f"\n\n✔️ Last checked on: {last_update} ({TIME_ZONE})\n\n**♻️ Refreshes automatically**"

    await app.edit_message_text(int(CHANNEL_ID), MESSAGE_ID, xxx_pratheek)
    print(f"Last checked on: {last_update}")

async def send_message_to_chat(chat_id, message):
    if chat_id:
        try:
            await app.send_message(chat_id, message)
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")

# Add a command handler to dynamically add bots and their owner IDs and log group IDs
@app.on_message(filters.command("addbot") & filters.chat(LOG_ID) & filters.group)
@app.on_message(filters.command("addbot") & filters.chat(LOG_ID) & filters.group)
async def add_bot_handler(client: Client, message: types.Message):
    global xxx_pratheek  # Define the global variable
    
    if not message.from_user.id in BOT_ADMIN_IDS:
        await message.reply("You are not authorized to add bots.")
        return

    try:
        # Split the command into its arguments (bot, owner_id, log_group_id)        
        _, bot, owner_id, log_group_id = message.text.split(" ", 3)

        # Check if the bot already exists in the dictionary
        if bot in BOT_OWNERS_AND_LOGS:
            await message.reply(f"The bot '{bot}' already exists in the list.")
            return
            
        # Convert owner_id and log_group_id to integers
        owner_id = int(owner_id)
        log_group_id = int(log_group_id)

        # Update the BOT_OWNERS_AND_LOGS dictionary
        BOT_OWNERS_AND_LOGS[bot] = {"owner_id": owner_id, "log_group_id": log_group_id}

        # Save the updated dictionary to environment variables
        save_bot_owners_and_logs_to_env()

        xxx_pratheek += f"\n\n🤖  @{bot}\n        └ **Down** ❌"  # Update status message for the newly added bot

        # Update the status message and send it to the channel
        await update_and_send_status_message()

        # Reply with a success message
        await message.reply(f"Added {bot} with owner ID: {owner_id} and log group ID: {log_group_id}")
    except ValueError:
        await message.reply("Invalid input. Use /addbot <bot> <owner_id> <log_group_id> format.")
        
# Add command handler to remove bots from the list
@app.on_message(filters.command("removebot") & filters.chat(LOG_ID) & filters.group)
async def remove_bot_handler(client: Client, message: types.Message):
    if not message.from_user.id in BOT_ADMIN_IDS:
        await message.reply("You are not authorized to remove bots.")
        return

    try:
        # Get the bot name to be removed
        _, bot = message.text.split(" ")

        # Check if the bot exists in the dictionary
        if bot in BOT_OWNERS_AND_LOGS:
            # Remove the bot from the dictionary
            BOT_OWNERS_AND_LOGS.pop(bot)

            # Save the updated dictionary to environment variables
            save_bot_owners_and_logs_to_env()

            # Update the status message and send it to the channel
            await update_and_send_status_message()

            await message.reply(f"Removed {bot} from the list.")
        else:
            await message.reply(f"The bot '{bot}' does not exist in the list.")
    except ValueError:
        await message.reply("Invalid input. Use /removebot <bot> format.")

# Helper function to save the updated BOT_OWNERS_AND_LOGS dictionary to environment variables
def save_bot_owners_and_logs_to_env():
    bot_owners_and_logs_json = json.dumps(BOT_OWNERS_AND_LOGS)
    os.environ["BOT_OWNERS_AND_LOGS"] = bot_owners_and_logs_json

async def main_pratheek():
    global xxx_pratheek
    async with app:
        while True:
            print("Checking...")                
            for bot in BOT_LIST:
                try:
                    ok = await app.get_users(f"@{bot}")
                    zzz_pratheek = app.get_chat_history(bot, limit=1)
                    async for ccc in zzz_pratheek:
                        bbb = ccc.id
                    if ccc.outgoing and ccc.text == "/help":
                        xxx_pratheek += f"\n\n🤖  @{bot}\n        └ **Alive** ✅"
                    else:
                        xxx_pratheek += f"\n\n🤖  @{bot}\n        └ **Down** ❌"
                except FloodWait as e:
                    await asyncio.sleep(e.x)            
            time = datetime.datetime.now(pytz.timezone(f"{TIME_ZONE}"))
            last_update = time.strftime(f"%d %b %Y at %I:%M %p")
            xxx_pratheek += f"\n\n✔️ Last checked on: {last_update} ({TIME_ZONE})\n\n**♻️ Refreshes automatically**"
            await app.edit_message_text(int(CHANNEL_ID), MESSAGE_ID, xxx_pratheek)
            print(f"Last checked on: {last_update}")   
            # Call the update_and_send_status_message() function
            await update_and_send_status_message()
        
            await asyncio.sleep(60)
                        
app.run(main_pratheek())
