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
    xxx_pratheek = "】★ | ▄︻デ ᑗŇƗV€ŘŞ€═一【 Ⴆσƚs • ⃤• ƗŇ₣Ø 】 | ★【"

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
                xxx_pratheek += f"\n\n🤡  @{bot}\n        ⇃➫ **─═ 🅒🅛🅞🅢🅔 ═─** 💔"
            else:
                xxx_pratheek += f"\n\n🤡  @{bot}\n        ⇃➫ **↬【 ƠƤЄƝ 】↫**  📂"
        except FloodWait as e:
            # Sleep based on the recommended delay from the FloodWait exception
            await asyncio.sleep(e.x)
        except Exception as e:
            # Log any errors for debugging purposes
            print(f"Error checking bot status for {bot}: {e}")

    time = datetime.datetime.now(pytz.timezone(f"{TIME_ZONE}"))
    last_update = time.strftime(f"%d %b %Y at %I:%M %p")
    xxx_pratheek += f"\n\n🆗🧘‍♂️ Fi͠n͠a͠l͠ ͠Up͠d͠a͠t͠i͠o͠n͠ ͠oN͠ : {last_update} ({TIME_ZONE})\n\n**🥶 🇷‌🇪‌🇧‌🇴‌🇴‌🇹‌🇸‌ 🇪‌🇻‌🇪‌🇷‌🇾‌ 1̳2̳0̳  🇸‌🇪‌🇨‌**"

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
        xxx_pratheek += f"\n\n🤡  @{bot}\n        ⇃➫ **─═ 🅒🅛🅞🅢🅔 ═─** 💔"  # Assume the bot is down initially

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

async def main_pratheek():
    global xxx_pratheek
    async with app:
        while True:
            print("Checking...")
            
            # Reset the xxx_pratheek variable before checking the status of each bot
            xxx_pratheek = "】★ | ▄︻デ ᑗŇƗV€ŘŞ€═一【 Ⴆσƚs • ⃤• ƗŇ₣Ø 】 | ★【"

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
                        xxx_pratheek += f"\n\n🤡  @{bot}\n        ⇃➫ **─═ 🅒🅛🅞🅢🅔 ═─** 💔"
                        owner_id = info["owner_id"]
                        log_group_id = info["log_group_id"]
                        if owner_id and log_group_id:
                            # Send a message to the bot's owner
                            await send_message_to_chat(owner_id, f"✪ 🅰🅻🅴🆁🆃 ✪ 𝓛𝓮𝔂 𝐢𝐧𝐠𝐚 𝐯𝐚𝐧𝐠𝐚 @{bot} 𝘾𝙡𝙤𝙨𝙚𝙚𝙙! 𝐎𝐝𝐢𝐲𝐚 𝐨𝐝𝐢𝐲𝐚")

                            # Send a message to the bot's log group
                            await send_message_to_chat(log_group_id, f"✪ 🅰🅻🅴🆁🆃 ✪ 𝓛𝓮𝔂 𝐢𝐧𝐠𝐚 𝐯𝐚𝐧𝐠𝐚 @{bot} 𝘾𝙡𝙤𝙨𝙚𝙚𝙙!  𝐎𝐝𝐢𝐲𝐚 𝐨𝐝𝐢𝐲𝐚")
                        if LOG_ID:
                            await send_message_to_chat(LOG_ID, f"@{bot} is down!")
                    else:
                        xxx_pratheek += f"\n\n🤡  @{bot}\n        ⇃➫ **↬【 ƠƤЄƝ 】↫**  📂"
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                except Exception as e:
                    print(f"Error checking bot status for {bot}: {e}")

            time = datetime.datetime.now(pytz.timezone(f"{TIME_ZONE}"))
            last_update = time.strftime(f"%d %b %Y at %I:%M %p")
            xxx_pratheek += f"\n\n🆗🧘‍♂️ Fi͠n͠a͠l͠ ͠Up͠d͠a͠t͠i͠o͠n͠ ͠oN͠ : {last_update} ({TIME_ZONE})\n\n**🥶 🇷‌🇪‌🇧‌🇴‌🇴‌🇹‌🇸‌ 🇪‌🇻‌🇪‌🇷‌🇾‌ 1̳2̳0̳  🇸‌🇪‌🇨**"
            
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

            await asyncio.sleep(120)
                        
app.run(main_pratheek())
