import discord
from discord.ext import commands, tasks
from replit import db
from random import choice
import os
from utils import *
import time
import errors


class MysticsGym(commands.Cog):
    def __init__(self, client):
        self.client = client
        

    def cog_check(self, ctx):
        if ctx.guild.id == 927259600628088842:
            return True
        else:
            raise errors.WrongServer
            
    cog_help(name="Mystics Gym", desc="Private commands for the Mystics Gym server", guild=927259600628088842)
    
    # Commands

    


def setup(client):
    client.add_cog(MysticsGym(client))
