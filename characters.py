from discord.ext import commands


class Characters(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Merge two of the same character together. The second '
                                  'will be consumed to make the first stronger',
                      brief='Merge two of the same character together.',
                      pass_context=True)
    async def merge(self, ctx, character_one, character_two):
        return await self.bot.send(character_one + " has been merged with " + character_two + " and is now stronger")

    @commands.command(description='Displays the stats of a characters that the user owns',
                      brief='Shows the stats of a characters that you own',
                      pass_context=True)
    async def view_stats(self, ctx, character):
        return await self.bot.send(
            "Let me find that character for you... Here are the stats for the character [DISPLAY STATS]")

    @commands.command(description='Will level up a character that the user owns by the desired amount',
                      brief='Level up a character that you own',
                      pass_context=True)
    async def level_up(self, ctx, character, number=1):
        return await self.bot.send("I have leveled up" + character + " " + str(number) + " times for you")

    @commands.command(description='Adds a level of Ascension to a character that '
                                  'you own and resets their level back to 1',
                      brief='Adds a level of Ascension to a character that you own',
                      pass_context=True)
    async def ascend(self, ctx, character):
        return await self.bot.send("I have ascended " + character + " for you. It is now even stronger than before")


def setup(bot):
    bot.add_cog(Characters(bot))
