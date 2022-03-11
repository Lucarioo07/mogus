import discord
from discord.ext import commands
from replit import db
import os
from utils import *
import errors


class Boiz(commands.Cog):
    def __init__(self, client):
        self.client = client
       
        
    def cog_check(self, ctx):
        if ctx.guild.id == 949280269427421224:
            return True
        else:
            raise errors.WrongServer()

    cog_help(name="Da Boiz", desc="Private commands for the 'da boiz' server", guild=949280269427421224)

    
    @commands.command(aliases=["cc"])
    @command_help(name="CustomChannel", 
                  desc="Creates a custom channel with full perms for yourself. Limited to one. If no name is specified it'll give you some boring                              name", 
                  syntax="cc [name]",
                  cog="Da Boiz",
                  aliases=["cc"])
    async def customchannel_create(self, ctx, *, name=None):
        if not name:
            name = f"{ctx.author.name}'s channel"

        if str(ctx.author.id) not in db['custom'].values():
            
            category = discord.utils.get(ctx.guild.categories, id=949679965438369862)
            channel = await category.create_text_channel(name, topic=f"This channel belongs to {ctx.author}")
            await channel.set_permissions(ctx.author, manage_channels=True, manage_permissions=True)
            
            db['custom'][str(channel.id)] = str(ctx.author.id)

            
            await channel.send(f"Welcome to `{name}`, `{ctx.author}`'s channel!")
        else:
            await ctx.reply("You already have a custom channel lmao")

    @commands.command(aliases=["cd"])
    @command_help(name="CustomChannel_Delete", 
                  desc="Deletes your custom channel", 
                  syntax="cd",
                  cog="Da Boiz",
                  aliases=["cd"])
    async def customchannel_delete(self, ctx):
        if str(ctx.author.id) in db['custom'].values():
            c = get_key(str(ctx.author.id), db['custom'])
            channel = await client.fetch_channel(c)
            del db['custom'][str(c)]
            await channel.delete()
            
            await ctx.send(f"Deleted channel that belonged to {ctx.author.mention}")
        else:
            await ctx.send("You need a channel to delete lol")

    
    @commands.command(aliases=['cban'])
    @command_help(name="CustomChannel_Ban", 
                  desc="Bans a user from your custom channel", 
                  syntax="cban <user>",
                  cog="Da Boiz",
                  aliases=["cban"])
    async def customchannel_ban(self, ctx, member: discord.Member):

        if str(ctx.author.id) not in db['custom'].values():
            await ctx.send("You need a custom channel, make one using `>cc (name)`")
        else:
            channel = await client.fetch_channel(get_key(str(ctx.author.id), db['custom']))
            await channel.set_permissions(member, read_messages=False)
            await ctx.send(f"{member.mention} has been banned from {channel.mention}")
            await member.send(f"You've been banned from {channel.mention} (`{ctx.author.id}`s channel)")


    @commands.command(aliases=['cunban'])
    @command_help(name="CustomChannel_Unban", 
                  desc="Unbans a user from your custom channel", 
                  syntax="cunban <user>",
                  cog="Da Boiz",
                  aliases=["cunban"])
    async def customchannel_unban(self, ctx, member: discord.Member):

        if str(ctx.author.id) not in db['custom'].values():
            await ctx.send("You need a custom channel, make one using `>cc (name)`")
        else:
            channel = await client.fetch_channel(get_key(str(ctx.author.id), db['custom']))
            await channel.set_permissions(member, read_messages=True)
            await ctx.send(f"{member.mention} has been unbanned from {channel.mention}")
            await member.send(f"You've been unbanned from {channel.mention} (`{ctx.author.id}`s channel)")

    
def setup(client):
    client.add_cog(Boiz(client))