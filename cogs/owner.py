import discord
from discord.ext import commands
# idk
from utils import *
import utils
import game_info
import os
from replit import db
from traceback import format_exception
from copy import copy
# eval
import io
import contextlib
import textwrap


class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    def cog_check(self, ctx):
        if is_owner(ctx.author):
            return True
        else:
            raise commands.NotOwner()

    # Commands

    @commands.command(aliases=["lockdown"])
    async def lock(self, ctx, l:bool = True):
        await ctx.send(f"`Lock status has been updated to {l}`")
        db['lock'] = l
    

    @commands.command(aliases=["bb"])
    async def botban(self, ctx, user: discord.Member):

        banned = db["banned"]

        if user.id not in banned:
            banned.append(user.id)
            db["banned"] = banned

            await ctx.send(embed=discord.Embed(
                description=f"haha **`{user}`**, you are ~~bangi~~ botbanned",
                color=cyan))
        else:
            await ctx.send("user already banned wheeeeeeee")

    @commands.command(aliases=["ubb", "unban"])
    async def unbotban(self, ctx, user: discord.Member):

        banned = db["banned"]

        if user.id in banned:
            banned.remove(user.id)
            db["banned"] = banned

            await ctx.send(embed=discord.Embed(
                description=f"sadly, **`{user}`** was unbanned", color=cyan))
        else:
            await ctx.send("user isnt banned :(")

    @commands.command()
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


    @commands.command(name="eval", aliases=["exec"])
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
            "utils": utils,
            "game_info": game_info,
            "db": db
        }

        stdout = io.StringIO()
        ded = True
        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}",
                    local_variables,
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

            pager = Pag(timeout=100,
                        entries=[
                            result[i:i + 2000]
                            for i in range(0, len(result), 2000)
                        ],
                        length=1,
                        prefix="```py\n",
                        suffix="```")

            await pager.start(ctx)

    @commands.command()
    async def sudo(self, ctx, user: discord.Member, *, msg):

        fake = copy(ctx.message)
        fake.author = user
        fake.content = ctx.prefix + msg
        await self.client.process_commands(fake)

    # _HELP EDIT COMMANDS_

    # Cog Help Commands

    @commands.command(aliases=['dcg', 'deletecog'])
    async def deletecoghelp(self, ctx, cogname):

        if cogname in db['help'].keys():
            await ctx.send(f"Help entry for Cog `{cogname}` has been deleted.")
            del db['help'][cogname]
        else:
            await ctx.send("cog not found")

    # Command Help Commands

    @commands.command(aliases=['dcd', 'deletecmd'])
    async def deletecmdhelp(self, ctx, cogname, cmdname):

        if cogname in db['help'].keys():
            if cmdname in db['help'][cogname]['cmds'].keys():
                await ctx.send(
                    f"Help entry for command `{cmdname}` has been deleted.")
                del db['help'][cmdname]
            else:
                await ctx.send("command not found")
        else:
            await ctx.send("cog not found")


def setup(client):
    client.add_cog(Owner(client))
