import discord
from discord.ext import commands
from replit import db
from random import choice
import os
from utils import *
import time


class Errors(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    # Events 

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
      
      if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
          title="Command is on cooldown", 
          description=f"This command is currently on cooldown, try again in `{error.retry_after:.2f}s`", 
          color=cyan
        )
        await ctx.send(embed=embed, delete_after=30)
      
      elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
          title="Missing Argument", 
          description=f"You missed the `{error.param}` argument, check `{db['prefix'][str(ctx.guild.id)]}help` for information about any command", 
          color=cyan
        )
        await ctx.send(embed=embed, delete_after=30)
      
      elif isinstance(error, commands.TooManyArguments):
        embed = discord.Embed(
          title="Too Many Arguments", 
          description=f"You entered too many arguments, check `{db['prefix'][str(ctx.guild.id)]}help` for information about any command", 
          color=cyan
        )
        await ctx.send(embed=embed, delete_after=30)

      elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(
          title="Wrong Argument(s) Given", 
          description=f"Something went wrong with the argument(s) you gave, check `{db['prefix'][str(ctx.guild.id)]}help` for information about any command", 
          color=cyan
        )
        await ctx.send(embed=embed, delete_after=30)


      elif isinstance(error, commands.CheckFailure):

        if isinstance(error, commands.NotOwner):
          embed = discord.Embed(
            title="Owner Command", 
            description="imagine not being the owner lol hah", 
            color=cyan
          )
          await ctx.send(embed=embed, delete_after=30)
        
        elif isinstance(error, commands.MissingPermissions):
          embed = discord.Embed(
            title="Missing Permissions", 
            description=f"Uhhhh ahaha you actually need the `{error.missing_perms}` to do this", 
            color=cyan
          )
          await ctx.send(embed=embed, delete_after=30)
        
        elif isinstance(error, commands.BotMissingPermissions):
          embed = discord.Embed(
            title="Bot Missing Permissions", 
            description=f"hmm i'm not able to do this, ask a staff member to give me the `{error.missing_perms}` permission", 
            color=cyan
          )
          await ctx.send(embed=embed, delete_after=30)
        
        else:
          embed = discord.Embed(
            title="You can't use this command", 
            description="this command for non-normies only, sorry (maybe)", 
            color=cyan
          )
          await ctx.send(embed=embed, delete_after=30)
      
      elif isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            description=f"This command does not exist, check `{db['prefix'][str(ctx.guild.id)]}help`", 
            color=cyan
          )
        embed.set_footer(text="If you didn't mean to use a command, just ignore this 💀")
        await ctx.send(embed=embed, delete_after=7.5 )

      else:
        raise error


def setup(client):
    client.add_cog(Errors(client))