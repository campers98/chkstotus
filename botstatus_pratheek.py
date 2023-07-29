from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import asyncio
import datetime
import pytz
import os
from dotenv import load_dotenv

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

async def send_message_to_chat(chat_id, message):
    if chat_id:
        try:
            await app.send_message(chat_id, message)
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")

async def main_pratheek():
    async with app:
            while True:
                print("Checking...")
                xxx_pratheek = f"📊 | 𝗟𝗜𝗩𝗘 𝗕𝗢𝗧 𝗦𝗧𝗔𝗧𝗨𝗦"
                for bot in BOT_LIST:
                    ok = await app.get_users(f"@{bot}")
                    try:
                        yyy_pratheek = await app.send_message(bot, "/start")
                        aaa = yyy_pratheek.id
                        await asyncio.sleep(2)
                        zzz_pratheek = app.get_chat_history(bot, limit = 1)
                        async for ccc in zzz_pratheek:
                            bbb = ccc.id
                        if aaa == bbb:
                            xxx_pratheek += f"\n\n🤖  @{bot}\n        └ **Down** ❌"
                            bot_data = BOT_OWNERS_AND_LOGS.get(bot)
                            if bot_data:
                                bot_owner_id = bot_data.get("owner_id")
                                log_group_id = bot_data.get("log_group_id")
        
                                if bot_owner_id:        
                                    # Send message to the bot owner
                                    bot_owner_message = f"🚨 **Beep! Beep!! @{bot} is down** ❌"
                                    await send_message_to_chat(bot_owner_id, bot_owner_message)
                                
                                if log_group_id:
                                    # Send message to the log group
                                    log_group_message = f"🚨 **@{bot} is down** ❌"
                                    await send_message_to_chat(log_group_id, log_group_message)

                                # Send message to the common log group
                                common_log_group_id = BOT_OWNERS_AND_LOGS.get("common", {}).get("log_group_id")
                                if common_log_group_id:
                                    common_log_group_message = f"🚨 **@{bot} is down** ❌"
                                    await send_message_to_chat(common_log_group_id, common_log_group_message)                                
        
                            await app.read_chat_history(bot)
                        else:
                            xxx_pratheek += f"\n\n🤖  @{bot}\n        └ **Alive** ✅"
                            await app.read_chat_history(bot)
                    except FloodWait as e:
                        await asyncio.sleep(e.x)            
                time = datetime.datetime.now(pytz.timezone(f"{TIME_ZONE}"))
                last_update = time.strftime(f"%d %b %Y at %I:%M %p")
                xxx_pratheek += f"\n\n✔️ Last checked on: {last_update} ({TIME_ZONE})\n\n**♻️ Refreshes automatically**"
                await app.edit_message_text(int(CHANNEL_ID), MESSAGE_ID, xxx_pratheek)
                print(f"Last checked on: {last_update}")                
                await asyncio.sleep(60)
                        
app.run(main_pratheek())
