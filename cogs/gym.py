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

    @is_staff()
    @commands.command()
    @command_help(name="Log", 
                  desc="A staff command to log the results of a match", 
                  syntax="cban <user>",
                  cog="Mystics Gym")
    async def log(self, ctx, win: discord.Member, lose: discord.Member):

        if str(win.id) not in db['points'].keys():
            db['points'][win.id] = 0
        if str(lose.id) not in db['points'].keys():
            db['points'][lose.id] = 0

        db['points'][str(win.id)] += 10
        db['points'][str(lose.id)] -= 10

        embed = discord.Embed(
            description=f"Successfully logged.\n"
            f"`{win}` won and now has `{db['points'][str(win.id)]}` points\n"
            f"`{lose}` lost and now has `{db['points'][str(lose.id)]}` points",
            color=cyan)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['view', 'point'])
    async def viewpoint(self, ctx, user: discord.Member = None):

        if user is None:
            user = ctx.author

        if str(user.id) not in db['points'].keys():
            db['points'][str(user.id)] = 0

        e = f"`{user}` has `{db['points'][str(user.id)]}` points"

        embed = discord.Embed(description=e, color=cyan)
        await ctx.reply(embed=embed)

    @is_staff()
    @commands.command()
    async def editpoint(self, ctx, user: discord.Member, point: int):

        if str(user.id) not in db['points'].keys():
            db['points'][str(user.id)] = 0

        old = db['points'][str(user.id)]
        db['points'][str(user.id)] = point

        e = f"`{user}`'s points have been changed from `{old}` to `{point}`"

        embed = discord.Embed(description=e, color=cyan)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["lb"])
    async def leaderboard(self, ctx):

        m = await ctx.reply(embed=discord.Embed(
            description="wait two seconds, fetching leaderboard...",
            color=cyan))
        s = list(db['points'].keys())
        if len(s) > 0:
            asc = sorted(s, key=lambda k: db['points'][k], reverse=True)

            lb = "```prolog\n"
            i = 1
            for uid in asc:
                lb += f"{i}. {await client.fetch_user(int(uid))} : {db['points'][uid]}\n"
                i += 1
            lb += "```"
        else:
            lb = "br no one has any points yet"

        embed = discord.Embed(description=lb, color=cyan)
        await m.edit(embed=embed)

    @is_staff()
    @commands.command()
    async def reset(self, ctx):

        await ctx.reply("`Leaderboard has been reset`")
        db['points'] = {}


def setup(client):
    client.add_cog(MysticsGym(client))
