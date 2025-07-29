import discord
import re
from datetime import timedelta
from dotenv import load_dotenv
import os
from discord.ext import commands
import asyncio

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
GUILD_ID = 1281044586244079636

LOGS_CHANNEL_ID = 1396679018430074951
MFINGER_CHANNEL_ID = 1395862969874649149
POST_CHANNEL_ID = 1387607135675748414
INTERVIEW_RESPONSES_CHANNEL_ID = 1399853770451718204

CREATOR_ROLE_ID = 1387605514946478080
CREATOR_PING_ROLE_ID = 1387647177416769670
EMERGENCY_ROLE_ID = 1281148981367410822
TRIAL_MODERATOR_ROLE_ID = 1377649082755190804
HEAD_MODERATOR_ROLE_ID = 1287596206104641596
ADMINISTRATOR_ROLE_ID = 1287596206104641596
SENIOR_ADMINISTRATOR_ROLE_ID = 1287429827623649331
HEAD_ADMINISTRATOR_ROLE_ID = 1378039379431264450
COMMUNITY_MANAGER_ROLE_ID = 1323338117838798930
CO_FOUNDER_ROLE_ID = 1282081387649830963
PHOLECTIFY_ROLE_ID = 1282081387649830963

intents = discord.Intents.all()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='.', intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    print(f'✅ Online as {bot.user}')
    guild = bot.get_guild(GUILD_ID)
    member_count = guild.member_count
    activity = discord.Activity(type=discord.ActivityType.watching, name=f"{member_count} members in .gg/beetleshelp")
    await bot.change_presence(activity=activity)

    log_channel = bot.get_channel(LOGS_CHANNEL_ID)
    try:
        if log_channel:
            await log_channel.send("Good morning, I am awake. ☀️ || <@679810887518781495> ||")
    except:
        print("❌ Unable to send startup message.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Middle Finger Auto Timeout
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
                            await log_channel.send(
                                f"❌ **Missing permissions to timeout <@{user_id}> ({user_id}).** <@&{EMERGENCY_ROLE_ID}> Manual Timeout Required \"?mute {user_id} 14d Middle Finger Reaction\"")
                            await message.add_reaction("❌")
                    except Exception as e:
                        print(f"❌ Error timing out user: {e}")
                        if log_channel:
                            await log_channel.send(
                                f"❌ **Error timing out user <@{user_id}> ({user_id}).** <@&{EMERGENCY_ROLE_ID}> Manual Timeout Required \"?mute {user_id} 14d Middle Finger Reaction\"")
                            await message.add_reaction("❌")

    await bot.process_commands(message)


def has_any_role(*role_ids):
    def predicate(ctx):
        return any(role.id in role_ids for role in ctx.author.roles)
    return commands.check(predicate)

# unknown command handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

# .post Command
@bot.command()
@commands.has_role(CREATOR_ROLE_ID)
async def post(ctx, *, content: str):
    if ctx.channel.id == POST_CHANNEL_ID:
        formatted_content = content.strip()
        await ctx.message.delete()
        formatted_message = f"<@&{CREATOR_PING_ROLE_ID}>\n# <@{ctx.message.author.id}>\n**has posted a new video:**\n\n{formatted_content}"
        await ctx.send(formatted_message)
    else:
        return


@post.error
async def post_error(ctx, error):
    logs_channel = bot.get_channel(LOGS_CHANNEL_ID)
    try:
        if isinstance(error, commands.MissingRole):
            error_msg = await ctx.send("🚫 You do not have permission to use this.")
        elif isinstance(error, commands.MissingRequiredArgument):
            error_msg = await ctx.send("⚠️ Usage: `.post <message>`")
        else:
            error_msg = await ctx.send(f"❌ Error: {error}")
            if logs_channel:
                await logs_channel.send(
                    f"❌ Error in <#{ctx.channel.id}>:\n`{str(error)}`"
                )
        await asyncio.sleep(60)
        await error_msg.delete()
    except Exception as e:
        print(f"Error during error handling: {e}")
    await ctx.message.delete()

# .nopingpost Command
@bot.command()
@commands.has_role(CREATOR_ROLE_ID)
async def nopingpost(ctx, *, content: str):
    if ctx.channel.id == POST_CHANNEL_ID:
        formatted_content = content.strip()
        await ctx.message.delete()
        formatted_message = f"# <@{ctx.message.author.id}>\n**has posted a new video:**\n\n{formatted_content}"
        await ctx.send(formatted_message)
    else:
        return


@nopingpost.error
async def nopingpost_error(ctx, error):
    logs_channel = bot.get_channel(LOGS_CHANNEL_ID)
    try:
        if isinstance(error, commands.MissingRole):
            error_msg = await ctx.send("🚫 You do not have permission to use this.")
        elif isinstance(error, commands.MissingRequiredArgument):
            error_msg = await ctx.send("⚠️ Usage: `.nopingpost <message>`")
        else:
            error_msg = await ctx.send(f"❌ Error: {error}")
            if logs_channel:
                await logs_channel.send(
                    f"❌ Error in <#{ctx.channel.id}>:\n`{str(error)}`"
                )
        await asyncio.sleep(10)
        await error_msg.delete()
    except Exception as e:
        print(f"Error during error handling: {e}")
    await ctx.message.delete()

# .acceptinterview Command
@bot.command()
@has_any_role(HEAD_MODERATOR_ROLE_ID, ADMINISTRATOR_ROLE_ID, SENIOR_ADMINISTRATOR_ROLE_ID, HEAD_ADMINISTRATOR_ROLE_ID, COMMUNITY_MANAGER_ROLE_ID, CO_FOUNDER_ROLE_ID, PHOLECTIFY_ROLE_ID)
async def acceptinterview(ctx, user_id: int, *, content: str):
    if ctx.channel.id != INTERVIEW_RESPONSES_CHANNEL_ID:
        return 
    
    try:
        member = await ctx.guild.fetch_member(user_id)
    except discord.NotFound:
        msg = await ctx.send("❌ That user isn't in the server.")
        await ctx.message.delete()
        await asyncio.sleep(5)
        await msg.delete()
        return
    except discord.HTTPException:
        msg = await ctx.send("⚠️ Failed to fetch user. Try again later.")
        await ctx.message.delete()
        await asyncio.sleep(5)
        await msg.delete()
        return
    
    if not member:
        msg = await ctx.send("❌ That user isn't in the server.")
        await ctx.message.delete()
        await asyncio.sleep(5)
        await msg.delete()
        return

    trial_mod_role = ctx.guild.get_role(TRIAL_MODERATOR_ROLE_ID)
    if not trial_mod_role:
        msg = await ctx.send("⚠️ Trial Moderator role not found.")
        await ctx.message.delete()
        await asyncio.sleep(5)
        await msg.delete()
        return

    try:
        await member.add_roles(trial_mod_role)
    except discord.Forbidden:
        msg = await ctx.send("🚫 I do not have permission to give that role.")
        await ctx.message.delete()
        await asyncio.sleep(5)
        await msg.delete()
        return

    formatted_content = content.strip()
    formatted_message = (
        f"# <@{user_id}> you have received an update for your Staff Team interview.\n\n"
        f"**Congratulations, you have passed** your staff team interview. Please check out "
        f"<#1399866509630767224> for your training.\n\n"
        f"**Note:** {formatted_content}"
    )
    
    await ctx.send(formatted_message)
    await ctx.message.delete()



@acceptinterview.error
async def acceptinterview_error(ctx, error):
    logs_channel = bot.get_channel(LOGS_CHANNEL_ID)
    try:
        if isinstance(error, commands.MissingRole):
            error_msg = await ctx.send("🚫 You do not have permission to use this.")
        elif isinstance(error, commands.MissingRequiredArgument):
            error_msg = await ctx.send("⚠️ Usage: `.acceptinterview <user_id> <note>`")
        else:
            error_msg = await ctx.send(f"❌ Error: {error}")
            if logs_channel:
                await logs_channel.send(
                    f"❌ Error in <#{ctx.channel.id}>:\n`{str(error)}`"
                )
        await ctx.delete()
        await asyncio.sleep(60)
        await error_msg.delete()
    except Exception as e:
        print(f"Error during error handling: {e}")
    await ctx.message.delete()

# .denyinterview Command
@bot.command()
@has_any_role(HEAD_MODERATOR_ROLE_ID, ADMINISTRATOR_ROLE_ID, SENIOR_ADMINISTRATOR_ROLE_ID, HEAD_ADMINISTRATOR_ROLE_ID, COMMUNITY_MANAGER_ROLE_ID, CO_FOUNDER_ROLE_ID, PHOLECTIFY_ROLE_ID)
async def denyinterview(ctx, user_id, *, content: str):
    if ctx.channel.id == INTERVIEW_RESPONSES_CHANNEL_ID:
        formatted_content = content.strip()
        formatted_message = f"# <@{user_id}> you have received an update for your Staff Team interview.\n\n**Unfortunately, you have failed** your staff team interview. You can try again in **3 days.** \n\n**Reason:** {formatted_content}"
        await ctx.send(formatted_message)
        await ctx.message.delete()
    else:
        return


@denyinterview.error
async def denyinterview(ctx, error):
    logs_channel = bot.get_channel(LOGS_CHANNEL_ID)
    try:
        if isinstance(error, commands.MissingRole):
            error_msg = await ctx.send("🚫 You do not have permission to use this.")
        elif isinstance(error, commands.MissingRequiredArgument):
            error_msg = await ctx.send("⚠️ Usage: `.post <message>`")
        else:
            error_msg = await ctx.send(f"❌ Error: {error}")
            if logs_channel:
                await logs_channel.send(
                    f"❌ Error in <#{ctx.channel.id}>:\n`{str(error)}`"
                )
        await asyncio.sleep(60)
        await error_msg.delete()
    except Exception as e:
        print(f"Error during error handling: {e}")
    await ctx.message.delete()

# .purgeall Command
@bot.command()
@commands.has_permissions(administrator=True)
async def purgeall(ctx, user_id: int):
    guild = ctx.guild
    target = guild.get_member(user_id)
    log_lines = []

    command_channel = ctx.channel
    await ctx.message.delete()

    if not target:
        await ctx.send("❌ User not found.")
        return

    deleted_total = 0
    checked_channels = 0

    status_message = await ctx.send(f"🕒 Purge job for <@{user_id}> started by <@{ctx.message.author.id}>. Please wait, this can take several minutes...")

    for channel in guild.text_channels:
        if channel.permissions_for(target).send_messages:
            checked_channels += 1
            try:
                def is_target(m): return m.author.id == user_id
                deleted = await channel.purge(limit=1000, check=is_target)
                print(f"Deleted {len(deleted)} message(s) by {user_id} in {channel}")

                for msg in deleted:
                    log_lines.append(f"[#{channel.name}] {msg.created_at} - {msg.author.name}: {msg.content}")

                deleted_total += len(deleted)
            except discord.NotFound:
                print(f"❌ A message was already deleted in #{channel.name}.")
            except discord.Forbidden:
                print(f"❌ No perms in #{channel.name}")
            except Exception as e:
                print(f"⚠️ Error in #{channel.name}: {e}")

    if log_lines:
        filename = f"{user_id}.purgeall.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(log_lines))

        await status_message.delete()
        await command_channel.send(
            f"✅ Purge complete for <@{user_id}>.\n"
            f"🔍 Scanned {checked_channels} channels.\n"
            f"🗑️ Deleted {deleted_total} messages.",
            file=discord.File(fp=filename)
        )

        os.remove(filename) 
    else:
        await status_message.delete()
        await command_channel.send(
            f"✅ Purge complete for <@{user_id}>.\n"
            "🔍 Found 0 messages."
        )

@purgeall.error
async def purgeall_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("🚫 You do not have permission to use this.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Usage: `.purgeall <user_id>`")
    else:
        await ctx.send(f"❌ Error: {error}")

bot.run(TOKEN)
