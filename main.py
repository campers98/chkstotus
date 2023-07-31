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
#BOT_LIST = [i.strip() for i in os.getenv("BOT_LIST").split(' ')]
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
MESSAGE_ID = int(os.getenv("MESSAGE_ID"))
BOT_ADMIN_IDS = [int(i.strip()) for i in os.getenv("BOT_ADMIN_IDS").split(' ')]
LOG_ID = int(os.getenv("LOG_ID"))

# Dictionary to store bot owner and log group associations
BOT_OWNERS_AND_LOGS = {
    #"Divu1_bot": {"owner_id": 5276467211, "log_group_id": -1001686570455}, # Add more bots and their corresponding owner_id and log_group_id
    #"Isai_mazhai_bot": {"owner_id": 655594746, "log_group_id": -1001975251757}, # Add more bots and their corresponding owner_id and log_group_id
    #"common": {"log_group_id": -1001600523208},  # Add the common log group ID here    
}

# Global variable to hold the status message
xxx_pratheek = ""

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
    global xxx_pratheek
    xxx_pratheek = "📊 | 𝗟𝗜𝗩𝗘 𝗕𝗢𝗧 𝗦𝗧𝗔𝗧𝗨𝗦"

    for bot in BOT_OWNERS_AND_LOGS:
        try:
            # Send the /help command to the bot
            yyy_pratheek = await app.send_message(bot, "/help")
            aaa = yyy_pratheek.id
            
            # Wait for a short time to allow the bot to respond
            await asyncio.sleep(2)
            
            async for ccc in app.get_chat_history(bot, limit=1):
                bbb = ccc.id

            if aaa == bbb:
                xxx_pratheek += f"\n\n🤖  @{bot}\n        └ **Down** ❌"
            else:
                xxx_pratheek += f"\n\n🤖  @{bot}\n        └ **Alive** ✅"
        except FloodWait as e:
            # Sleep based on the recommended delay from the FloodWait exception
            await asyncio.sleep(e.x)
        except Exception as e:
            # Log any errors for debugging purposes
            print(f"Error checking bot status for {bot}: {e}")

    time = datetime.datetime.now(pytz.timezone(f"{TIME_ZONE}"))
    last_update = time.strftime(f"%d %b %Y at %I:%M %p")
    xxx_pratheek += f"\n\n✔️ Last checked on: {last_update} ({TIME_ZONE})\n\n**♻️ Refreshes automatically**"

    try:
        # Convert CHANNEL_ID and MESSAGE_ID to integers if provided as strings
        channel_id_int = int(CHANNEL_ID)
        message_id_int = int(MESSAGE_ID)
        
        # Update the status message in the channel
        await app.edit_message_text(channel_id_int, message_id_int, xxx_pratheek)
        print(f"Last checked on: {last_update}")
    except Exception as e:
        # Log any errors for debugging purposes
        print(f"Error updating status message: {e}")

async def send_message_to_chat(chat_id, message):
    if chat_id:
        try:
            await app.send_message(chat_id, message)
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")

# Add a command handler to dynamically add bots and their owner IDs and log group IDs
@app.on_message(filters.command("addbot") & filters.chat(LOG_ID) & filters.group)
async def add_bot_handler(client: Client, message: types.Message):
    print("add_bot_handler called!")  # Add this line to check if the function is called
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

        # Save the updated dictionary to the JSON file
        save_bot_owners_and_logs_to_file(BOT_OWNERS_AND_LOGS_FILE, BOT_OWNERS_AND_LOGS)

        # Update the status message with the newly added bot
        xxx_pratheek += f"\n\n🤖  @{bot}\n        └ **Down** ❌"  # Assume the bot is down initially

        # Update the status message and send it to the channel
        await update_and_send_status_message()

        # Reply with a success message
        await message.reply(f"Added {bot} with owner ID: {owner_id} and log group ID: {log_group_id}")
    except ValueError:
        await message.reply("Invalid input. Use `/addbot bot_name owner_id log_group_id` format.")
    print("Status message after adding the bot:", xxx_pratheek)
        
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

            # Save the updated dictionary to the JSON file
            save_bot_owners_and_logs_to_file(BOT_OWNERS_AND_LOGS_FILE, BOT_OWNERS_AND_LOGS)


            # Update the status message and send it to the channel
            await update_and_send_status_message()

            await message.reply(f"Removed {bot} from the list.")
        else:
            await message.reply(f"The bot '{bot}' does not exist in the list.")
    except ValueError:
        await message.reply("Invalid input. Use `/removebot bot_name` format.")

# Command handler to list all the bots and their details
@app.on_message(filters.command("botslist") & filters.chat(LOG_ID) & filters.group)
async def list_bots(client: Client, message: types.Message):
    print("botslist_handler called!")  # Add this line to check if the function is called
    if not message.from_user.id in BOT_ADMIN_IDS:
        await message.reply("You are not authorized to access the bots list.")
        return

    if not BOT_OWNERS_AND_LOGS:
        await message.reply("No bots have been added to the list yet.")
        return

    response = "**List of Bots and their Details:**\n"
    for bot, info in BOT_OWNERS_AND_LOGS.items():
        owner_id = info["owner_id"]  # Assuming owner_id is always present
        log_group_id = info["log_group_id"]  # Assuming log_group_id is always present
        response += f"\nBot: {bot}\nOwner ID: {owner_id}\nLog Group ID: {log_group_id}\n"

    await message.reply(response)
    # Add a print statement for confirmation
    print(f"/botslist command invoked by user {message.from_user.id} in group {message.chat.id}")

@app.on_message(filters.command("test"))
async def test_command(client: Client, message: types.Message):
    print(f"/test command invoked by user {message.from_user.id} in group {message.chat.id}")
    await message.reply("Test command received.")

# Function to calculate the uptime and downtime of each bot
async def calculate_uptime_and_downtime():
    bot_uptime_data = {}
    for bot, info in BOT_OWNERS_AND_LOGS.items():
        try:
            yyy_pratheek = await app.send_message(bot, "/help")
            aaa = yyy_pratheek.id
            await asyncio.sleep(2)
            zzz_pratheek = [ccc async for ccc in app.get_chat_history(bot, limit=1)]  # Collect items as a list
            bbb = zzz_pratheek[0].id if zzz_pratheek else None
            if aaa == bbb:
                bot_uptime_data[bot] = {"status": "down", "downtime": []}
            else:
                bot_uptime_data[bot] = {"status": "up", "uptime": []}
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            print(f"Error checking bot status for {bot}: {e}")
    return bot_uptime_data

async def main_pratheek():
    global xxx_pratheek
    async with app:
        while True:
            print("Checking...")
            bot_uptime_data = await calculate_uptime_and_downtime()
            
            # Reset the xxx_pratheek variable before checking the status of each bot
            xxx_pratheek = "📊 | 𝗟𝗜𝗩𝗘 𝗕𝗢𝗧 𝗦𝗧𝗔𝗧𝗨𝗦"

            # Loop through BOT_OWNERS_AND_LOGS to check the status of each bot
            for bot, info in BOT_OWNERS_AND_LOGS.items():
                try:
                    yyy_pratheek = await app.send_message(bot, "/help")
                    aaa = yyy_pratheek.id
                    await asyncio.sleep(2)
                    zzz_pratheek = app.get_chat_history(bot, limit=1)
                    async for ccc in zzz_pratheek:
                        bbb = ccc.id
                    if aaa == bbb:
                        xxx_pratheek += f"\n\n🤖  @{bot}\n        └ **Down** ❌"
                        owner_id = info["owner_id"]
                        log_group_id = info["log_group_id"]
                        if owner_id and log_group_id:
                            # Send a message to the bot's owner
                            await send_message_to_chat(owner_id, f"Your bot @{bot} is down!")

                            # Send a message to the bot's log group
                            await send_message_to_chat(log_group_id, f"Bot @{bot} is down!")
                        if LOG_ID:
                            await send_message_to_chat(LOG_ID, f"@{bot} is down!")
                    else:
                        xxx_pratheek += f"\n\n🤖  @{bot}\n        └ **Alive** ✅"
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                except Exception as e:
                    print(f"Error checking bot status for {bot}: {e}")

            time = datetime.datetime.now(pytz.timezone(f"{TIME_ZONE}"))
            last_update = time.strftime(f"%d %b %Y at %I:%M %p")
            xxx_pratheek += f"\n\n✔️ Last checked on: {last_update} ({TIME_ZONE})\n\n**♻️ Refreshes automatically**"
            
            try:
                # Convert CHANNEL_ID and MESSAGE_ID to integers if provided as strings
                channel_id_int = int(CHANNEL_ID)
                message_id_int = int(MESSAGE_ID)
                
                # Update the status message in the channel
                await app.edit_message_text(channel_id_int, message_id_int, xxx_pratheek)
                print(f"Last checked on: {last_update}")
            except Exception as e:
                # Log any errors for debugging purposes
                print(f"Error updating status message: {e}")

            # Send daily status report to LOG_ID group
            if LOG_ID:
                daily_status_report = f"📅 Daily Status Report - {last_update}\n"
                for bot, data in bot_uptime_data.items():
                    status = data["status"]
                    if status == "down":
                        downtime_periods = data["downtime"]
                        report = f"\n🤖 @{bot} was down at the following times:\n"
                        for start, end in downtime_periods:
                            report += f"  - From: {start} To: {end}\n"
                        daily_status_report += report
                    else:
                        daily_status_report += f"\n🤖 @{bot} is up and running.\n"
                await send_message_to_chat(LOG_ID, daily_status_report)

            await asyncio.sleep(300)  # Sleep for 24 hours (86400 seconds)

            await asyncio.sleep(120)
                        
app.run(main_pratheek())
