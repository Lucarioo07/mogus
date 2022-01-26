import discord
from discord.ext import commands, tasks
from replit import db
import datetime
from utils import *


class Grade(commands.Cog):
    def __init__(self, client):
        self.client = client

    def cog_check(self, ctx):
        if ctx.guild.id == 764060384897925120:
            return True
        else:
            raise errors.WrongServer()

    # Commands
    @commands.command()
    @is_staff()
    async def warn(self, ctx, warned: discord.Member, *, reason):

        now = datetime.datetime.now(dxb_tz)
        timestr = now.strftime("%d %B %Y")
        try:
            db["warns"][str(ctx.guild.id)][str(warned.id)][str(
                ctx.message.id)] = {
                    "staff": ctx.author.id,
                    "reason": reason,
                    "channel": ctx.channel.id,
                    "time": timestr
                }

        except:
            try:
                db["warns"][str(ctx.guild.id)][str(warned.id)] = {
                    str(ctx.message.id): {
                        "staff": ctx.author.id,
                        "reason": reason,
                        "channel": ctx.channel.id,
                        "time": timestr
                    }
                }
            except:
                db["warns"][str(ctx.guild.id)] = {
                    str(warned.id): {
                        str(ctx.message.id): {
                            "staff": ctx.author.id,
                            "reason": reason,
                            "channel": ctx.channel.id,
                            "time": timestr
                        }
                    }
                }

        embed = discord.Embed(
            description=
            f"***{str(warned)}** was warned by **{str(ctx.author)}** for* **`{reason}`**",
            color=cyan)

        warncount = recent_warns(warned.id, ctx.guild.id)
        muterole = discord.utils.get(ctx.guild.roles, id=764060384956383237)

        footer = ""

        if warncount == 3:
            dtime = now + pun['30m']
            db['punishments']['mute'][str(
                warned.id)] = dtime.strftime("%d %B %Y, %H:%M")
            await warned.add_roles(muterole)
            footer = "User has also been muted for 30m for having 3 warns in the past 3 days. "
        elif warncount == 5:
            dtime = now + pun['1h']
            db['punishments']['mute'][str(
                warned.id)] = dtime.strftime("%d %B %Y, %H:%M")
            await warned.add_roles(muterole)
            footer = "User has also been muted for 1h for having 5 warns in the past 3 days. "
        elif warncount == 7:
            dtime = now + pun['1d']
            db['punishments']['mute'][str(
                warned.id)] = dtime.strftime("%d %B %Y, %H:%M")
            await warned.add_roles(muterole)
            footer = "User has also been muted for 1d having 7 warns in the past 3 days. "
        elif warncount == 10:
            dtime = now + pun['3d']
            db['punishments']['tempban'][str(
                warned.id)] = dtime.strftime("%d %B %Y, %H:%M")
            await ctx.guild.ban(warned)
            footer = "User has also been tempbanned for 3d for having 10 warns in the past 3 days. "

        if staff_check(warned, ctx.guild):

            if warncount > 2:

                staff_rank: discord.Role

                for roleid in db['staff'][str(ctx.guild.id)]:
                    for role in warned.roles:
                        if roleid == role.id:
                            staff_rank = role

                try:
                    demote_role = discord.utils.get(
                        ctx.guild.roles,
                        id=db['staff'][str(
                            ctx.guild.id)][(staff.index(staff_rank.id) + 1)])
                    await warned.add_roles(demote_role)
                    footer = footer + f"Demoted to role of {demote_role.name}"
                except:
                    footer = footer + f"Demoted to Member"
                await warned.remove_roles(staff_rank)

        embed.set_footer(text=footer)
        await ctx.send(embed=embed)
        await warned.send(embed=embed)

    @commands.command()
    @is_staff()
    async def delwarn(self, ctx, warn_id):
        try:
            found = False
            for user in db['warns'][str(ctx.guild.id)].keys():
                if warn_id in db['warns'][str(ctx.guild.id)][user].keys():
                    del db['warns'][str(ctx.guild.id)][user][warn_id]
                    embed = discord.Embed(
                        description=
                        f"*The warn with ID `{warn_id}` has been deleted from **{await client.fetch_user(user)}***",
                        color=cyan)
                    found = True
                    break
            if not found:
                embed = discord.Embed(
                    description=
                    f"A warn with ID `{warn_id}` couldnt't be found",
                    color=cyan)

        except:
            embed = discord.Embed(
                description=
                f"A warn for this user with ID `{warn_id}` couldnt't be found",
                color=cyan)
        await ctx.send(embed=embed)

    @commands.command()
    @is_staff()
    async def editwarn(self, ctx, warn_id, new):
        try:
            found = False
            for user in db['warns'][str(ctx.guild.id)].keys():
                if warn_id in db['warns'][str(ctx.guild.id)][user].keys():
                    db['warns'][str(ctx.guild.id)][user][warn_id] = new
                    embed = discord.Embed(
                        description=
                        f"Warn `{warn_id}` reason has been successfully edited to `{new}`",
                        color=cyan)
                    found = True
                    break
            if not found:
                embed = discord.Embed(
                    description=
                    f"A warn with ID `{warn_id}` couldnt't be found",
                    color=cyan)

        except:
            embed = discord.Embed(
                description=
                f"A warn for this user with ID `{warn_id}` couldnt't be found",
                color=cyan)
        await ctx.send(embed=embed)

    @commands.command()
    @is_staff()
    async def clearwarn(self, ctx, user: discord.User):
        try:
            del db["warns"][str(ctx.guild.id)][str(user.id)]
            await ctx.send(embed=discord.Embed(
                description=f"***{user}** has had their warns cleared*",
                color=cyan))
        except:
            await ctx.send(embed=discord.Embed(
                description=
                f"*It appears **`{user}`** doesn't have any warns, but we could fix that...*",
                color=cyan))

    @commands.command(aliases=["warnings", "oopsies"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def warns(self, ctx, user: discord.User = None):

        if user is None:
            user = ctx.author

        try:
            warns = db["warns"][str(ctx.guild.id)][str(user.id)]

        except Exception as e:
            await ctx.send(embed=discord.Embed(
                description="dam this guy has no warns lmao what", color=cyan))
            return

        if warns == {}:
            await ctx.send(embed=discord.Embed(
                description="dam this guy has no warns lmao what", color=cyan))
        else:
            embed = discord.Embed(title=f"__Warns for {user}__", color=cyan)
            description = "**Context Menu:** \n"
            for value in warns.values():
                warn_id = get_key(value, warns)
                reason = value["reason"]
                channel = await client.fetch_channel(value['channel'])
                timestamp = value["time"]
                msg = await channel.fetch_message(warn_id)

                embed.add_field(
                    name=f"ID: `{warn_id}` \n",
                    value=
                    f"Staff: `{await client.fetch_user(value['staff'])}` \n"
                    f"Timestamp: `{timestamp}` \n"
                    f"Reason: \n"
                    f"> **`{reason}`**")
                if len(reason) <= 20:
                    description += f'> [**{reason}**]({msg.jump_url} "Warn ID: {warn_id}") \n'
                else:
                    description += f'> [**{reason[0:20]}...**]({msg.jump_url} "Warn ID: {warn_id}") \n'
            embed.description = description
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Grade(client))
