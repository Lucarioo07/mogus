import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle
from utils import *
from keep_alive import keep_alive
import os

client.remove_command("help")


@client.event
async def on_ready():
    activity=discord.Game(name=">help")
    await client.change_presence(activity=activity, status=discord.Status.dnd)

    for filename in os.listdir('./cogs'):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")

    print("Bot is ready.")


@client.command()
@commands.is_owner()
async def load(ctx, extension):
    if extension == "all":
        for filename in os.listdir('./cogs'):
            if filename.endswith(".py"):
                client.load_extension(f"cogs.{filename[:-3]}")

        ded = "**`All Cogs successfully loaded`**"
    else:
        if f"{extension}.py" not in os.listdir("./cogs"):
            ded = "`Not a valid cog`"
        else:
            client.load_extension(f'cogs.{extension}')
            ded = f"**`Cog {extension} successfully loaded`**"

    embed = discord.Embed(
        description=ded,
        color=cyan
    )
    await ctx.send(embed=embed)


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    if extension == "all":
        for filename in os.listdir('./cogs'):
            if filename.endswith(".py"):
                client.unload_extension(f"cogs.{filename[:-3]}")

        ded = "**`All Cogs successfully unloaded`**"
    else:
        if f"{extension}.py" not in os.listdir("./cogs"):
            ded = "`Not a valid cog`"
        else:
            client.unload_extension(f'cogs.{extension}')
            ded = f"**`Cog {extension} successfully unloaded`**"

    embed = discord.Embed(
        description=ded,
        color=cyan
    )
    await ctx.send(embed=embed)


@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    if extension == "all":
        for filename in os.listdir('./cogs'):
            if filename.endswith(".py"):
                client.unload_extension(f"cogs.{filename[:-3]}")
                client.load_extension(f"cogs.{filename[:-3]}")

        ded = "**`All Cogs successfully reloaded`**"
    else:
        if f"{extension}.py" not in os.listdir("./cogs"):
            ded = "`Not a valid cog`"
        else:
            client.unload_extension(f'cogs.{extension}')
            client.load_extension(f'cogs.{extension}')
            ded = f"**`Cog {extension} successfully reloaded`**"

    embed = discord.Embed(
        description=ded,
        color=cyan
    )
    await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    await ctx.send(f'Ping of main instance is `{round(client.latency * 1000)}ms` 🏓')


keep_alive()
client.run(bot_token)