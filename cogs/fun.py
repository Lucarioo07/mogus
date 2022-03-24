import discord
from discord.ext import commands
from replit import db
import os
from utils import *
import errors


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    cog_help(name="Fun", desc="Commands for fun!") 
    

    # Commands

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @command_help(name="Frame", 
                  desc="Frames a user to make it look like they said something", 
                  syntax="frame <user> <text>",
                  cog="Fun")
    async def frame(self, ctx, user: discord.Member, *, content):

        if is_owner(ctx.author.id) or (user.id not in [client.owner.id, client.user.id]):
            frame(content, user, await fetch_webhook(ctx.channel))
        else:
            frame(content, ctx.author, await fetch_webhook(ctx.channel))

    """
    @commands.command(aliases=['name'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands
    async def names(self, ctx, user: discord.Member, name):

      if names.startswith("remove"):
        if not staff_check(ctx.author, ctx.guild):
          raise errors.NotStaff(ctx.author)
    """


def setup(client):
    client.add_cog(Fun(client))
