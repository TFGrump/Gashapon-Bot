from discord.ext import commands
from discord import Embed
import database as db
import gashapon_bot as gb


class Profile(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Creates a profile for the user (probably will be removed)',
                      brief='Makes a profile so you can keep all your progress')
    async def make_profile(self, ctx):
        db.add_user(gb.database, ctx.author.name)
        await ctx.send("Your profile has been made.")
        await self.view_profile(ctx)

    @commands.command(description='Displays various stats on the user profile',
                      brief='Shows the basics stats of your profile',
                      pass_context=True)
    async def view_profile(self, ctx):
        embed = Embed(title='User Profile')
        user = db.lookup_user(gb.database, ctx.author.name)
        print(user)
        embed.add_field(name=user['id'],
                        value='Joined: {}\nOrbs : {}\nAscendant Shards : {}\nLevel Up Shards: {}'
                        .format(user['join_ts'], user['orb_count'], user['ascendent_shard_count'],
                                user['level_up_shard_count']))
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send("Here is your profile:")
        await ctx.send(embed=embed)

    @commands.command(description='adds tokens used for summoning to the user`s profile',
                      brief='Used once a day to get some Summoning Tokens',
                      pass_context=True)
    async def daily_gift(self, ctx):
        db.update_user_orb_count(gb.database, ctx.author.name, 1)
        await ctx.send("Here are your Summoning Tokens for today. Use them wisely!")
        await self.view_profile(ctx)

    @commands.command(description='Displays a list of the characters the user owns',
                      brief='View collected characters',
                      pass_context=True)
    async def view_collection(self, ctx):
        embed = Embed(title='Collection')
        units = db.lookup_units_for_user(gb.database, ctx.author.name)
        for unit in units:
            embed.add_field(name=unit['id'], value="Obtained: {}\nLevel: {}".format(unit['obtain_ts'], unit['level']))
        await ctx.send("Let me gather your Collection real quick... "
                       "Here they are")
        await ctx.send(embed=embed)

    @commands.command(description='Adds more space to your Collection so you can collect more characters',
                      brief='Adds more space to your Collection',
                      pass_context=True)
    async def expand_collection(self, ctx):
        return await ctx.send("I have made your Collection larger")


def setup(bot):
    bot.add_cog(Profile(bot))
