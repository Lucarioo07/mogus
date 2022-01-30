import discord
from discord.ext import commands, tasks
from replit import db
from random import choice
import os
from utils import *


class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.punishmentcheck.start()

    def cog_check(self, ctx):
        if staff_check(ctx.author, ctx.guild):
            return True
        else:
            raise errors.NotStaff()

    def cog_unload(self):
        self.punishmentcheck.cancel()

    # Tasks

    @tasks.loop(seconds=15.0)
    async def punishmentcheck(self):
        now = datetime.datetime.now(dxb_tz)

        for g in db['muterole'].keys():
            guild = await client.fetch_guild(g)
            muterole = discord.utils.get(guild.roles, id=db['muterole'][g])

            for timestr in db['punishments']['mute'].values():
                raw_wtime = datetime.datetime.strptime(timestr,
                                                       "%d %B %Y, %H:%M")
                wtime = raw_wtime.replace(tzinfo=dxb_tz)
                delta = wtime - now
                if delta.total_seconds() < 0:
                    userid = get_key(timestr, db['punishments']['mute'])
                    member = await guild.fetch_member(userid)
                    await member.remove_roles(muterole)
                    del db['punishments']['mute'][userid]

    # Commands

    @commands.command(aliases=['shut'])
    async def mute(self, ctx, member: discord.Member, timestr='30m'):

        try:
            duration = timestr[:-1]
            timetype = timestr[-1]

            if timetype == "m":
                delta = datetime.timedelta(minutes=int(duration))
            elif timetype == "h":
                delta = datetime.timedelta(hours=int(duration))
            elif timetype == "d":
                delta = datetime.timedelta(days=int(duration))
            else:
                await ctx.send("Invalid time input")
                return
        except Exception as e:
            print(e)
            await ctx.send("Invalid time input")
            return

        try:
            muterole = discord.utils.get(ctx.guild.roles,
                                         id=db['muterole'][str(ctx.guild.id)])
        except:
            embed = discord.Embed(
                description=
                f"This server doesn't have a muterole, make one using `{db['prefix'][str(ctx.guild.id)]}muterole`",
                color=cyan)
            await ctx.reply(embed=embed)
            return

        if muterole not in member.roles:
            await member.add_roles(muterole)
            mtime = datetime.datetime.now(dxb_tz) + delta
            db['punishments']['mute'][str(
                member.id)] = mtime.strftime("%d %B %Y, %H:%M")

            embed = discord.Embed(
                description=
                f"***{str(member)}** was muted by **{str(ctx.author)}** for* **`{delta}`**",
                color=cyan)
            await member.send(embed=embed)
        else:
            embed = discord.Embed(
                description=f"***{str(member)}** is already muted lmao",
                color=cyan)
        await ctx.send(embed=embed)

    @commands.command(aliases=['unshut'])
    async def unmute(self, ctx, member: discord.Member):

        try:
            muterole = discord.utils.get(ctx.guild.roles,
                                         id=db['muterole'][str(ctx.guild.id)])
        except:
            embed = discord.Embed(
                description=
                f"This server doesn't have a muterole, make one using `{db['prefix'][str(ctx.guild.id)]}muterole`",
                color=cyan)
            await ctx.reply(embed=embed)
            return

        if muterole in member.roles:
            await member.remove_roles(muterole)
            del db['punishments']['mute'][str(member.id)]
            embed = discord.Embed(
                description=
                f"***{str(member)}** was unmuted by **{str(ctx.author)}***",
                color=cyan)
        else:
            embed = discord.Embed(
                description=f"***{str(member)}** is not muted*", color=cyan)
        await ctx.send(embed=embed)

    @commands.command()
    async def muterole(self, ctx, muterole: discord.Role):

        db['muterole'][ctx.guild.id] = muterole.id

        embed = discord.Embed(
            description=f"You've set the role `{muterole}` to be the muterole",
            color=cyan)
        await ctx.send(embed=embed)

    @commands.command(aliases=['prefix', 'sp'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def setprefix(self, ctx, *, prefix):

        db['prefix'][str(ctx.guild.id)] = prefix

        embed = discord.Embed(
            description=
            f"The prefix of this server has been changed to `{prefix}`",
            color=cyan)
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

                remove = roles[i + 1:]
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
                    description=
                    "Please use a '|' to seperate the roles to be added and the roles to be removed",
                    color=cyan)
                await ctx.reply(embed=embed)
                return

            for r in remove:
                if r not in user.roles:
                    await ctx.reply(embed=discord.Embed(
                        description=f"User doesn't have the role `{r}`",
                        color=cyan))
                    return
                else:
                    await user.remove_roles(r)

            for a in add:
                await user.add_roles(add)

            embed = discord.Embed(
                description=
                f"The roles `{', '.join(add)}` have been added \nThe roles `{', '.join(remove)}` have been removed",
                color=cyan)
            await ctx.send(embed=embed)

        except commands.RoleNotFound as e:
            embed = discord.Embed(
                description=f"The role `{e.argument}` couldn't be found",
                color=cyan)
            embed.set_footer(
                text=
                "Make sure to keep spaces between each of the role names, and the '|'"
            )
            await ctx.reply(embed=embed)

    @commands.command(aliases=["dc", "disable"])
    async def disablecommand(self, ctx, command):
        if command == "enablecommand":
            await ctx.reply("nice try, but you can't disable enablecommand 🤡")
            return
        elif str(ctx.guild.id) not in db['disabled'].keys():
            db['disabled'][str(ctx.guild.id)] = []
        elif command in db['disabled'][str(ctx.guild.id)]:
            await ctx.reply("this command is already disabled f")
            return

        if command in [i.name for i in client.commands]:
            l = db['disabled'][str(ctx.guild.id)]
            l.append(command)
            db['disabled'][str(ctx.guild.id)] = l

            embed = discord.Embed(
                description=f"The command `{command}` has been successfully disabled.",
                color=cyan)
            await ctx.send(embed=embed)
    
    @commands.command(aliases=["ec", "enable"])
    async def enablecommand(self, ctx, command):

        if str(ctx.guild.id) not in db['disabled'].keys():
            db['disabled'][str(ctx.guild.id)] = []
            await ctx.reply("This command wasn't disabled in the first place")
            return
        elif command not in db['disabled'][str(ctx.guild.id)]:
            await ctx.reply("this command wasn't disabled in the first place")
            return

        if command in [i.name for i in client.commands]:
            l = db['disabled'][str(ctx.guild.id)]
            l.remove(command)
            db['disabled'][str(ctx.guild.id)] = l

            embed = discord.Embed(
                description=f"The command `{command}` has been successfully enabled.",
                color=cyan)
            await ctx.send(embed=embed)

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
        embed = discord.Embed(
            description=
            f"The role(s) `{s}` will now be able to do staff commands",
            color=cyan)
        embed.set_footer(
            text=
            "Having the administrator permission will let you do all staff commands"
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['astaff'])
    async def addstaff(self, ctx, role: discord.Role):

        if str(ctx.guild.id) not in db['staff'].keys():
            db['staff'][str(ctx.guild.id)] = [role.id]
        else:
            staff = db['staff'][str(ctx.guild.id)]
            staff.append(role.id)
            db['staff'][str(ctx.guild.id)] = staff

        embed = discord.Embed(
            description=
            f"The role `{role}` will now be able to do staff commands",
            color=cyan)
        embed.set_footer(
            text=
            "Having the administrator permission will let you do all staff commands"
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['rstaff'])
    async def removestaff(self, ctx, role: discord.Role):

        staff = db['staff'][str(ctx.guild.id)]
        staff.remove(role.id)
        db['staff'][str(ctx.guild.id)] = staff

        embed = discord.Embed(
            description=
            f"The role `{role}` will no longer be able to do staff commands",
            color=cyan)
        embed.set_footer(
            text=
            "Having the administrator permission will let you do all staff commands"
        )
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


def setup(client):
    client.add_cog(Mod(client))
