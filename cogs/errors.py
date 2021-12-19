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

      if isinstance(error, commands.CommandError):

        if isinstance(error, commands.CommandOnCooldown):
          embed = discord.Embed(
            title="Command is on cooldown", 
            description=f"This command is currently on cooldown, try again in `{error.retry_after:.2f}s`", 
            color=cyan
          )
          await ctx.send(embed=embed, delete_after=10)
        
        elif isinstance(error, commands.MissingRequiredArgument):
          embed = discord.Embed(
            title="Missing Argument", 
            description=f"You missed the `{error.param}` argument, check the help command for information about any command", 
            color=cyan
          )
          await ctx.send(embed=embed, delete_after=10)
        
        elif isinstance(error, commands.MissingRequiredArgument):
          embed = discord.Embed(
            title="Too Many Arguments", 
            description=f"You entered too many arguments, check the help command for information about any command", 
            color=cyan
          )
          await ctx.send(embed=embed, delete_after=10)

        elif isinstance(error, commands.BadArgument):
          embed = discord.Embed(
            title="Wrong Argument Given", 
            description="Something went wrong with the argument(s) you gave, check the help command for information about any command", 
            color=cyan
          )
          await ctx.send(embed=embed, delete_after=10)


        elif isinstance(error, commands.CheckFailure):

          if isinstance(error, commands.NotOwner):
            embed = discord.Embed(
              title="Owner Command", 
              description="imagine not being the owner lol hah", 
              color=cyan
            )
            await ctx.send(embed=embed, delete_after=10)
          
          elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
              title="Missing Permissions", 
              description="Uhhhh ahaha you actually can't do that", 
              color=cyan
            )
            await ctx.send(embed=embed, delete_after=10)
          
          elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
              title="Bot Missing Permissions", 
              description="hmm i'm not able to do this, ask a staff member to give me permissions", 
              color=cyan
            )
            await ctx.send(embed=embed, delete_after=10)
          
          else:
            embed = discord.Embed(
              title="You can't use this command", 
              description="this command for non-normies only, sorry (maybe)", 
              color=cyan
            )
            await ctx.send(embed=embed, delete_after=10)
        
        if isinstance(error, commands.ExtensionError):
          
          if isinstance(error, commands.ExtensionAlreadyLoaded):
            embed = discord.Embed(
              description=f"This extension is already loaded", 
              color=cyan
            )
            await ctx.send(embed=embed, delete_after=10)

          elif isinstance(error, commands.ExtensionNotLoaded):
            embed = discord.Embed(
              description=f"This extension is not loaded", 
              color=cyan
            )
            await ctx.send(embed=embed, delete_after=10)


def setup(client):
    client.add_cog(Errors(client))