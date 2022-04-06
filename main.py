from discord.ext import commands
import discord
from PyDictionary import PyDictionary
from http_exceptions import ClientException
from deep_translator import GoogleTranslator

dictionary=PyDictionary()

client = commands.Bot(
    command_prefix='$', help_command=None, status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="$help")
)


@client.event
async def on_ready():
    print("Client is now active.")

@client.event # CURRENTLY NOT WORKING
async def on_guild_join(guild):
    channel = client.get_channel(961053064150810675) #channel id here
    await channel.send("```Joined Guild Name : {}\nGuild ID : {}```", member.guild.id, member.guild.name)
@client.command()
async def servers(guild):
    channel = client.get_channel(961056847199092746)
    activeservers = client.guilds
    for guild in activeservers:
        await channel.send("```{}```".format(guild.name))
        print(guild.name)
    await channel.send("***LIST COMPLETE ^ -----------------------------------------***")

@client.command()
async def feature_request(ctx, *, args):
    channel = client.get_channel(961050242604740629) #channel id here
    await channel.send("Recommendation : \n```{}```".format(args))

    
@client.command()
async def help(ctx):
    await ctx.send("$add : Addition Command - Two Arguments")
    await ctx.send("$definition : Grab the definition of a word.")
    await ctx.send("$translate : Translate a message into a selected language!")


@client.command()
async def add(ctx, arg1, arg2):
    try:
        total = int(arg1) + int(arg2)
    except:
        await ctx.send("There was an error.")
    finally:
        await ctx.send(total)

@client.command()
async def definition(ctx, arg):
    definition_view = dictionary.meaning(arg)
    try:
        await ctx.send(definition_view)
    except:
        await ctx.send("There was an error.")
    finally:
        print("Test completed.")

@client.command()
async def serverlist(ctx):
    await ctx.send("I'm in " + str(len(client.guilds)) + " servers!")

@client.command()
async def translate(ctx, *, args):
    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author != ctx.me
    await ctx.send("What language would you like to translate to? type 'list' for all languages.")
    lang = await client.wait_for("message", check=check)
    
    langformat = format(lang.content)
    if langformat == "french":
        lang = GoogleTranslator(source='auto', target='fr').translate(args)
        await ctx.send(lang)
    elif langformat == "latin":
        lang = GoogleTranslator(source='auto', target='la').translate(args)
        await ctx.send(lang)
    elif langformat == "russian":
        lang = GoogleTranslator(source='auto', target='ru').translate(args)
        await ctx.send(lang)
    elif langformat == "german":
        lang = GoogleTranslator(source='auto', target='de').translate(args)
        await ctx.send(lang)
    elif langformat == "arabic":
        lang = GoogleTranslator(source='auto', target='ar').translate(args)
        await ctx.send(lang)
    elif langformat == "english":
        lang = GoogleTranslator(source='auto', target='en').translate(args)
        await ctx.send(lang)
    elif langformat == "list":
        await ctx.send("french, latin, russian, german, arabic, english")
    else:
        await ctx.send("Incorrect usage.")




client.run('OTYwOTUwMjIzODQzMjM3OTM5.Ykx4og.3C2MvkbeGYyub8K_e7u6_ZdWCj4')
