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

    # Commands 

    @in_guild(927259600628088842)
    @commands.is_owner()
    @commands.command()
    async def log(self, ctx, win: discord.Member, lose: discord.Member):
    
      if str(win.id) not in db['points'].tags():
        db['points'][win.id] = 0
      if str(lose.id) not in db['points'].tags():
        db['points'][lose.id] = 0

      db['points'][str(win.id)] += 10
      db['points'][str(lose.id)] -= 10

      embed = discord.Embed(description=
        f"Successfully logged.\n"
        f"`{win}` won and now has `{db['points'][str(win.id)]}` points"
        f"`{lose}` lost and now has `{db['points'][str(lost.id)]}` points",
        color=cyan
      )
      await ctx.send(embed=embed)

    @in_guild(927259600628088842)
    @commands.is_owner()
    @commands.command(aliases= ['view', 'point'])
    async def viewpoint(self, ctx, user: discord.Member = None):

      if user is not None:
        user = ctx.author

      if str(user.id) not in db['points'].tags():
        e = f"`{user}` has no points f"
      else:
        e = f"`{user}` has `{db['points'][str(user.id)]}` points"
      
      embed = discord.Embed(description=e, color=cyan)
      await ctx.send(embed=embed)
    
    @in_guild(927259600628088842)
    @commands.is_owner()
    @commands.command()
    async def editpoint(self, ctx, user: discord.Member, point):

      if str(user.id) not in db['points'].tags():
        e = f"`{user}` has no points f"
      else:
        old = db['points'][str(user.id)]
        db['points'][str(user.id)] = point

        e = f"`{user}`'s points have been changed from `{old}` to `{new}`"
      
      embed = discord.Embed(description=e, color=cyan)
      await ctx.send(embed)


    @in_guild(927259600628088842)
    @commands.is_owner()
    @commands.command(aliases="lb")
    async def leaderboard(self, ctx):
      
      asc = db['points'].values().sort(reverse=True)

      lb = "```prolog\n"
      i = 0
      empty = True
      for v in asc:
        uid = get_key(v, db['points'])
        lb += f"{i}. {client.fetch_user(uid)}\n"
        i += 1
        empty = False

      lb += "```"
      if empty:
        lb = "br no one has any points yet"
      embed = discord.Embed(description=lb)

    @in_guild(927259600628088842)
    @commands.is_owner()
    @commands.command()
    async def reset(self, ctx):

      await ctx.send(embed=discord.Embed(description='Are you sure you want to reset the leaderboard? Respond with `yes` if so'))
      
      def check(m):
        return m.content == 'hello' and m.channel == channel and m.author == ctx.author

      try:
        check = await client.wait_for('message', check=check, timeout=15.0)
      except:
        await ctx.reply("ill take that as a no then")
      else: 
        await ctx.reply("`Leaderboard has been reset`")
        db['points'] = {}
    

def setup(client):
  client.add_cog(Mystics(client))