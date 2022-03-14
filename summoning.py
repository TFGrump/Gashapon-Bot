from discord.ext import commands
from discord import Embed
import database as db
import gashapon_bot as gb


class Summoning(commands.Cog):


    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Displays the pools available to summon from',
                      brief='Shows the available Gocha Machine for summoning',
                      pass_context=True)
    async def view_pools(self, ctx):
        pools = db.lookup_all_pools(gb.database)
        embed = Embed(title='Pools')
        for pool in pools:
            embed.add_field(name=pool['name'], value='ID: {}'.format(pool['id']))
        await ctx.send("Here are the available Gocha Machines:\n")
        await ctx.send(embed=embed)

    @commands.command(description='Displays more detailed information about the pool',
                      brief='Show the characters that are a given Machine',
                      pass_context=True)
    async def view_pool(self, ctx, pool):
        await ctx.send("Here are the characters that are inside " + pool +
                       ": [INSERT CHARACTERS AND CHANCES TO GET THEM]")

    @commands.command(description='Displays the desired number of characters randomly chosen from the desired pool.\n'
                                  'Use the \"pool id\" when you are writing the command.',
                      brief='Get characters from a specific Gocha Machine',
                      pass_context=True)
    async def summon_from(self, ctx, pool, number=1):
        unit = db.summon_unit(gb.database, pool, ctx.author.name)
        embed = Embed(title='Collection')
        embed.add_field(name=unit['id'], value="Obtained: {}\nLevel: {}".format(unit['obtain_ts'], unit['level']))
        await ctx.send("I am getting " + str(number) + " of characters for you from the " + str(pool) +
                       " Gocha Machine... And I got:")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Summoning(bot))
