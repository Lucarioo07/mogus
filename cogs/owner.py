# discord imports
import discord
from discord.ext import commands
# idk
from utils import *
import utils
import game_info
import os
from replit import db
# eval
import io
import contextlib
import textwrap
from traceback import format_exception


class Owner(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events


    # Commands

    @commands.command(aliases=["exit", "quit"])
    @commands.is_owner()
    async def kill(self, ctx):
        await ctx.send("`Exiting test instance`")
        await client.close()

    @commands.command(aliases=["bb", "ban"])
    @commands.is_owner()
    async def botban(self, ctx, user: discord.Member):

        banned = db["banned"]
        print(banned)

        if user.id not in banned:
            banned.append(user.id)
            db["banned"] = banned

            await ctx.send(embed=discord.Embed(description=f"haha **`{user}`**, you are now botbanned", color=cyan))
        else:
            await ctx.send("user already banned wheeeeeeee")

    @commands.command(aliases=["ubb", "unban"])
    @commands.is_owner()
    async def unbotban(self, ctx, user: discord.Member):

        banned = db["banned"]

        if user.id in banned:
            banned.remove(user.id)
            db["banned"] = banned

            await ctx.send(embed=discord.Embed(description=f"sadly, **`{user}`** was unbanned", color=cyan))
        else:
            await ctx.send("user isnt banned :(")

    @commands.command()
    @commands.is_owner()
    async def banlist(self, ctx):
        banned = db["banned"]

        benlist = "```prolog\n"
        i = 1
        empty = True
        for mogus in banned:
            benlist += f"{i}. {str(await client.fetch_user(mogus))}\n"
            i += 1
            empty = False

        benlist += "```"

        if empty:
            benlist = "no one benned :sob:"

        await ctx.send(embed=discord.Embed(description=benlist, color=cyan))

    @commands.is_owner()
    @commands.command()
    async def tag(self, ctx, user: discord.Member):
        snipe_target = db["snipe_target"]
        if user.id not in snipe_target:
            snipe_target.append(user.id)
            db["snipe_target"] = snipe_target
            await ctx.send(embed=discord.Embed(description=f"**`{user}`** has been tagged. Have fun 💀", color=cyan))
        else:
            await ctx.send(f"**`{user}`** has already been tagged.")

    @commands.is_owner()
    @commands.command()
    async def untag(self, ctx, user: discord.Member):
        snipe_target = db["snipe_target"]
        if user.id in snipe_target:
            snipe_target.remove(user.id)
            db["snipe_target"] = snipe_target
            await ctx.send(embed=discord.Embed(description=f"**`{user}`** has been untagged. sad.", color=cyan))
        else:
            await ctx.send(f"**`{user}`** hasn't been tagged... yet")

    @commands.command(name="eval", aliases=["exec"])
    @commands.is_owner()
    async def _eval(self, ctx, *, code):
        code = clean_code(code)

        local_variables = {
            "discord": discord,
            "commands": commands,
            "client": client,
            "os": os,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "private": utils,
            "game_info": game_info,
            "db":  db
        }

        stdout = io.StringIO()
        ded = True
        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
                )

                returned = await local_variables["func"]()
                console = stdout.getvalue()
                if returned is None and console != "":
                  result = f"{console}"
                elif console == "" and returned is None:
                  ded = False
                else:
                  result = f"{console}\n-- {returned}\n"
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))

        if ded:

            pager = Pag(
              timeout=100,
              entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
              length=1,
              prefix="```py\n",
              suffix="```"
            )

            await pager.start(ctx)


def setup(client):
    client.add_cog(Owner(client))