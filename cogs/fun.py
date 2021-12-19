import discord
from discord.ext import commands
from replit import db
from random import choice
import os
from utils import *


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
            send = f"> [{after.content}]({after.jump_url}) \n **Before:** `{ctx.content}`"
            send_webhook(send, f"{ctx.author.name} (editsnipe)", ctx.author.avatar_url, await fetch_webhook(ctx.channel))

    # Commands

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def frame(self, ctx, user: discord.Member, *, content):

        banned = db["banned"]

        if await commands.Bot.is_owner(client, ctx.author) or (
                (user.id not in safe) and (ctx.author.id not in banned)):
            if content != "":
              
              frame(content, user, await fetch_webhook(ctx.channel))
        else:
            frame(content, ctx.author, await fetch_webhook(ctx.channel))
    
    @commands.command()
    async def names(self, ctx):
      if ctx.guild.id == 764060384897925120:

        chn = await client.fetch_channel(765197786680786964)
        msg = await chn.fetch_message(896296462328135680)
        desc = f'{msg.content}\n [Original](https://discord.com/channels/{ctx.guild.id}/{chn.id}/{msg.id} "Jump to original message")'
        await ctx.send(embed=discord.Embed(description=desc, color=cyan))
      


def setup(client):
    client.add_cog(Fun(client))