from discord.ext import commands
from discord import Embed
import database as db
import gashapon_bot as gb


class Summoning(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        description='Displays the pools available to summon from',
        brief='Shows the available Gocha Machine for summoning',
        pass_context=True
    )
    async def view_pools(self, ctx):
        pools = db.lookup_all_pools(gb.database)  # Grabs all the pools in the database

        # Sets up, makes, and sends a user friendly way of reading what pools are available
        embed = Embed(title='Pools')
        for pool in pools:
            embed.add_field(name=pool['name'], value='ID: {}'.format(pool['id']))
        await ctx.send("Here are the available Gocha Machines:\n")
        await ctx.send(embed=embed)

    @commands.command(
        description='Displays more detailed information about the pool',
        brief='Show the characters that are a given Machine',
        pass_context=True
    )
    async def view_pool(self, ctx, pool):
        await ctx.send("Here are the characters that are inside " + pool +
                       ": [INSERT CHARACTERS AND CHANCES TO GET THEM]")

    @commands.command(
        description='* Displays the desired number of characters randomly chosen from the desired pool.\n'
                    '\n* The pool ID is used for \"pool\".\n'
                    '* Any number greater than 1 can be used for \"units_to_be_summoned\"  if you wanted '
                    'to summon more than one unit.\n\n'
                    'Example:\n(summons 5 characters from the pool with ID 1)\n  ~summon_from 1 5',
        brief='Get characters from a specific Gocha Machine',
        pass_context=True
    )
    async def summon_from(self, ctx, pool, units_to_be_summoned=1):
        token_count = db.lookup_user(gb.database, ctx.author.name, add_nonexistent_user=False)["orb_count"]

        # The initial 'if' is used to make sure the user can even summon a character/unit to begin with, and does not
        # have to go through all the other checks to finish executing the function.
        if token_count >= 5:
            embeds = []  # Will be implemented when art is added so the picture of the character can be the "thumbnail"
            number = units_to_be_summoned

            """
            Summons the desired number of characters/units. It also checks before summoning to see if the user has
            enough tokens so the user doesn't get any 'free' characters/units.
            """
            while number > 0 and token_count >= 5:
                # Summons the character/unit
                db.update_user_orb_count(gb.database, ctx.author.name, -5)
                token_count = db.lookup_user(gb.database, ctx.author.name, add_nonexistent_user=False)["orb_count"]
                unit = db.summon_unit(gb.database, pool, ctx.author.name)

                # Sets up and makes a user friendly way of seeing what the got.
                hero = db.lookup_hero(gb.database, unit['hero_id'])
                embed = Embed(title='Unit')
                embed.add_field(
                    name=hero['name'],
                    value="Obtained: {}\nLevel: {}".format(unit['obtain_ts'], unit['level'])
                )
                embeds.append(embed)
                number -= 1

            # Some text to show that the bot was working on something; also shows what the user got from summoning.
            if number > 0:
                await ctx.send("Looks like you ran out of tokens and I was not able to summon the remaining {} like "
                               "you wanted. But...".format(number))
            units_summoned = units_to_be_summoned - number
            await ctx.send("I got " + str(units_summoned) + " characters for you from the " + str(pool) +
                           " Gocha Machine:")
            for e in embeds:
                await ctx.send(embed=e)
        else:
            await ctx.send("I am sorry, but you don't have enough tokens to summon any characters.")


def setup(bot):
    bot.add_cog(Summoning(bot))
