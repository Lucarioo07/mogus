import discord
from discord.ext import commands
from replit import db
from random import choice
import os
from utils import *
import time


class Errors(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    # Events 

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
      if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="__Command is on cooldown__", description=f"This command is currently on cooldown, try again in `{error.retry_after:.2f}s`", color=cyan)
        await ctx.reply(embed=embed)


def setup(client):
    client.add_cog(Errors(client))