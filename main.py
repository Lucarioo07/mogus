import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle
from utils import *
from keep_alive import keep_alive
import os
from replit import db

client.remove_command("help")


@client.event
async def on_ready():

    if not is_owner(discord.AppInfo.owner):
      await client.close()

    activity = discord.Game(name=">help")
    await client.change_presence(activity=activity, status=discord.Status.dnd)

    for filename in os.listdir('./cogs'):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")

    print("Bot is ready.")


@client.event
async def on_guild_join(guild):
    if str(guild.id) not in db['prefix'].keys():
        db['prefix'][str(guild.id)] = ">"


@client.command()
@commands.is_owner()
async def load(ctx, extension):

    if extension == "all":
        for filename in os.listdir('./cogs'):
            if filename.endswith(".py"):
                try:
                    client.load_extension(f"cogs.{filename[:-3]}")
                except commands.ExtensionAlreadyLoaded:
                    client.reload_extension(f"cogs.{filename[:-3]}")

        ded = "**`All Cogs successfully loaded`**"
    else:
        if f"{extension}.py" not in os.listdir("./cogs"):
            ded = "`Not a valid cog`"
        else:
            try:
                client.load_extension(f"cogs.{extension}")
            except commands.ExtensionAlreadyLoaded:
                ded = f"**Cog `{extension}` is already loaded**"
            else:
                ded = f"**Cog `{extension}` successfully loaded`**"

    embed = discord.Embed(description=ded, color=cyan)
    await ctx.send(embed=embed)


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    if extension == "all":
        for filename in os.listdir('./cogs'):
            if filename.endswith(".py"):
                try:
                    client.unload_extension(f"cogs.{filename[:-3]}")
                except commands.ExtensionNotLoaded:
                    pass

        ded = "**`All Cogs successfully unloaded`**"
    else:
        if f"{extension}.py" not in os.listdir("./cogs"):
            ded = "`Not a valid cog`"
        else:
            try:
                client.unload_extension(f'cogs.{extension}')
            except commands.ExtensionNotLoaded:
                ded = f"**Cog `{extension}` is already unloaded**"
            else:
                ded = f"**Cog `{extension}` successfully unloaded**"

    embed = discord.Embed(description=ded, color=cyan)
    await ctx.send(embed=embed)


@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    if extension == "all":
        for filename in os.listdir('./cogs'):
            if filename.endswith(".py"):
                try:
                    client.unload_extension(f"cogs.{filename[:-3]}")
                except commands.ExtensionNotLoaded:
                    pass
                finally:
                    client.load_extension(f"cogs.{filename[:-3]}")

        ded = "**`All Cogs successfully reloaded`**"
    else:
        if f"{extension}.py" not in os.listdir("./cogs"):
            ded = "`Not a valid cog`"
        else:
            try:
                client.unload_extension(f'cogs.{extension}')
                client.load_extension(f"cogs.{extension}")
            except commands.ExtensionNotLoaded:
                ded = f"**Cog `{extension}` is currently unloaded**"
            else:
                ded = f"**Cog `{extension}` successfully reloaded**"

    embed = discord.Embed(description=ded, color=cyan)
    await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    await ctx.send(
        f'Ping of main instance is `{round(client.latency * 1000)}ms` 🏓')


keep_alive()
client.run(bot_token)
