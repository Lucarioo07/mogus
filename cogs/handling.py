import discord
from discord.ext import commands
from replit import db
from random import choice
import os
from utils import *
import time
from traceback import format_exception
import errors


class Handling(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Events

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        
        logchannel = await client.fetch_channel(log)
        result = "".join(format_exception(error, error, error.__traceback__))
        embed = discord.Embed(description=
                                f'__**Information**__\n'
                                f'> **Guild:** `{ctx.guild}` `{ctx.guild.id}`\n'
                                f'> **User:** `{ctx.author}` `{ctx.author.id}`\n'
                                f'> **Message:** `{ctx.message.content}`\n'
                                f"```py\n{result}```",
                                timestamp=ctx.message.created_at,
                                color=cyan)
        check = lambda x: x.mention if is_owner(x) else ""
        await logchannel.send(check(ctx.author), embed=embed)

        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="Command is on cooldown",
                description=
                f"This command is currently on cooldown, try again in `{error.retry_after:.2f}s`",
                color=cyan)
            await ctx.send(embed=embed, delete_after=30)

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Missing Argument",
                description=
                f"You missed the `{error.param}` argument, check `{db['prefix'][str(ctx.guild.id)]}help` for information about any command",
                color=cyan)
            await ctx.send(embed=embed, delete_after=30)

        elif isinstance(error, commands.TooManyArguments):
            embed = discord.Embed(
                title="Too Many Arguments",
                description=
                f"You entered too many arguments, check `{db['prefix'][str(ctx.guild.id)]}help` for information about any command",
                color=cyan)
            await ctx.send(embed=embed, delete_after=30)

        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title="Wrong Argument(s) Given",
                description=
                f"Something went wrong with the argument(s) you gave, check `{db['prefix'][str(ctx.guild.id)]}help` for information about any command",
                color=cyan)
            await ctx.send(embed=embed, delete_after=30)

        elif isinstance(error, commands.CheckFailure):

            if isinstance(error, commands.NotOwner):
                embed = discord.Embed(
                    title="Owner Command",
                    description="imagine not being the owner lol hah",
                    color=cyan)
                await ctx.send(embed=embed, delete_after=30)

            elif isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    title="Missing Permissions",
                    description=
                    f"Uhhhh ahaha you actually need the `{error.missing_perms}` to do this",
                    color=cyan)
                await ctx.send(embed=embed, delete_after=30)

            elif isinstance(error, errors.WrongServer):
                embed = discord.Embed(
                    title="Not available",
                    description=f"This command cannot be used in this server",
                    color=cyan)
                embed.set_footer(
                    text=
                    "If you didn't mean to use a command, just ignore this ????")
                await ctx.send(embed=embed, delete_after=7.5)

            elif isinstance(error, errors.NotStaff):
                embed = discord.Embed(
                    title="Missing Permissions",
                    description=
                    f"lmao loser you need a staff role to use this command",
                    color=cyan)
                await ctx.send(embed=embed, delete_after=30)

            elif isinstance(error, errors.UserBanned):
                embed = discord.Embed(
                    title="That moment when banned",
                    description=
                    f"You've been botbanned, and cannot use this command. Appeal to the bot owner if you want to be bot banned (but dont overdo it or you'll get blocked too)",
                    color=cyan)
                embed.set_footer(text="lollers")
                await ctx.send(embed=embed, delete_after=15)

            elif isinstance(error, errors.CommandDisabled):
                embed = discord.Embed(
                    title="Command Disabled",
                    description=
                    "This command is disabled in this server, ask a staff member to enable it again",
                    color=cyan
                )
                embed.set_footer(text="imagine disabling it in the first place")
                await ctx.send(embed=embed, delete_after=15)
            
            elif isinstance(error, errors.BotLocked):
                embed = discord.Embed(
                    title="Bot is Locked",
                    description=
                    "The bot is currently locked for whatsoever reason, please bear with it until resolved ||zank you||",
                    color=cyan
                )
                embed.set_footer(text="locking bot is kinda cring")
                await ctx.send(embed=embed, delete_after=15)

            else:
                embed = discord.Embed(
                    title="You can't use this command",
                    description=
                    "something went wrong when you tried to use this command",
                    color=cyan)
                await ctx.send(embed=embed, delete_after=30)

        elif isinstance(error, discord.Forbidden):
            embed = discord.Embed(
                title="Bot Missing Permissions",
                description=
                f"hmm i'm not able to do this, ask a staff member to try and fix this",
                color=cyan)
            await ctx.send(embed=embed, delete_after=30)

        elif isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                description=
                f"This command does not exist, check `{db['prefix'][str(ctx.guild.id)]}help`",
                color=cyan)
            embed.set_footer(
                text="If you didn't mean to use a command, just ignore this ????")
            await ctx.send(embed=embed, delete_after=7.5)

        else:
            raise error


def setup(client):
    client.add_cog(Handling(client))
