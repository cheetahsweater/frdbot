import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import os
import json
from json import JSONDecodeError
import math
import random
from scipy.optimize import newton

status = "Ableton Live 20 (now costs $1000 per upgrade)"
#status = "Testing new features!"
versionnum = "1.2"
updatetime = "2024/02/04 22:37"
changes = "**(1.2)** Updated level-up system so that XP/levels accrue slower"
path = os.getcwd()
print(f"Future Riddim Daily Bot v{versionnum}")
print(updatetime)
print("Gay")
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents=discord.Intents.default()
intents.message_content=True
client = commands.Bot(intents=intents)

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

# shoutout chatGPT for the math help
coefficients = [2459.81826343, -39.83367834, -26.84958046, 3.38057449]

def xp_for_level(level, coefs):
    return sum(coef * (level ** i) for i, coef in enumerate(coefs))

# again: shoutout chatGPT for the math help
def calculate_level(xp):
    # Define the function whose root (zero) we want to find
    def f(level):
        return xp_for_level(level, coefficients) - xp

    # Use the Newton-Raphson method to find a root, starting with an initial guess
    initial_guess = 1
    level = newton(f, initial_guess)
    return math.floor(level)  # Level should be an integer

import math

# AGAIN: shoutout chatGPT for the math help
def award_points(content):
    x = len(content)
    a, b = 1, 2000  # Message length range
    average_message_length = 75  # New average message length
    total_messages = 2000
    cumulative_xp_for_level_30 = 68375.7  # Cumulative XP needed for level 30

    # The average XP per message needed to reach level 30 after 2000 messages
    average_xp_per_message = cumulative_xp_for_level_30 / total_messages

    # We want the XP for a message of average length (75 characters) to be the average XP per message
    xp_for_average_length = average_xp_per_message

    # Calculate the XP range scale factor based on the average message length
    c, d = 8, 10  # Base XP range for the minimum and maximum message lengths
    scale_factor = xp_for_average_length / ((c + ((math.log(average_message_length + 1) - math.log(a + 1)) * (d - c)) / (math.log(b + 1) - math.log(a + 1))))

    # Adjusted XP range based on the scale factor
    c_adj = c * scale_factor
    d_adj = d * scale_factor

    # Return the XP awarded for the actual message length, scaled appropriately
    return c_adj + ((math.log(x + 1) - math.log(a + 1)) * (d_adj - c_adj)) / (math.log(b + 1) - math.log(a + 1))


@client.slash_command(description="Returns a @futureriddimdaily server invite link",guild_ids=[1172027590287052811])
async def invite(ctx): 
    await ctx.respond("🩵**Get your friends in here!!**🩷\n*Discord Invite* :: https://discord.gg/kTWTkgRf5M")

@client.slash_command(description="Returns version number, date/time, and changelog (for nerds)",guild_ids=[1172027590287052811])
async def version(ctx): 
    await ctx.respond(f"FRDBot\nVersion {versionnum}\n{updatetime}\n\n__Changelog__\n{changes}")

@client.slash_command(description="Returns @futureriddimdaily contact info as seen in the info/rules channel",guild_ids=[1172027590287052811])
async def info(ctx): 
    await ctx.respond("**Contact** :: futureriddimdaily@gmail.com\n\n**Social Media**\n—Discord :: frdcustomerservice (FRDCS)\n—Instagram :: <https://instagram.com/futureriddimdaily> (you better be following ngl...)\n—Spotify :: <https://open.spotify.com/user/31anncfkcfhwwgkikryejjrefrty?si=700059a96b024d82>")

@client.slash_command(description="Returns the rules as seen in the info/rules channel",guild_ids=[1172027590287052811])
async def rules(ctx): 
    await ctx.respond(":notebook:RULES:notebook:\n**—1). Respect everyone...** :: *Bullying and harrasment cannot be tolerated. Hate and/or bigotry toward any race, identity, religion, etc. cannot be tolerated.*\n**—2). Please, be normal...** ::  *Refrain from posting media which is NSFW, violent/gory or otherwise disturbing. Refrain from unwarranted mentions of explicit and/or discomforting topics such as self-harm, sex/fetishes, suicide, etc. Just don't be a goddamn weirdo man, seriously...*\n**—3). Respect the mods...** :: *Mods are here to accentuate your good experience here in the server- and are human, too. They will intervene and may take actions when necessary. If you are issued a penalty or ban, please trust that we have done our duty properly and proceed accordingly.*\n**—4). No spam of ANY kind...** :: *Do not tag anyone excessively, do not spam voice or text chats, do not promote your own work or product/service excessively. ('Networking' isn't necessarily discouraged but tread lightly...)*\n**—5). Use the server properly...** :: *Maintain a level of contingency when conversing in channels. Be sure to abide by each channel's topic and rules.*")

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
                msg = random.choice(range(1,7))
                if msg == 1:
                    await message.channel.send(f"<:frdCaption1:1173323899539308754> if true: <@{message.author.id}> has reached level {curlevel}")
                if msg == 2:
                    await message.channel.send(f"OMG! <@{message.author.id}> leveled up! They are now level {curlevel}!")
                if msg == 3:
                    await message.channel.send(f"Holy Smokes!! <@{message.author.id}> leveled up and is now level {curlevel}!")
                if msg == 4:
                    await message.channel.send(f"Yooo... <@{message.author.id}> just leveled up! They are now level {curlevel}...")
                if msg == 5:
                    await message.channel.send(f"A... <@{message.author.id}> just leveled up! 👀 Congrats on level {curlevel} #gang <:frdSoldier1:1173165919036506124>")
                if msg == 6:
                    await message.channel.send(f"<@{message.author.id}> was spotted <:frdSpotted1:1173129330667311197> leveling up! They are now level {curlevel}! ")
            levels[str(message.author.id)] = calculate_level(frd[str(message.author.id)])
        except KeyError:
            levels[str(message.author.id)] = calculate_level(frd[str(message.author.id)])
        with open(f"{path}\\assets\\levels.json", "w") as file:
            file.write(json.dumps(levels))
            file.close()

client.run(TOKEN)