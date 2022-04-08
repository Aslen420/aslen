from discord.ext import commands
from discord.ext.commands import has_permissions
import discord
from PyDictionary import PyDictionary
from http_exceptions import ClientException
from deep_translator import GoogleTranslator
from countryinfo import CountryInfo
import country_converter as coco
from udpy import UrbanClient
import os
import sys
import subprocess
import pyjokes
import requests
cc_all = coco.CountryConverter(include_obsolete=True)
dictionary=PyDictionary()
udclient = UrbanClient()
client = commands.Bot(
    command_prefix='$', help_command=None, status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="$help")
)

snipe_message_author = {}
snipe_message_content = {}

@client.event
async def on_message_delete(message):
    snipe_message_author[message.channel.id] = message.author
    snipe_message_content[message.channel.id] = message.content
    await sleep(60)
    del snipe_message_author[message.channel.id]
    del snipe_message_content[message.channel.id]

@client.event
async def on_ready():
    print("Client is now active.")

@client.command(name = 'snipe')
async def snipe(ctx):
    channel = ctx.channel
    try: 
        em = discord.Embed(name = f"Last deleted message in #{channel.name}", description = snipe_message_content[channel.id])
        em.set_footer(text = f"This message was sent by {snipe_message_author[channel.id]}")
        await ctx.send(embed = em)
    except KeyError: 
        await ctx.send(f"There are no recently deleted messages in #{channel.name}")
@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, *, user_id : int):
    user = await client.fetch_user(user_id)
    await ctx.guild.ban(user)
    await ctx.send("**{0}** has been banned.".format(str(user)))
@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, user_id : int):
    user = await client.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send("**{0}** has been unbanned.".format(str(user)))
@client.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, *, user_id : int):
    user = await client.fetch_user(user_id)
    await ctx.guild.kick(user)
    await ctx.send("**{0}** has been kicked.".format(str(user)))
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
    channel = client.get_channel(961080191294255144) 
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
async def joke(ctx):
    a = requests.get("https://v2.jokeapi.dev/joke/Dark?blacklistFlags=nsfw,political,racist&format=txt")
    await ctx.send("{}".format(str(a.text)))

@client.command()
async def insult(ctx):
    ins = requests.get("https://evilinsult.com/generate_insult.php?lang=en")
    await ctx.send("**{}**".format(str(ins.text)))
@client.command()
async def add(ctx, arg1, arg2):
    try:
        total = int(arg1) + int(arg2)
    except:
        await ctx.send("There was an error.")
    finally:
        await ctx.send(total)
@client.command()
@has_permissions(manage_roles=True)
async def mkr(ctx, *, name):
	guild=ctx.guild
	await guild.create_role(name=name)
	await ctx.send(f'Role `{name}` has been created')
@client.command(pass_context=True)
async def sus(ctx, *, role_name):
    role = discord.utils.get(ctx.message.guild.roles, name=f"{role_name}")
    await role.delete()
    await ctx.send(f"[{role_name}] Has been deleted!")

@client.command(pass_context=True)
async def clean(ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.send('Cleared by {}'.format(ctx.author.mention))
        await ctx.message.delete()
@client.command()
async def define(ctx, *, args):
    definition_view = dictionary.meaning(args)
    embedFun = discord.Embed(title="Word: {}".format(args), color=0x336EFF)
    embedFun.add_field(name=args, value=definition_view, inline=False)
    try:
        await ctx.send(embed=embedFun)
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
async def pause(ctx):
    myID = 516366251484774401
    altID = 949532007279525948
    if ctx.message.author.id == myID or ctx.message.author.id == altID:
        await ctx.send("Pausing event loop...")
        pausing = input("Enter something to resume event loop : ")
    else:
        await ctx.send('You are not allowed to execute this command!')
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
    embedFun = discord.Embed(title="Word(s): {}".format(args), color=0x336EFF)
    defs = udclient.get_definition(str(args))
    index = 0
    for item in defs: 
        embedFun.add_field(name=args, value=item.definition, inline=False)
    await ctx.send(embed=embedFun)
@client.command()
async def urban(ctx, *, args):
    embedFun = discord.Embed(title="Word(s): {}".format(args), color=0x336EFF)
    defs = udclient.get_definition(str(args))
    index = 0
    for item in defs: 
        embedFun.add_field(name=args, value=item.definition, inline=False)   
        await ctx.send(embed=embedFun)
        index += 1
        if index == 10:
            break    
        break
@client.command(aliases=['client-ss'])
async def client_ss(ctx):
    myID = 516366251484774401
    altID = 949532007279525948
    if ctx.message.author.id == myID or ctx.message.author.id == altID:
        os.system("flameshot gui")
    else:
        await ctx.send('You are not allowed to execute this command!')
@client.command()
async def reload(ctx):
    await ctx.send("***Restarting...***")
    subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])


client.run('OTYxMDc4MjU4NjYzODIxMzIy.Ykzv4A.6jLDtLyh_76XzpMTPhv9e4t1VqE')


