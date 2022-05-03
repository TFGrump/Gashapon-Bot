from discord.ext import commands
from discord import Embed
import database as db
import gashapon_bot as gb
import random


class Profile(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        description='Creates a profile for the user (probably will be removed)',
        brief='Makes a profile so you can keep all your progress'
    )
    async def make_profile(self, ctx):
        # Determines if a profile needs to be made for a user, then shows it in a user-friendly way
        if db.add_user(gb.database, ctx.author.name):
            await ctx.send("Your profile has been made.")
        else:
            await ctx.send("You have already made a profile.")
        await self.view_profile(ctx)

    @commands.command(
        description='Displays various stats on the user profile',
        brief='Shows the basics stats of your profile',
        pass_context=True
    )
    async def view_profile(self, ctx):
        # Grabs the user's profile for the database
        user = db.lookup_user(gb.database, ctx.author.name, add_nonexistent_user=False)

        # Checks to see if the user is even in the database. If not, then a profile will be made.
        if user is None:
            await ctx.send("Seems like you have not make a profile yet, let me do that for you.")
            await self.make_profile(ctx)
            # Used only if the first one did not succeed
            user = db.lookup_user(gb.database, ctx.author.name, add_nonexistent_user=False)

        # Sets up, makes, and sends a user-friendly way for reading their profile
        embed = Embed(title='User Profile')
        embed.add_field(
            name=user['id'],
            value='Joined: {}\nOrbs : {}\nAscendant Shards : {}\nLevel Up Shards: {}'.format(
                user['join_ts'],
                user['orb_count'],
                user['ascendant_shard_count'],
                user['level_up_shard_count']
            )
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send("Here is your profile:")
        await ctx.send(embed=embed)

    @commands.command(
        description='Adds tokens used for summoning to the user`s profile',
        brief='Used once a day to get some Summoning Tokens',
        pass_context=True
    )
    async def daily_gift(self, ctx):
        # Adds a random amount of tokens (from 5 to 20, inclusive) to the user's profile
        token_amount = random.randrange(5, 21)
        db.update_user_orb_count(gb.database, ctx.author.name, token_amount)
        await ctx.send("Here are your Summoning Tokens ({}) for today. Use them wisely!".format(token_amount))
        await self.view_profile(ctx)

    @commands.command(
        description='Displays a list of the characters the user owns',
        brief='View collected characters',
        pass_context=True
    )
    async def view_collection(self, ctx):
        # NOTE: Paging is done due to the fact that Discord only allows 25 fields per embed.
        #       More info on Discord embed limitations: https://discord.com/developers/docs/resources/channel#embed-object-embed-limits
        page = 1
        embed = Embed(title='Collection: Page {}'.format(page))
        embeds = []
        i = 0
        for unit in db.lookup_units_for_user(gb.database, ctx.author.name):
            # Grabbing the hero form the database so the character's/unit's name can be accessed.
            hero = db.lookup_hero(gb.database, unit['hero_id'])
            embed.add_field(name=hero['name'], value="Obtained: {}\nLevel: {}".format(unit['obtain_ts'], unit['level']))
            i += 1

            # Makes a new page if all the fields of an Embed are used up.
            if i % 25 == 0:
                embeds.append(embed)
                page = page + 1
                embed = Embed(title='Collection: Page {}'.format(page))
        embeds.append(embed)

        # The bot sends 'pages' of the characters/units the user owns
        await ctx.send("Let me gather your Collection real quick...\nHere they are")
        for embed in embeds:
            await ctx.send(embed=embed)

    @commands.command(
        description='Adds more space to your Collection so you can collect more characters',
        brief='Adds more space to your Collection',
        pass_context=True
    )
    async def expand_collection(self, ctx):
        return await ctx.send("I have made your Collection larger")


def setup(bot):
    bot.add_cog(Profile(bot))
