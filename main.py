import discord
from discord.ext import commands
from utils import client, bot_token, disabled_check, locked_check, ban_check, log, cyan
from keep_alive import keep_alive
import os
from replit import db


client.remove_command("help")

    
@client.check
async def global_checks(ctx):
    
    if disabled_check(ctx.guild, ctx.command.name):
        if locked_check(ctx.author):
            if ban_check(ctx.author):
                return True


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
            ded = "**`Not a valid cog`**"
        else:
            try:
                client.load_extension(f"cogs.{extension}")
            except commands.ExtensionAlreadyLoaded:
                ded = f"Cog **`{extension}`** is already loaded"
            else:
                ded = f"Cog **`{extension}`** successfully loaded"

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
            ded = "**`Not a valid cog`**"
        else:
            try:
                client.unload_extension(f'cogs.{extension}')
            except commands.ExtensionNotLoaded:
                ded = f"Cog **`{extension}`** is already unloaded"
            else:
                ded = f"Cog **`{extension}`** successfully unloaded"

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
            ded = "**`Not a valid cog`**"
        else:
            try:
                client.unload_extension(f'cogs.{extension}')
                client.load_extension(f"cogs.{extension}")
            except commands.ExtensionNotLoaded:
                ded = f"Cog **`{extension}`** is currently unloaded"
            else:
                ded = f"Cog **`{extension}`** successfully reloaded"

    embed = discord.Embed(description=ded, color=cyan)
    await ctx.send(embed=embed)


keep_alive()
client.run(bot_token)
