import discord
import re
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN") 
GUILD_ID = 1281044586244079636 
CHANNEL_ID = 1395862969874649149 
LOG_CHANNEL_ID = 1395862969874649149 

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.messages = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.channel.id != CHANNEL_ID:
        return

    if message.author.bot and "Middle Finger Reaction Detected" in message.content:
        match = re.search(r'\*\*User:\*\* <@(\d+)> \((\d+)\)', message.content)
        if match:
            user_id = int(match.group(2))
            guild = bot.get_guild(GUILD_ID)
            member = guild.get_member(user_id)

            if member:
                try:
                    duration = timedelta(days=14)
                    await member.timeout(duration, reason="Middle Finger Reaction (Automated System Timeout)")
                    await message.add_reaction("✅")
                    print(f"✅ Timed out {member} for 14 days.")

                    # Log message
                    log_channel = bot.get_channel(LOG_CHANNEL_ID)
                    if log_channel:
                        await log_channel.send(
                            f"🔇 **Muted <@{user_id}> ({user_id}) for 14 days** due to \"Middle Finger Reaction (Automated System Timeout)\"")
                except discord.Forbidden:
                    print("❌ Missing permissions to timeout this member.")
                    log_channel = bot.get_channel(LOG_CHANNEL_ID)
                    if log_channel:
                        await log_channel.send(
                            f"❌ **Missing permissions to timeout <@{user_id}> ({user_id}).** <@&1281148981367410822> Manual Timeout Required \"?mute {user_id} 14d Middle Finger Reaction\"")
                        await message.add_reaction("❌")
                except Exception as e:
                    print(f"❌ Error timing out user: {e}")
                    if log_channel:
                        await log_channel.send(
                            f"❌ **Error timing out user <@{user_id}> ({user_id}).** <@&1281148981367410822> Manual Timeout Required \"?mute {user_id} 14d Middle Finger Reaction\"")
                        await message.add_reaction("❌")

bot.run(TOKEN)