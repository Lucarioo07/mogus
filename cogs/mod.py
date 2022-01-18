import discord
from discord.ext import commands
from replit import db
from random import choice
import os
from utils import *


class Mod(commands.Cog):

    def __init__(self, client):
        self.client = client

    def cog_check(self, ctx):
      perm = ctx.author.permissions_in(ctx.channel)
      return perm.administator or staff_check(ctx.author, ctx.guild)

    # Commands

    @commands.command(aliases=['sstaff'])
    async def setstaff(self, ctx, *staff: discord.Role):

      s = []
      for sid in staff:
        s.append(sid)
      db['staff'][str(ctx.guild.id)] = s

      embed = discord.Embed(description=f"The roles `{staff.join(', ')}` will now be able to do staff commands")
      await ctx.send(embed=embed)
      
    
    @commands.command(aliases=['astaff'])
    async def addstaff(self, ctx, role: discord.Role):

      if str(ctx.guild.id) not in db['staff'].keys():
        db['staff'][str(ctx.guild.id)] = [role.id]
      else:
        staff = db['staff'][str(ctx.guild.id)]
        staff.append(role.id)
        db['staff'][str(ctx.guild.id)] = staff

      embed = discord.Embed(description=f"The role `{staff}` will now be able to do staff commands")
      await ctx.send(embed=embed)

    @commands.command(aliases=['rstaff'])
    async def removestaff(self, ctx, role: discord.Role):
      
      staff = db['staff'][str(ctx.guild.id)]
      staff.remove(role.id)
      db['staff'][str(ctx.guild.id)] = staff

      embed = discord.Embed(description=f"The role `{staff}` will no longer be able to do staff commands")
      await ctx.send(embed=embed)

    @commands.command(aliases=['prefix', 'sp'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def setprefix(self, ctx, *, prefix):

      db['prefix'][str(ctx.guild.id)] = prefix

      embed = discord.Embed(description=f"The prefix of this server has been changed to `{prefix}`", color=cyan)
      await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Mod(client))