import discord
from discord.ext import commands
from replit import db
import os

cyan = 65486
log = 936979333891903518


async def prefix(client, message):
    try:
        return commands.when_mentioned_or(db['prefix'][str(message.guild.id)])(client, message)
    except:
        db['prefix'][str(message.guild.id)] = ">"
        return commands.when_mentioned_or(">")(client, message)


class Pegasus(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix=prefix, intents=intents)

    async def on_ready(self):

        activity = discord.Game(name=">help")
        await self.change_presence(activity=activity, status=discord.Status.dnd)
    
        for filename in os.listdir('./cogs'):
            if filename.endswith(".py"):
                self.load_extension(f"cogs.{filename[:-3]}")
        
        print(f"{self.user} is now online.")

    async def on_guild_join(self, guild):
        if str(guild.id) not in db['prefix'].keys():
            db['prefix'][str(guild.id)] = ">"
    
        embed = discord.Embed(title="Thanks for inviting me!",
                              description="My prefix is `>`, but if you want to change that then use the `prefix` command. "
                                          "Use `help` to get more info on any field or command. To set staff roles, use the `sstaff` command",
                              color=cyan
                             )
        channel = guild.system_channel or guild.text_channels[0]
        await channel.send(embed=embed)

    async def on_command(self, ctx):
        logchannel = await client.fetch_channel(log)
        embed = discord.Embed(
            description=
            f"`{ctx.author}` used command `{ctx.command}` with args `{ctx.message.content[len(ctx.command.name)+1:]} `",
            timestamp=ctx.message.created_at,
            color=cyan
        )
        await logchannel.send(embed=embed)

client = Pegasus()

