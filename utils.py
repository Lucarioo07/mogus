import discord
import requests
from discord.ext import commands
from discord.ext.buttons import Paginator
from discord_components import DiscordComponents
from replit import db
import os

bot_token = os.environ['bot_token']

client = commands.Bot(command_prefix=">")  
com = DiscordComponents(client)

staff = [764063896478154754, 764063938370469888, 764064311722508288, 764064474323746826]

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
          return ctx.guild and ctx.guild.id == guild_id
      return commands.check(predicate)
    
def is_not_banned():
  async def predicate(ctx):
    return ctx.author.id not in db['banned']
  return commands.check(predicate)

def is_staff():
  async def predicate(ctx):
    for role in ctx.author.roles:
      if role.id in staff:
        return True
  return commands.check(predicate)
