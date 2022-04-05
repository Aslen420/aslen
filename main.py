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

@client.command()
async def help(ctx):
    await ctx.send("$add : Addition Command - Two Arguments")
    await ctx.send("$definition : Grab the definition of a word.")

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
async def translate(ctx, *, args):
    def check(message: discord.Message):
        return message.channel == ctx.channel and message.author != ctx.me
    await ctx.send("What language would you like to translate to? type 'list' for all languages.")
    lang = await client.wait_for("message", check=check)
    langformat = format(lang.content)
    if langformat == "french":
        french = GoogleTranslator(source='auto', target='fr').translate(args)
        await ctx.send(french)
    elif langformat == "latin":
        latin = GoogleTranslator(source='auto', target='la').translate(args)
        await ctx.send(latin)
    elif langformat == "russian":
        russian = GoogleTranslator(source='auto', target='ru').translate(args)
        await ctx.send(russian)
    elif langformat == "german":
        german = GoogleTranslator(source='auto', target='de').translate(args)
        await ctx.send(german)
    elif langformat == "arabic":
        arabic = GoogleTranslator(source='auto', target='ar').translate(args)
        await ctx.send(arabic)
    elif langformat == "list":
        await ctx.send("french, latin, russian, german, arabic")
    else:
        await ctx.send("Incorrect usage.")




client.run('OTYwOTUwMjIzODQzMjM3OTM5.Ykx4og.3C2MvkbeGYyub8K_e7u6_ZdWCj4')
