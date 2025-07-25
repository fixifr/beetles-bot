import discord
import re
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN") 
GUILD_ID = 1281044586244079636 
MFINGER_CHANNEL_ID = 1395862969874649149  # Middle Finger detection channel
CREATOR_CHANNEL_ID = 1387607135675748414 
POST_ROLE_ID = 1387647177416769670

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.messages = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'Online as {bot.user}')
    guild = bot.get_guild(GUILD_ID)
    member_count = guild.member_count
    activity = discord.Activity(type=discord.ActivityType.watching, name=f"{member_count} members in .gg/beetleshelp")
    await bot.change_presence(activity=activity)
    log_channel = bot.get_channel(MFINGER_CHANNEL_ID)
    try:
        if log_channel:
            pass
            await log_channel.send("|| <@679810887518781495> || Good morning, I am awake. ☀️ If you are not my developer, just ignore this message :)")
    except:
        print("❌ Unable to send startup message.")

@bot.event
async def on_message(message):
    # Middle Finger Reaction Auto Timeout
    if message.channel.id == MFINGER_CHANNEL_ID:
        if "middle finger reaction detected" in message.content.lower():
            match = re.search(r'\*\*User:\*\* <@(\d+)> \((\d+)\)', message.content)
            if match:
                user_id = int(match.group(2))
                guild = bot.get_guild(GUILD_ID)
                member = guild.get_member(user_id)

                if member:
                    log_channel = bot.get_channel(MFINGER_CHANNEL_ID)
                    try:
                        duration = timedelta(days=14)
                        await member.timeout(duration, reason="Middle Finger Reaction (Automated System Timeout)")
                        await message.add_reaction("✅")
                        print(f"✅ Timed out {member} for 14 days.")

                        if log_channel:
                            await log_channel.send(
                                f"🔇 **Muted <@{user_id}> ({user_id}) for 14 days** due to \"Middle Finger Reaction (Automated System Timeout)\"")
                    except discord.Forbidden:
                        print(f"❌ Missing permissions to timeout {user_id}")
                        if log_channel:
                            await log_channel.send(f"❌ **Missing permissions to timeout <@{user_id}> ({user_id}).** <@&1281148981367410822> Manual Timeout Required \"?mute {user_id} 14d Middle Finger Reaction\"")
                            await message.add_reaction("❌")
                    except Exception as e:
                        print(f"❌ Error timing out user: {e}")
                        if log_channel:
                            await log_channel.send(
                                f"❌ **Error timing out user <@{user_id}> ({user_id}).** <@&1281148981367410822> Manual Timeout Required \"?mute {user_id} 14d Middle Finger Reaction\"")
                            await message.add_reaction("❌")

    # Creator Commands Channel
    elif message.channel.id == CREATOR_CHANNEL_ID:
        if message.content.lower().startswith(".post "):
            content = message.content[6:].strip() 
            await message.delete()
            formatted = f"<@&{POST_ROLE_ID}>\n# {message.author.mention}\n**has posted a new video!**\n\n{content}"
            await message.channel.send(formatted)
        elif message.content.lower().startswith(".postnoping"):
            content = message.content[6:].strip() 
            await message.delete()
            formatted = f"# {message.author.mention}\n**has posted a new video!**\n\n{content}"
            await message.channel.send(formatted)

bot.run(TOKEN)
