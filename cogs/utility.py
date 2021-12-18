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
    
    @commands.command(aliases=["halp"])
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


def setup(client):
    client.add_cog(Utility(client))