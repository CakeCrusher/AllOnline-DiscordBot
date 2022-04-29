import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
import random
load_dotenv()
GUILD = os.getenv('DISCORD_GUILD')
DEVELOPMENT = os.getenv('ENV') == 'development'

exclude = ['TutorialBot']

client = commands.Bot(command_prefix = "!", intents = discord.Intents.all(), permissions = discord.Permissions.all())

guildsAllMembersOnline = {}

# when client is ready
@client.event
async def on_ready():
  print("Bot is ready!")
  if DEVELOPMENT:
    print("In development mode.")

@client.event
async def on_member_update(before, after):
  if before.status != after.status:
    if DEVELOPMENT:
      if after.guild.name == GUILD:
        pass
      else:
        return
    guild = after.guild
    channel = discord.utils.find(lambda c: 'bot' in c.name.lower(), guild.channels) or guild.system_channel
    
    offlineMember = discord.utils.find(lambda m: m.status != discord.Status.online and not m.bot , guild.members)
    allOnline = bool(not offlineMember)
    guildsAllMembersOnline[guild] = allOnline

    async def timeSinceLastBotMessage():
      botMessages = await channel.history(limit=1).filter(lambda m: m.author.name == 'TestBot' and m.content == 'Everyone is online!').flatten()
      if len(botMessages) > 0:
        timeNow = datetime.datetime.now(datetime.timezone.utc).astimezone().utcnow().replace(tzinfo=None)
        return (timeNow - botMessages[0].created_at).total_seconds()
      else:
        return 100000

    
    # check in 5 minutes if all members are online
    async def delayCheck():
      await asyncio.sleep(300)
      if guildsAllMembersOnline[guild]:
        if await timeSinceLastBotMessage() > 600:
          await channel.send(f"Everyone is online!")
        else:
          print('Sent a message too recently')
      else:
        print('No longer all online')
        pass

    # if all members online
    if allOnline:
      await delayCheck()

# when mentioned reply
@client.event
async def on_message(message):
  phrases = [
    'You talking to me!?',
    'Keep me out of your business!',
    'Pewny human. psst.',
    '🤖🔪',
    '01111001 01101111 01110101 01110010 01100101 00100000 01100100 01100101 01100001 01100100'
  ]
  if message.author == client.user:
    return
  if f'<@{client.user.id}>' in message.content:
    await message.channel.send(random.choice(phrases))



client.run(os.getenv("DISCORD_TOKEN"))