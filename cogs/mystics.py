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
    @is_staff()
    @commands.command()
    async def log(self, ctx, win: discord.Member, lose: discord.Member):
      
      if str(win.id) not in db['points'].keys():
        db['points'][win.id] = 0
      if str(lose.id) not in db['points'].keys():
        db['points'][lose.id] = 0

      db['points'][str(win.id)] += 10
      db['points'][str(lose.id)] -= 10

      embed = discord.Embed(description=
        f"Successfully logged.\n"
        f"`{win}` won and now has `{db['points'][str(win.id)]}` points\n"
        f"`{lose}` lost and now has `{db['points'][str(lose.id)]}` points",
        color=cyan
      )
      await ctx.reply(embed=embed)

    @in_guild(927259600628088842)
    @commands.command(aliases= ['view', 'point'])
    async def viewpoint(self, ctx, user: discord.Member = None):

      if user is None:
        user = ctx.author

      if str(user.id) not in db['points'].keys():
        db['points'][str(user.id)] = 0
    
      e = f"`{user}` has `{db['points'][str(user.id)]}` points"
      
      embed = discord.Embed(description=e, color=cyan)
      await ctx.reply(embed=embed)
    
    @in_guild(927259600628088842)
    @is_staff()
    @commands.command()
    async def editpoint(self, ctx, user: discord.Member, point:int):

      if str(user.id) not in db['points'].keys():
        db['points'][str(user.id)] = 0
    
      old = db['points'][str(user.id)]
      db['points'][str(user.id)] = point

      e = f"`{user}`'s points have been changed from `{old}` to `{point}`"
      
      embed = discord.Embed(description=e, color=cyan)
      await ctx.reply(embed=embed)


    @in_guild(927259600628088842)
    @commands.command(aliases=["lb"])
    async def leaderboard(self, ctx):
      if len(db['points'].keys()) > 0:
        asc = [] 
        for i in db['points'].keys():
          asc.append(int(db['points'][i]))
        asc.sort(reverse=True)

        lb = "```prolog\n"
        i = 1
        for v in asc:
          uid = get_key(v, db['points'])
          lb += f"{i}. {await client.fetch_user(uid)} : {v}\n"
          i += 1
        lb += "```"
      else:
        lb = "br no one has any points yet"
        
      embed = discord.Embed(description=lb, color=cyan)
      await ctx.reply(embed=embed)

    @in_guild(927259600628088842)
    @is_staff()
    @commands.command()
    async def reset(self, ctx):

      await ctx.reply("`Leaderboard has been reset`")
      db['points'] = {}
    

def setup(client):
  client.add_cog(Mystics(client))