import discord 
from discord.ext import commands
import logging
import os 
from dotenv import load_dotenv
import requests


load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


handler = logging.FileHandler(filename="discord.log", encoding='utf-8', mode = 'w')
intents = discord.Intents.default()
intents.message_content = True 
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents) # using ! to talk to bot

@bot.event
async def on_ready():
    print(f"Bot is ready: {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f'Welcome to the server {member.name}')

@bot.command()
async def rank(ctx, arg):
    url = f"https://api.wynncraft.com/v3/player/{arg}"
    response = requests.get(url)
    data = response.json()
    playtime = int(data["playtime"])

    if playtime < 100:
        await ctx.send(f"You still kinda have a life you have {playtime} hours played")
    else:
        await ctx.send(f"You have no life get off wynncraft and get a job you {playtime} degen")

@bot.command()
async def quest(ctx, arg):
    url = f"https://api.wynncraft.com/v3/player/{arg}"
    response = requests.get(url)
    data = response.json()
    quest = data["globalData"]["completedQuests"]
    await ctx.send(f"You have completed {quest} quests")

@bot.command()
async def level(ctx, arg):
    url = f"https://api.wynncraft.com/v3/player/{arg}/characters"
    response = requests.get(url)
    data = response.json()
    for id in data:
        classType = data[id]["type"]
        lvl = data[id]["level"]
        await ctx.send(f"{classType} Level: {lvl}")

@bot.command()
async def profession(ctx, arg):
    url = f"https://api.wynncraft.com/v3/player/{arg}/characters"
    response = requests.get(url)
    data = response.json()

    highest_level_id = ""
    highest_level = 0

    for id in data:
        lvl = data[id]["level"]
        if data[id]["level"] > highest_level:
            highest_level = lvl
            highest_level_id = id


    url = f"https://api.wynncraft.com/v3/player/{arg}/characters/{highest_level_id}"
    response = requests.get(url)
    data = response.json()
    for p in data["professions"]:
        level = data['professions'][p]['level']
        await ctx.send(f"You are level {level} in {p}")

bot.run(DISCORD_TOKEN, log_handler=handler, log_level=logging.DEBUG)
