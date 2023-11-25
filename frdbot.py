import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import os
import json
from json import JSONDecodeError
import math

status = "Ableton Live 22 (now costs $1000 per upgrade)"
#status = "Testing new features!"
version = "Alpha 1.0"
updatetime = "2023/11/25 06:20"
changes = "(Alpha 1.0) Created bot"
path = os.getcwd()
print(f"Awesomeness Bot v{version}")
print(updatetime)
print("Gay")
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents=discord.Intents.default()
intents.message_content=True
client = discord.Client(intents=intents)

try:
    with open(f"{path}\\assets\\frd.json", "r") as file:
        frd = json.loads(file.read())
        file.close()
except FileNotFoundError:
    with open(f"{path}\\assets\\frd.json", "w") as file:
        frd = {}
        file.close()
except JSONDecodeError:
    print(JSONDecodeError)
    frd = {}
    file.close()
    pass

try:
    with open(f"{path}\\assets\\levels.json", "r") as file:
        levels = json.loads(file.read())
        file.close()
except FileNotFoundError:
    with open(f"{path}\\assets\\levels.json", "w") as file:
        levels = {}
        file.close()
except JSONDecodeError:
    print(JSONDecodeError)
    levels = {}
    file.close()
    pass

def calculate_level(xp):
    return math.floor(math.sqrt(5 * xp + 5625) / 5 - 15)

def award_points(content):
    x = len(content)
    a, b = 0, 2000  #Message length range
    c, d = 8, 10    #XP range
    return c + ((math.log(x + 1) - math.log(a + 1)) * (d - c)) / (math.log(b + 1) - math.log(a + 1))

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"{status}"))
    print('Bot is online!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        try:
            frd[str(message.author.id)] = frd[str(message.author.id)] + award_points(message.content)
        except KeyError:
            frd[str(message.author.id)] = award_points(message.content)
        with open(f"{path}\\assets\\frd.json", "w") as file:
            file.write(json.dumps(frd))
            file.close()
        try:
            prevlevel = levels[str(message.author.id)]
            curlevel = calculate_level(frd[str(message.author.id)])
            if prevlevel != curlevel:
                if curlevel == 33:
                    try:
                        role = get(message.guild.roles, id=1172433064836739092)
                    except Exception as e:
                        await message.channel.send(e)
                    try:
                        await message.author.add_roles(role)
                    except Exception as e:
                        await message.channel.send(e) #DEBUG
                await message.channel.send(f"<:frdCaption1:1173323899539308754> if true: <@{message.author.id}> has reached level {curlevel} <:frdSoldier1:1173165919036506124>")
            levels[str(message.author.id)] = curlevel
        except KeyError:
            levels[str(message.author.id)] = curlevel
        with open(f"{path}\\assets\\levels.json", "w") as file:
            file.write(json.dumps(levels))
            file.close()

client.run(TOKEN)