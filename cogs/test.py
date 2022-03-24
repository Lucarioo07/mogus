import discord
from discord.ext import commands
from replit import db
from random import choice
import os
from utils import *
import errors

class Test(commands.Cog):
    def __init__(self, client):
        self.client = client
    def cog_check(self, ctx):
        return is_owner(ctx.author)
            

            
def setup(client):
    client.add_cog(Test(client))
