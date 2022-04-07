from discord.ext import commands
import discord
from PyDictionary import PyDictionary
from http_exceptions import ClientException
from deep_translator import GoogleTranslator
from countryinfo import CountryInfo
import country_converter as coco
from udpy import UrbanClient
cc_all = coco.CountryConverter(include_obsolete=True)


dictionary=PyDictionary()

udclient = UrbanClient()

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
        embedVar = discord.Embed(title="Help - Commands", description="List of commands for Aslen Bot!", color=0x336EFF)
        embedVar.add_field(name="$add :", value="Addition Command - Two Arguments", inline=False)
        embedVar.add_field(name="$define :", value="Grab the definition of a word", inline=False)
        embedVar.add_field(name="$translate :", value="Translate a message into a selected language!", inline=False)
        embedVar.add_field(name="$feature_request :", value="Request a feature to be added", inline=False)
        embedVar.add_field(name="$serverlist :", value="Show the amount of servers the bot is in", inline=False)
        embedVar.add_field(name="$country :", value="Grab different information about specified countries", inline=False)
        embedVar.add_field(name="$urban :", value="Grab the urban dictionary definition of specified words | use $urban-all to show all results", inline=False)
        await ctx.send(embed=embedVar)


@client.command()
async def add(ctx, arg1, arg2):
    try:
        total = int(arg1) + int(arg2)
    except:
        await ctx.send("There was an error.")
    finally:
        await ctx.send(total)

@client.command()
async def define(ctx, *, args):
    definition_view = dictionary.meaning(args)
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
    await ctx.send("What language would you like to translate to? Use $translate-list for all languages.")
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
    else:
        await ctx.send("Incorrect usage.")

@client.command()
async def country(ctx, arg1, arg2):
    country = CountryInfo(arg1)
    if arg2 == "population":
        countrymod = country.population()
        await ctx.send(countrymod)
    elif arg2 == "region":
        countrymod = country.region()
        await ctx.send(countrymod)
    elif arg2 == "languages":
        countrymod = country.languages()
        new_lst=(', '.join(countrymod)) 
        await ctx.send(new_lst)
    elif  arg2 == "borders":
        countrymod = country.borders() 
        countryfin = cc_all.convert(countrymod, to='name')
        new_lst=(', '.join(countryfin)) 
        await ctx.send(new_lst)
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
        pass

@client.command(aliases=['translate-list'])
async def translate_list(ctx):
    await ctx.send("french, latin, russian, german, arabic, english")

@client.command(aliases=['urban-all'])
async def urban_all(ctx, *, args):
    embedFun = discord.Embed(title="Word: {}".format(args), color=0x336EFF)
    defs = udclient.get_definition(str(args))
    index = 0
    for item in defs: # Python's `for` loop is a for-each.
        embedFun.add_field(name=args, value=item.definition, inline=False)
    await ctx.send(embed=embedFun)


@client.command()
async def urban(ctx, *, args):
    embedFun = discord.Embed(title="Word: {}".format(args), color=0x336EFF)
    defs = udclient.get_definition(str(args))
    index = 0
    for item in defs: # Python's `for` loop is a for-each.
        embedFun.add_field(name=args, value=item.definition, inline=False)    # or whatever function of that item.
        await ctx.send(embed=embedFun)
        index += 1
        if index == 1:
            break    
        break
    

client.run('token')
