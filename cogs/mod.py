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
      if staff_check(ctx.author, ctx.guild):
        return True
      else:
        raise errors.NotStaff()

    # Commands

    @commands.command(aliases=['sstaff'])
    async def setstaff(self, ctx, *staff: discord.Role):

      s = []
      for sid in staff:
        s.append(sid.id)
      db['staff'][str(ctx.guild.id)] = s
      s = ""
      for sid in staff:
        s = s + sid.name + ", "
      s = s[:-2]
      embed = discord.Embed(description=f"The role(s) `{s}` will now be able to do staff commands", color=cyan)
      embed.set_footer(text="Having the administrator permission will let you do all staff commands")
      await ctx.send(embed=embed)
      
    
    @commands.command(aliases=['astaff'])
    async def addstaff(self, ctx, role: discord.Role):

      if str(ctx.guild.id) not in db['staff'].keys():
        db['staff'][str(ctx.guild.id)] = [role.id]
      else:
        staff = db['staff'][str(ctx.guild.id)]
        staff.append(role.id)
        db['staff'][str(ctx.guild.id)] = staff

      embed = discord.Embed(description=f"The role `{role}` will now be able to do staff commands", color=cyan)
      embed.set_footer(text="Having the administrator permission will let you do all staff commands")
      await ctx.send(embed=embed)

    @commands.command(aliases=['rstaff'])
    async def removestaff(self, ctx, role: discord.Role):
      
      staff = db['staff'][str(ctx.guild.id)]
      staff.remove(role.id)
      db['staff'][str(ctx.guild.id)] = staff

      embed = discord.Embed(description=f"The role `{role}` will no longer be able to do staff commands", color=cyan)
      embed.set_footer(text="Having the administrator permission will let you do all staff commands")
      await ctx.send(embed=embed)
    
    @commands.command(aliases=['slist'])
    async def stafflist(self, ctx):
      staff = db['staff'][str(ctx.guild.id)]
      sname = ""
      for s in staff:
        sr = discord.utils.get(ctx.guild.roles, id=s)
        sname = sname + sr.name + "\n"
      embed = discord.Embed(description=f"```prolog\n{sname}```", color=cyan)
      await ctx.send(embed=embed)


    @commands.command(aliases=['prefix', 'sp'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def setprefix(self, ctx, *, prefix):

      db['prefix'][str(ctx.guild.id)] = prefix

      embed = discord.Embed(description=f"The prefix of this server has been changed to `{prefix}`", color=cyan)
      await ctx.send(embed=embed)

    @commands.command(aliases=['mr'])
    async def modifyroles(self, ctx, user: discord.Member, *roles):

      try:
        if "|" in roles:
          i = roles.index("|")

          add = roles[:i]
          for a in add:

            if a.isnumeric():
              a = discord.utils.get(ctx.guild.roles, id=int(a))
            elif a.startswith("<@&") and a.endswith(">"):
              a = discord.utils.get(ctx.guild.roles, id=int(a[4:-1]))
            else:
              a = discord.utils.get(ctx.guild.roles, name=a)
            print(type(a), a)
            await user.add_roles(a)

          remove = roles[i+1:]
          for r in remove:

            if r.isnumeric():
              r = discord.utils.get(ctx.guild.roles, id=r)
            elif r.startswith("<@&") and r.endswith(">"):
              r = discord.utils.get(ctx.guild.roles, id=int(r[4:-1]))
            else:
              r = discord.utils.get(ctx.guild.roles, name=r)

            await user.remove_roles(r)
            
        else:
          embed = discord.Embed(
            description="Please use a '|' to seperate the roles to be added and the roles to be removed",
            color=cyan)
          await ctx.reply(embed=embed)
          return

        for r in remove:
          if r not in user.roles:
            await ctx.reply(embed=discord.Embed(description=f"User doesn't have the role `{r}`", color=cyan))
            return
          else:
            await user.remove_roles(r)
        
        for a in add:
          await user.add_roles(add)

        embed = discord.Embed(description=f"The roles `{', '.join(add)}` have been added \nThe roles `{', '.join(remove)}` have been removed", color=cyan)
        await ctx.send(embed=embed)
        
      except commands.RoleNotFound as e:
        embed = discord.Embed(description=f"The role `{e.argument}` couldn't be found", color=cyan)
        embed.set_footer(text="Make sure to keep spaces between each of the role names, and the '|'")
        await ctx.reply(embed=embed)


def setup(client):
    client.add_cog(Mod(client))