from discord.ext import commands


class Expeditions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Send a character that you own on an Expedition to gather materials',
                      brief='Send a character that you own on an Expedition',
                      pass_context=True)
    async def collect_materials(self, character):
        return await self.bot.send("Sending " + character + " to gather materials. Hopefully they find something nice!")

    @commands.command(description='Show the characters currently on Expeditions and the time remaining on them',
                      brief='Show the characters currently on Expeditions',
                      pass_context=True)
    async def view_expeditions(self):
        return await self.bot.send("Here are your current Expeditions")

    @commands.command(description='Increase the amount of characters allowed to go on Expeditions',
                      brief='Increase Expeditions slots',
                      pass_context=True)
    async def expand_expeditions(self):
        return await self.bot.send("More of your characters can now go on Expeditions")

    @commands.command(description='Displays what the user can get from expeditions',
                      brief='Explains what Expeditions',
                      pass_context=True)
    async def expedition_details(self):
        return await self.bot.send("Here is what Expeditions are: [INSERT DETAILED EXPLANATION]")


def setup(bot):
    bot.add_cog(Expeditions(bot))
