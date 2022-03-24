import discord
from discord.ext import commands
from game_stuff import moves, info
from utils import *


class Game(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    cog_help(name="Game", 
            desc="Commands related to the bots custom Dragon-Ball Z game. Use the info command to learn how to play. (Caution: not factually accurate)")
    
    @commands.command(aliases=["dbzinfo", "info"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @command_help(name="DBZ_info", 
                  desc="Gives information on how to play the Dragon-Ball Z game", 
                  syntax="info",
                  cog="Game",
                  aliases=["dbzinfo, info"])
    async def dbz_info(self, ctx):

        embed = discord.Embed(
            title="Yes so basically...",
            description=
            "This command is based off of a hand game I used to play with my friends, and though it might not be entirely factually correct, I hope its still fun :) \n"
            "The syntax for the command is `>fight <mention> [reloads] [saiyan]`. Leaving saiyan or reloads blank will default it to 0. "
            "The game itself is simple, each use of `Reload` gives you a reload, the energy used to pull off the attacks. "
            "The more reloads an attack needs, more powerful the move is. "
            "Using a move that costs more reloads than you have results in `Overloading`, which kills you regardless of your super-saiyan level. "
            "The price of each attack is put next to the button. "
            "Green buttons are power up moves, red buttons are attacks, and blue buttons are defensive. "
            "Each of the defensive moves have pros and cons, which will be listed below, read or else <:gru_gun:786829006476410910>. "
            "Hope you enjoy!",
            color=cyan)

        movelist = ['reload', 'kame', 'double', 'slash', 'spirit', 'fist', 'reflect', 'block', 'tp', 'saiyan']
        for move in movelist:
            embed.add_field(name=info[f"{move}_title"], value=info[f"{move}_desc"])

        await ctx.send(embed=embed)

    @commands.command(aliases=["fight", "dbz"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @command_help(name="Challenge", 
                  desc="Challenge a user to a game of Dragon-Ball Z. You can set your starting super-saiyan level or reloads", 
                  syntax="fight <opponent> [reloads] [saiyan]",
                  cog="Game",
                  aliases=["fight, dbz"])
    async def challenge(self,
                        ctx,
                        opponent: discord.Member,
                        reloads=0,
                        saiyan=0):

        global message, embed
        sender = ctx.author

        challenge_embed = discord.Embed(
            title=f"You have been challenged to a battle by {ctx.author.name}",
            description="Do you accept or not?",
            color=cyan)

        challenge_embed.add_field(
            name="__**Details**__",
            value=f"**Super-Saiyan:** `{saiyan}`\n**Reloads:** `{reloads}`")
        ch = await ctx.send(f"{opponent.mention}",
                            embed=challenge_embed,
                            components=[[
                                Button(style=ButtonStyle.green,
                                       label="Yes",
                                       custom_id="y"),
                                Button(style=ButtonStyle.red,
                                       label="No",
                                       custom_id="n")
                            ]])

        while True:
            try:
                inter = await client.wait_for("button_click", timeout=60.0)
            except:
                for component in ch.components:
                    for button in component:
                        button.disabled = True
                await ch.edit(components=ch.components)
                await ctx.message.reply("The challenge timed out...")
                return
            else:
                clicker_id = inter.user.id
                response = inter.custom_id
                battle = None
                if clicker_id == opponent.id or clicker_id == 622090741862236200:
                    if response == 'y':
                        await inter.send(
                            content="You accepted the challenge request")
                        await ctx.send("Let the battle begin!")

                        embed = discord.Embed(title="Select Your Moves!",
                                              color=cyan)
                        message = await ctx.send(
                            content=f"{ctx.author.mention} {opponent.mention}",
                            embed=embed)

                        battle = True
                    elif response == 'n':
                        await inter.send(
                            content="You declined the challenge request")
                        await inter.send("Declined :crying_cat_face:")
                        battle = False

                    for component in ch.components:
                        for button in component:
                            button.disabled = True
                    await ch.edit(components=ch.components)
                    break

        move = 0

        sender_saiyan = saiyan + 1
        sender_tp = 0
        sender_reloads = reloads

        opponent_saiyan = saiyan + 1
        opponent_tp = 0
        opponent_reloads = reloads

        output = None

        global hax

        while battle:
            move += 1

            embed.description = f"**{ctx.author.name}**'s Reloads: `{sender_reloads}` \n" \
                                f"**{ctx.author.name}**'s Super-Saiyan Level:  `{sender_saiyan-1}` \n" \
                                f"\n" \
                                f"**{opponent.name}**'s Reloads: `{opponent_reloads}` \n" \
                                f"**{opponent.name}**'s Super-Saiyan Level: `{opponent_saiyan-1}`"

            await message.edit(embed=embed,
                               components=[
                                   [
                                       Button(style=ButtonStyle.green,
                                              label="Reload",
                                              custom_id="Reload"),
                                       Button(style=ButtonStyle.green,
                                              label="Super Saiyan (6)",
                                              custom_id="Super Saiyan")
                                   ],
                                   [
                                       Button(style=ButtonStyle.red,
                                              label="Kamehameha (1)",
                                              custom_id="Kamehameha"),
                                       Button(style=ButtonStyle.red,
                                              label="Double Kamehameha (2)",
                                              custom_id="Double Kamehameha"),
                                       Button(style=ButtonStyle.red,
                                              label="Slash (4)",
                                              custom_id="Slash"),
                                       Button(style=ButtonStyle.red,
                                              label="Spirit Bomb (6)",
                                              custom_id="Spirit Bomb"),
                                       Button(style=ButtonStyle.red,
                                              label="Dragon Fist (8)",
                                              custom_id="Dragon Fist"),
                                   ],
                                   [
                                       Button(style=ButtonStyle.blue,
                                              label="Reflect",
                                              custom_id="Reflect"),
                                       Button(style=ButtonStyle.blue,
                                              label="Block",
                                              custom_id="Block"),
                                       Button(style=ButtonStyle.blue,
                                              label="Teleport",
                                              custom_id="Teleport")
                                   ],
                               ])

            sender_move = None
            opponent_move = None
            sender_picked = False
            opponent_picked = False
            footer = ""

            while True:

                try:
                    inter = await client.wait_for(
                        "button_click",
                        timeout=15.0,
                        check=lambda x: x.message.id == message.id)
                except:

                    for component in ch.components:
                        for button in component:
                            button.disabled = True
                    await ch.edit(components=ch.components)

                    if (not sender_picked) and (not opponent_picked):
                        embed = discord.Embed(
                            title=f"__**Its a tie!**__",
                            description=f"`Reason:` Both users timed out...",
                            color=cyan)
                    elif sender_picked:
                        embed = discord.Embed(
                            title=f"Game Over, {ctx.author.name} wins!",
                            description=
                            f"`Reason:` Both {opponent.name} timed out...",
                            color=cyan)
                    elif opponent_picked:
                        embed = discord.Embed(
                            title=f"Game Over, {opponent.name} wins!",
                            description=
                            f"`Reason:` {ctx.author.name} timed out...",
                            color=cyan)
                    await ctx.send(f"{ctx.author.mention} {opponent.mention}",
                                   embed=embed)
                    return

                else:
                    clicker_id = inter.user.id

                    if clicker_id == ctx.author.id:
                        sender_move = inter.custom_id

                        if not sender_picked:

                            footer = footer + f"({ctx.author.name} is ready) "
                            embed.set_footer(text=footer)
                            await inter.send(
                                content=f"You picked the move `{sender_move}`")
                            await message.edit(embed=embed)
                            sender_picked = True
                        else:
                            await inter.send(
                                "You can't change your move after its picked 😔😔"
                            )

                    if clicker_id == opponent.id:
                        opponent_move = inter.custom_id

                        if not opponent_picked:

                            footer = footer + f"({opponent.name} is ready) "
                            embed.set_footer(text=footer)
                            await inter.send(
                                content=f"You picked the move `{opponent_move}`"
                            )
                            await message.edit(embed=embed)
                            opponent_picked = True
                        else:
                            await inter.send(
                                "You can't change your move after its picked 😔😔"
                            )

                    if sender_move and opponent_move is not None:
                        embed.set_footer(text="")
                        await message.edit(embed=embed)
                        break

            # __Game Logic here__

            s_action = moves[sender_move]
            o_action = moves[opponent_move]

            # super saiyan logic
            if sender_move == "Super Saiyan":
                sender_saiyan += 1

            if opponent_move == "Super Saiyan":
                opponent_saiyan += 1

            # giving one extra reload for using Reload and taking away reloads for using a move
            if sender_move == "Reload":
                sender_reloads += 1
            else:
                sender_reloads -= s_action["Cost"]

            if opponent_move == "Reload":
                opponent_reloads += 1
            else:
                opponent_reloads -= o_action["Cost"]

            # causing death for using teleport more than twice in a row
            if sender_move == "Teleport":
                sender_tp += 1
            else:
                sender_tp = 0
            if opponent_move == "Teleport":
                opponent_tp += 1
            else:
                opponent_tp = 0

            if sender_tp or opponent_tp > 1:

                if sender_tp > 1:
                    sender_reloads = -1

                if opponent_tp > 1:
                    opponent_reloads = -1

            if (sender_reloads >= 0) and (opponent_reloads >= 0):

                # if both moves are attacks
                if (s_action["Type"] == 0) and (o_action["Type"] == 0):

                    result = (s_action["Attack"] + sender_saiyan) - (
                        o_action["Attack"] + opponent_saiyan)

                    if result > 0:
                        opponent_saiyan -= 1
                        output = f"**{ctx.author.name}**'s attack was more powerful than that of **{opponent.name}**."
                    elif result < 0:
                        sender_saiyan -= 1
                        output = f"**{opponent.name}**'s attack was more powerful than that of **{ctx.author.name}**."

                # there is no code for if both moves are blocks as nothing would happen.

                # if one is an attack and one is a block
                if sender_move == "Kamehameha" and opponent_move == "Reflect":
                    sender_saiyan -= 1
                    output = f"**{ctx.author.name}**'s `Kamehameha` was sent back by **{opponent.name}**'s `Reflect`."
                elif opponent_move == "Kamehameha" and sender_move == "Reflect":
                    opponent_saiyan -= 1
                    output = f"**{opponent.name}**'s `Kamehameha` was sent back by **{ctx.author.name}**'s `Reflect`."
                elif ((s_action["Type"] == 1) and
                      (o_action["Type"] == 0)) or ((s_action["Type"] == 0) and
                                                   (o_action["Type"] == 1)):

                    if (s_action["Type"] == 1) and (o_action["Type"] == 0):
                        result = s_action["Defense"] - (o_action["Attack"] +
                                                        opponent_saiyan)

                        if result < 0:
                            sender_saiyan -= 1
                            output = f"**{opponent.name}**'s attack broke through **{ctx.author.name}**'s defense."

                    elif (s_action["Type"] == 0) and (o_action["Type"] == 1):
                        result = o_action["Defense"] - (s_action["Attack"] +
                                                        sender_saiyan)

                        if result < 0:
                            opponent_saiyan -= 1
                            output = f"**{ctx.author.name}**'s attack broke through **{opponent.name}**'s defense."

            # if you use more reloads than you have, "overloading"
            elif (sender_reloads < 0) and (opponent_reloads < 0):
                sender_saiyan = 0
                opponent_saiyan = 0
                output = "Both users overloaded lmfao what"
            else:
                if sender_reloads < 0:
                    sender_saiyan = 0
                    if sender_move == "Teleport":
                        output = f"{ctx.author.name} was split into a million atoms when they tried to teleport twice in a row"
                    else:
                        output = f"{ctx.author.name} overloaded when he tried to use {sender_move}"
                if opponent_reloads < 0:
                    opponent_saiyan = 0
                    if opponent_move == "Teleport":
                        output = f"{opponent.name} was split into a million atoms when they tried to teleport twice in a row"
                    else:
                        output = f"{opponent.name} overloaded when he tried to use {opponent_move}"

            embed.add_field(
                name=f"`Move {move}`",
                value=f"> {ctx.author.mention} used `{sender_move}`. \n"
                f"> {opponent.mention} used `{opponent_move}`",
            )

            # __Checking for loss here__

            if (sender_saiyan < 1) and (opponent_saiyan < 1):

                output = "`Reason:` " + output

                embed = discord.Embed(title="__**Its a tie!**__",
                                      description=f"{output}",
                                      color=cyan)

                embed.add_field(
                    name=f"`Move {move}`",
                    value=f"> {ctx.author.mention} used `{sender_move}`. \n"
                    f"> {opponent.mention} used `{opponent_move}`",
                )

                embed.set_footer(
                    text=
                    "Note: The reason might not always be exactly accurate.")
                await ctx.send(embed=embed)

                for component in ch.components:
                    for button in component:
                        button.disabled = True
                await ch.edit(components=ch.components)

                break
            elif (sender_saiyan < 1) or (opponent_saiyan < 1):

                output = "`Reason:` " + output

                if sender_saiyan < 1:
                    embed = discord.Embed(
                        title=f"Game Over, {opponent.name} wins!",
                        description=f"{output}",
                        color=cyan)

                    embed.add_field(
                        name=f"`Move {move}`",
                        value=f"> {ctx.author.mention} used `{sender_move}`. \n"
                        f"> {opponent.mention} used `{opponent_move}`",
                    )

                    embed.set_footer(
                        text=
                        "Note: reason might not always be exactly accurate.")
                    await ctx.send(embed=embed)
                elif opponent_saiyan < 1:
                    embed = discord.Embed(
                        title=f"Game Over, {ctx.author.name} wins!",
                        description=f"{output}",
                        color=cyan)

                    embed.add_field(
                        name=f"`Move {move}`",
                        value=f"> {ctx.author.mention} used `{sender_move}`. \n"
                        f"> {opponent.mention} used `{opponent_move}`",
                    )

                    embed.set_footer(
                        text=
                        "Note: The reason might not always be exactly accurate."
                    )
                    await ctx.send(embed=embed)

                for component in ch.components:
                    for button in component:
                        button.disabled = True
                await ch.edit(components=ch.components)

                break


def setup(client):
    client.add_cog(Game(client))
