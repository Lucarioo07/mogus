import discord
from discord.ext import commands
from replit import db
from random import choice
import os
from utils import *
import time


class Mystics(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    # Events 

    # Commands 

def setup(client):
  client.add_cog(Mystics(client))