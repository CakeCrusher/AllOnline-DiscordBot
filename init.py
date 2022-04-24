import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
load_dotenv()



client = commands.Bot(command_prefix = ">", intents = discord.Intents.all(), permissions = discord.Permissions.all())
# when client is ready
@client.event
async def on_ready():
  print("Bot is ready!")
@client.event
async def on_member_update(before, after):
  if before.status != after.status:
    guild = after.guild
    channel = guild.system_channel
    allOnline = True
    for member in guild.members:
      if member.status != discord.Status.online:
        allOnline = False
        break
    # if all members online
    if allOnline:
      channelMessages = await channel.history(limit=20).flatten()
      botMessages = []
      for message in channelMessages:
        if message.author.name == "TestBot":
          botMessages.append(message)
      # if the latest botMessage is at least 10 minutes old
      if len(botMessages) > 0:
        timeNow = datetime.datetime.now(datetime.timezone.utc).astimezone().utcnow()
        timeNow = timeNow.replace(tzinfo=None)
        messageTime = botMessages[0].created_at
        messageTime = messageTime.replace(tzinfo=None)
        if (timeNow - botMessages[0].created_at).total_seconds() > 600:
          await guild.system_channel.send(f"Everyone is online!")

client.run(os.getenv("DISCORD_TOKEN"))