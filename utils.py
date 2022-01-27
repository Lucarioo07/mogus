import discord
import requests
from discord.ext import commands
from discord.ext.buttons import Paginator
from discord_components import DiscordComponents
import datetime
import pytz
from replit import db
import os
import errors

bot_token = os.environ['bot_token']


async def prefix(client, message):
    return db['prefix'][str(message.guild.id)]


client = commands.Bot(command_prefix=prefix)
com = DiscordComponents(client)

safe = [622090741862236200, 888373479655751700]

colors = {
    "WHITE": 0xFFFFFF,
    "AQUA": 0x1ABC9C,
    "GREEN": 0x2ECC71,
    "BLUE": 0x3498DB,
    "PURPLE": 0x9B59B6,
    "LUMINOUS_VIVID_PINK": 0xE91E63,
    "GOLD": 0xF1C40F,
    "ORANGE": 0xE67E22,
    "RED": 0xE74C3C,
    "NAVY": 0x34495E,
    "DARK_AQUA": 0x11806A,
    "DARK_GREEN": 0x1F8B4C,
    "DARK_BLUE": 0x206694,
    "DARK_PURPLE": 0x71368A,
    "DARK_VIVID_PINK": 0xAD1457,
    "DARK_GOLD": 0xC27C0E,
    "DARK_ORANGE": 0xA84300,
    "DARK_RED": 0x992D22,
    "DARK_NAVY": 0x2C3E50,
}
cyan = 65486


async def fetch_webhook(channel: discord.TextChannel):
    global webhook
    webhooks = await channel.webhooks()
    is_made = False
    for i in webhooks:
        if i.name == "amogus":
            webhook = i
            is_made = True
    if not is_made:
        webhook = await channel.create_webhook(name="amogus")
    return webhook


def frame(content, user, hook):
    data = {
        "content": content,
        "username": user.name,
        "avatar_url": str(user.avatar_url),
        "allowed_mentions": {
            "parse": []
        }
    }

    result = requests.post(hook.url, json=data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)


def send_webhook(content, name, avatar, hook):
    data = {
        "content": content,
        "username": name,
        "avatar_url": str(avatar),
        "allowed_mentions": {
            "parse": []
        }
    }

    result = requests.post(hook.url, json=data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)


def clean_code(content):

    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content


class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass


def get_key(val, my_dict):

    for key, value in my_dict.items():
        if val == value:
            return key

    return "key doesn't exist"


# Command Checks


def in_guild(guild_id):
    async def predicate(ctx):
        if ctx.guild and ctx.guild.id == guild_id:
            return True
        else:
            raise errors.WrongServer()

    return commands.check(predicate)


def is_staff():
    async def predicate(ctx):
        if staff_check(ctx.author, ctx.guild):
            return True
        else:
            raise errors.NotStaff()

    return commands.check(predicate)


# Checks and Mod Stuff


def is_owner(user):
    if isinstance(user, discord.User) or isinstance(user, discord.Member):
        return user.id == 622090741862236200
    else:
        return user == 622090741862236200

def is_not_banned(user):
        if isinstance(user, discord.User) or isinstance(user, discord.Member):
            return user.id not in db['banned']
        else:
            return user not in db['banned']
def ban_check(user):
    if is_not_banned(user):
        return True
    else:
        raise errors.UserBanned()


def staff_check(user: discord.Member, guild: discord.Guild):
    if user is int:
        user = client.get_user(user)
    if guild is int:
        guild = client.get_guild(guild)

    for role in user.roles:
        if role.id in db['staff'][str(
                guild.id)] or role.permissions.administrator:
            return True


def disabled_check(guild: discord.Guild, cmd):
    if str(guild.id) in db['disabled'] and cmd in [i for i in db['disabled'][str(guild.id)]]:
        raise errors.CommandDisabled
    else:
        return True


def locked_check(user: discord.User):
    if db['lock'] and not is_owner(user):
        raise errors.BotLocked()
    else:
        return True


def recent_warns(user, guild):
    count = 0
    now = datetime.datetime.now()
    for warn in db['warns'][str(guild)][str(user)].values():
        timestr = warn['time']
        wtime = datetime.datetime.strptime(timestr, "%d %B %Y")
        delta = now - wtime
        if delta.days < 4:
            count += 1
    return count


pun = {
    "30m": datetime.timedelta(minutes=30),
    "1h": datetime.timedelta(hours=1),
    "1d": datetime.timedelta(days=1),
    "3d": datetime.timedelta(days=3)
}

dxb_tz = pytz.timezone("Asia/Dubai")
