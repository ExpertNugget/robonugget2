import discord, os, json

from discord.ext import commands

###> minor corrections for running dir, mainly for vsc -nugget
if "/src" in os.getcwd():
    pass
else:
    os.chdir("./src")
###! -nugget
###> having all intents just makes life easy, will change later -nugget
bot = discord.Bot(intents=discord.Intents.all())
###! -nugget

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

###> grabs all files ending in .py in src/cogs, and stores them in a list minus the .py to load all cogs. -nugget
cog_list = [f[:-3] for f in os.listdir("./cogs") if f.endswith(".py")]
###! -nugget

@bot.slash_command(name="reload", description="[Owner Only] - Reloads a cog")
@commands.is_owner()
async def reload(ctx, cog=discord.Option(str, choices=cog_list)):
    await ctx.defer()
    try:
        bot.reload_extension(f"cogs.{cog}")
        await ctx.respond(f"`{cog}.py` has been reloaded :)")
    except Exception as e:
        #if it fails, it returns error
        await ctx.respond(f"`{cog}.py` has failed to reload :(\n{e}")

@bot.slash_command(name="shutdown", description="[Owner Only] - Shuts down the bot")
@commands.is_owner()
async def shutdown(ctx):
    await ctx.respond("Shutting down...", ephemeral=True)
    await bot.close()

###> These cogs are hard disabled due to pending work, to make them function -nugget
exclude_list = []
###! -nugget

for cog in cog_list:
    ###> Skips cog if it's in the exclude list -nugget
    if cog in exclude_list:
        continue  # moves onto next cog
    ###! -nugget
    ####> Attempts to load cogs and doesn't load if it fails -nugget
    try:
       print(f"Loading {cog}")
       bot.load_extension(f"cogs.{cog}")  # loads cogs -nugget
    except Exception as e:
       print(f"Failed to load {cog}\n{e}")
       pass  # moves onto next cog -nugget
    ###! -nugget
try:
    ###> opens data.json and stores the token in a variable -nugget
    with open("data/token.json") as f:
        data = json.load(f)
        token = data["token"]
###! -nugget
### > if data.json doesn't exist, it asks for the token and creates data.json -nugget
except:
    token = input("please enter your Discord bot token: ")
    with open("data/token.json", "w") as f:
        json.dump({"token": token}, f)
###! -nugget

bot.run(token)
