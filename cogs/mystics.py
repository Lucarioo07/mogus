import discord
from discord.ext import commands, tasks
from replit import db
from random import choice
import os
from utils import *
import time


class Mystics(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    # Tasks
    
    @tasks.loop(seconds=604800)
    async def weekloop(self):
      db['points'] = {}

    # Commands 
"""
    @commands.is_owner()
    @commands.command()
    async def log(self, ctx, win: discord.Member, lose: discord.Member):
"""

def setup(client):
  client.add_cog(Mystics(client))