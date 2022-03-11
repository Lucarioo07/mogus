import discord
from discord.ext import commands
from replit import db
from random import choice
import os
from utils import *
import time
import errors


class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    cog_help(name="Utility", desc="Commands that try to be useful but fail miserably")    
    
    # Events

    @commands.Cog.listener()
    async def on_message(self, ctx):
        
        if not ctx.author.bot:
            afk = db['afk']
            for user in ctx.mentions:
                if not (str(ctx.guild.id) in db['disabled'] and "afk" in db['disabled'][str(ctx.guild.id)]):
                    if str(ctx.guild.id) in afk['server'].keys() and str(
                            user.id) in afk['server'][str(ctx.guild.id)]:
                        embed = discord.Embed(
                            description=
                            f"***{user}:** `{afk['server'][str(ctx.guild.id)][str(user.id)]}`*",
                            color=cyan)
                        embed.set_footer(
                            text=
                            f"use {db['prefix'][str(ctx.guild.id)]}afk to get your own ping message"
                        )
                        await ctx.reply(embed=embed, delete_after=15)

                    elif str(user.id) in afk['global'].keys():
                        embed = discord.Embed(
                            description=
                            f"***{user}:** `{afk['global'][str(user.id)]}`*",
                            color=cyan)
                        embed.set_footer(
                            text=
                            f"use {db['prefix'][str(ctx.guild.id)]}afk to get your own ping message"
                        )
                        await ctx.reply(embed=embed, delete_after=15)

                if user == client.user:
                    embed = discord.Embed(
                        description=
                        f"The prefix of this server is `{db['prefix'][str(ctx.guild.id)]}`",
                        color=cyan)
                    await ctx.reply(embed=embed, delete_after=15)


    # Commands

    @commands.command(aliases=["halp"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @command_help(name="Help", 
              desc="Displays this message 🤡. You can ask for help for a whole field, or just a single command. Leaving it blank will display all the                                                fields available in the server", 
              syntax="help [command or field]",
              cog="Utility",
              aliases=["halp"])
    async def help(self, ctx, *, field=None):

        cmds = db['help']
        if field: field = field.title()
        if not field:
            embed = discord.Embed(
                title="__Help List__",
                description=
                "In the arguments of a command, a `<>` around one means a compulsory argument meanwhile a `[]` around one means an optional argument",
                color=cyan)
            for cogname in cmds.keys():
                if cmds[cogname]['guild']:
                    if ctx.guild.id == cmds[cogname]['guild']:
                        embed.add_field(name=f"{cogname} Field",
                                        value=f"> {cmds[cogname]['desc']}",
                                        inline=True)
                else:
                    embed.add_field(name=f"{cogname} Field",
                                    value=f"> {cmds[cogname]['desc']}",
                                    inline=True)
            embed.set_footer(text="Specify a field to get info on commands")

        else:
            if field in cmds.keys():
                if not cmds[field]['guild'] or cmds[field]['guild'] == ctx.guild.id:
                    embed = discord.Embed(
                        title=f"__{field} Field__", color=cyan)

                    for c in cmds[field]['commands'].keys():
                        cmd = cmds[field]['commands'][c]
                        embed.add_field(
                            name=f"{c} Command",
                            value=f"> {cmd['desc']} \n"
                                  f"__Syntax:__ `{gprefix(ctx.guild.id)}{cmd['syntax']}`")
                    embed.set_footer(text=f"Use help with a command as an argument to get more detailed information on it")
            else:
                for cog in cmds.keys():
                    if not cmds[cog]['guild'] or cmds[cog]['guild'] == ctx.guild.id:
                        if (field in cmds[cog]['commands'].keys()):

                            cmd = cmds[cog]['commands'][field]
                            a = lambda: f"__Aliases:__ `{', '.join(cmd['aliases'])}` \n" if cmd['aliases'] else "" 
                            
                            embed = discord.Embed(
                                title=f"__{field} Command__",
                                description=
                                f"> {cmd['desc']} \n"
                                f"{a()}"
                                f"__Syntax:__ `{gprefix(ctx.guild.id)}{cmd['syntax']}`",
                                color=cyan)
                            embed.set_footer(
                                text="lol imagine asking for help")

        try:
            await ctx.reply(embed=embed)
        except:
            await ctx.reply(embed=discord.Embed(
                description="Sorry but this field or command couldn't be found",
                color=cyan))

    

    @commands.command(aliases=['pingmsg', 'pingmessage'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @command_help(name="AFK", 
              desc="Displays a message to be sent when you get pinged. If you specify 'global' before the message, then this will be shown in all                         servers with me in it. Not specifying it will make it only be seen in this server", 
              syntax="afk ['global'] <message>",
              cog="Utility",
              aliases=["pingmsg" "pingmessage"])
    async def afk(self, ctx, *, message):

        desc = ""
        if message.count("\n") > 2:
            message = message.replace("\r", " ").replace("\n", " ")

        if message.startswith("global"):
            m = message[7:]
            if m == "remove":
                try:
                    del db['afk']['global'][str(ctx.author.id)]
                    desc = "Your global ping message has been removed"
                except:
                    desc = "You don't have a global ping message to remove ffs"
            else:
                db['afk']['global'][str(ctx.author.id)] = m
                desc = f"Your global ping message has been set to `{m}`"
        else:
            m = message
            if m == "remove":
                try:
                    del db['afk']['server'][str(ctx.guild.id)][str(
                        ctx.author.id)]
                    desc = "Your server ping message has been removed"
                except:
                    desc = "You don't have a server ping message to remove ffs"
            else:
                try:
                    db['afk']['server'][str(ctx.guild.id)][str(
                        ctx.author.id)] = m
                except:
                    db['afk']['server'][str(ctx.guild.id)] = {
                        str(ctx.author.id): m
                    }
                desc = f"Your server ping message has been set to `{m}`"

        embed = discord.Embed(description=desc, color=cyan)
        await ctx.send(embed=embed)
    
    @commands.command()
    @command_help(name="ping", 
                  desc="Show bot latency (or ping)", 
                  syntax="ping",
                  cog="Utility")
    async def ping(ctx):
        await ctx.send(
            f'Ping of main instance is `{round(client.latency * 1000)}ms` 🏓')


def setup(client):
    client.add_cog(Utility(client))
