import discord
from discord.ext import commands
from replit import db
from random import choice
import os
from utils import *
import errors


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    @commands.Cog.listener()
    async def on_message_delete(self, ctx):

        snipe_target = db["snipe_target"]
        if ctx.author.id in snipe_target:
            send_webhook(ctx.content, f"{ctx.author.name} (snipe)", ctx.author.avatar_url, await fetch_webhook(ctx.channel))
    
    @commands.Cog.listener()
    async def on_message_edit(self, ctx, after):

        snipe_target = db["snipe_target"]
        if ctx.author.id in snipe_target:
            send = f"> {after.content}\n **Before:** `{ctx.content}`"
            send_webhook(send, f"{ctx.author.name} (editsnipe)", ctx.author.avatar_url, await fetch_webhook(ctx.channel))

    # Commands

    @commands.command()
    @is_not_banned()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def frame(self, ctx, user: discord.Member, *, content):

      if is_owner(ctx.author.id) or (user.id not in safe):
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