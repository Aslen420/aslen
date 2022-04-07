from discord.ext import commands
import discord
from PyDictionary import PyDictionary
from http_exceptions import ClientException
from deep_translator import GoogleTranslator
from countryinfo import CountryInfo
import country_converter as coco
cc_all = coco.CountryConverter(include_obsolete=True)


dictionary=PyDictionary()

client = commands.Bot(
    command_prefix='$', help_command=None, status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="$help")
)

@client.event
async def on_ready():
    print("Client is now active.")

@client.command()
async def servers(guild):
    channel = client.get_channel(961080126232215592)
    activeservers = client.guilds
    for guild in activeservers:
        await channel.send("```{}```".format(guild.name))
        await channel.send("```{}```".format(guild.id))
        print(guild.name)
    await channel.send("***LIST COMPLETE ^ -----------------------------------------***")

@client.command()
async def feature_request(ctx, *, args):
    channel = client.get_channel(961080191294255144) #channel id here
    await channel.send("Recommendation : \n```{}```".format(args))

@client.command()
async def help(ctx):
    await ctx.send("$add : Addition Command - Two Arguments")
    await ctx.send("$definition : Grab the definition of a word.")
    await ctx.send("$translate : Translate a message into a selected language!")
    await ctx.send("$feature_request : Request a feature to be added")
    await ctx.send("$serverlist : Show the amount of servers the bot is in")

@client.command()
async def add(ctx, arg1, arg2):
    try:
        total = int(arg1) + int(arg2)
    except:
        await ctx.send("There was an error.")
    finally:
        await ctx.send(total)

@client.command()
async def definition(ctx, *, args):
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

@client.command()
async def country(ctx, arg1, arg2):
    country = CountryInfo(arg1)
    if arg1 == "help":
        await ctx.send("usage: $country country option")
        await ctx.send("option 1: borders")
        await ctx.send("option 2: provinces")
        await ctx.send("option 3: capital")
        await ctx.send("option 4: area (shows the area in km²)")
        await ctx.send("option 5: languages")
    elif arg2 == "languages":
        countrymod = country.languages()
        new_lst=(', '.join(countrymod)) 
        await ctx.send(new_lst)
    elif  arg2 == "borders":
        countrymod = country.borders() 
        countryfin = cc_all.convert(countrymod, to='name_short')
        await ctx.send(countryfin)
    elif arg2 == "provinces":
        countrymod = country.provinces()
        new_lst=(', '.join(countrymod)) 
        await ctx.send(new_lst)
    elif arg2 == "area":
        countrymod = country.area()
        await ctx.send("{} km²".format(countrymod))
    elif  arg2 == "capital":
        countrymod = country.capital()
        await ctx.send(countrymod)
    else:
        await ctx.send("Type $country help for more information")


client.run('token')
