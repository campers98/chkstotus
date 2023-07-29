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

async def main_pratheek():
    async with app:
            while True:
                print("Checking...")
                xxx_pratheek = f"📊 | 𝗟𝗜𝗩𝗘 𝗕𝗢𝗧 𝗦𝗧𝗔𝗧𝗨𝗦"
                for bot in BOT_LIST:
                    ok = await app.get_users(f"@{bots}")
                    try:
                        yyy_pratheek = await app.send_message(bot, "/start")
                        aaa = yyy_pratheek.id
                        await asyncio.sleep(10)
                        zzz_pratheek = app.get_chat_history(bot, limit = 1)
                        async for ccc in zzz_pratheek:
                            bbb = ccc.id
                        if aaa == bbb:
                            xxx_pratheek += f"\n\n🤖  @{bot}\n        └ **Down** ❌"
                            await app.send_message(LOG_ID, f"**[{ok.first_name}](tg://openmessage?user_id={ok.id}) off aagiduchii!! Seekiram on pannungaa**")
                            for bot_admin_id in BOT_ADMIN_IDS:
                                try:
                                    await app.send_message(int(bot_admin_id), f"🚨 **Beep! Beep!! @{bot} is down** ❌")
                                except Exception:
                                    pass
                            await app.read_chat_history(bot)
                        else:
                            xxx_pratheek += f"\n\n🤖  @{bot}\n        └ **Alive** ✅"
                            await app.read_chat_history(bot)
                    except FloodWait as e:
                        await asyncio.sleep(e.x)            
                time = datetime.datetime.now(pytz.timezone(f"{TIME_ZONE}"))
                last_update = time.strftime(f"%d %b %Y at %I:%M %p")
                xxx_pratheek += f"\n\n✔️ Last checked on: {last_update} ({TIME_ZONE})\n\n**♻️ Refreshes automatically - Powered By Pratheek**"
                await app.edit_message_text(int(CHANNEL_ID), MESSAGE_ID, xxx_pratheek)
                print(f"Last checked on: {last_update}")                
                await asyncio.sleep(6300)
                        
app.run(main_pratheek())
