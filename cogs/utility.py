import discord
from discord.ext import commands
from replit import db
from random import choice
import os
from utils import *
import time


class Utility(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    # Events 

    @commands.Cog.listener()
    async def on_message(self, ctx):
      afk = db['afk']
      i = True
      try:
        for user in afk['server'][str(ctx.guild.id)].keys():
          if f"<@!{user}>" in ctx.content:
            embed = discord.Embed(
              description=f"***{await client.fetch_user(user)}:** `{afk['server'][str(ctx.guild.id)][user]}`*", color=cyan
            )
            await ctx.reply(embed=embed)
            i = False
      except:
        pass
      if i:
        for user in afk['global'].keys():
          if f"<@!{user}>" in ctx.content:
            embed = discord.Embed(
              description=f"***{await client.fetch_user(user)}:** `{afk['global'][user]}`*", color=cyan
            )
            await ctx.reply(embed=embed)
      

    # Commands

    @commands.command(aliases=["halp"])
    @commands.command(1, 5, commands.BucketType.user)
    async def help(self, ctx, field=None):

      cmds = db['help']
      if not field:
        
        embed = discord.Embed(title= "__Help List__", description="In the arguments of a command, a `<>` around one means a compulsory argument meanwhile a `[]` around one means an optional argument", color=cyan)
        for cogname in cmds.keys():
          if cogname == "Mod":
            if ctx.guild.id == 764060384897925120:
              embed.add_field(name=f"{cogname} Field", value=f"> {cmds[cogname]['desc']}")
          else:
            embed.add_field(name=f"{cogname} Field", value=f"> {cmds[cogname]['desc']}", inline=True)
        embed.set_footer(text="Specify a field to get command info")

      else:
        if field.capitalize() in cmds.keys():

          embed = discord.Embed(title=f"__{field.capitalize()} Field__", color=cyan)
          embed.set_footer(text="Specify a command to get info on only that command")

          for cmd in cmds[field.capitalize()]['cmds'].keys():
            embed.add_field(name=f"{cmd} Command", value=f"> {cmds[field.capitalize()]['cmds'][cmd]}")
        else:
          for cog in cmds.keys():
            if field.capitalize() in cmds[cog]['cmds'].keys():
              embed = discord.Embed(title=f"__{field.capitalize()} Command__", description=f"> {cmds[cog]['cmds'][field.capitalize()]}", color=cyan)
              embed.set_footer(text="lol imagine asking for help")
        
      try:
        await ctx.reply(embed=embed)
      except:
        await ctx.reply(embed=discord.Embed(description= "Sorry but this field or command couldn't be found", color=cyan))
    
    @commands.command(aliases=['pingmsg'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def afk(self, ctx, *, message):

      desc = ""

      if message.startswith("global"):
        m = message.replace("global ", "")
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
            del db['afk']['server'][str(ctx.guild.id)][str(ctx.author.id)]
            desc = "Your server ping message has been removed"
          except:
            desc = "You don't have a server ping message to remove ffs"
        else:
          try:
            db['afk']['server'][str(ctx.guild.id)][str(ctx.author.id)] = m
          except:
            db['afk']['server'][str(ctx.guild.id)] = {ctx.author.id: m}
          desc = f"Your server ping message has been set to `{m}`"
      
      embed = discord.Embed(description=desc, color=cyan)
      await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Utility(client))