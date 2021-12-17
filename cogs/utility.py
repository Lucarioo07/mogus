import discord
from discord.ext import commands
from replit import db
from random import choice
import os
from utils import *


class Utility(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=["halp"])
    async def help(self, ctx, field=None):

      cmds = db['help']

      if not field:
        
        embed = discord.Embed(title= "__Help List__", color=cyan)
        for cmdname in cmds.keys():
          embed.add_field(name=cmdname, value=f"> {cmds[cmdname]}")

      else:
        for cmdname in cmds.keys():
          if field.capitalize() in cmdname:
            break
        try:
          embed = discord.Embed(title=f"{cmdname} Command", description=f"> {cmds[cmdname]}", color=cyan)
        except:
          embed = discord.Embed(description="sorry but this command couldn't be found", color=cyan)
          
      embed.set_footer(text="lol imagine asking for help")
      await ctx.reply(embed=embed)
 
def setup(client):
    client.add_cog(Utility(client))