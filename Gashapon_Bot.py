from discord.ext.commands import Bot
import random

bot = Bot(command_prefix="~")
TOKEN = ''


pools = "[REDACTED]"


@bot.command(description='Creates a profile for the user (probably will be removed)',
             brief='Makes a profile so you can keep all your progress',
             pass_context=True)
async def make_profile(ctx):
    return await ctx.send("Your profile has been made. Is what I would say if I could do that.")


@bot.command(description='Displays various stats on the user profile',
             brief='Shows the basics stats of your profile',
             pass_context=True)
async def view_profile(ctx):
    return await ctx.send("Here is your profile: [INSERT PROFILE HERE]")


@bot.command(description='adds tokens used for summoning to the user`s profile',
             brief='Used once a day to get some Summoning Tokens',
             pass_context=True)
async def daily_gift(ctx):
    return await ctx.send("Here are your Summoning Tokens for today; You get [AMOUNT]. Use them wisely!")


@bot.command(description='Displays the pools available to summon from',
             brief='Shows the available Gocha Machine for summoning',
             pass_context=True)
async def view_pools(ctx):
    return await ctx.send("Here are the available Gocha Machines: [DISPLAY LIST]")


@bot.command(description='Displays more detailed information about the pool',
             brief='Show the prizes that are a given Machine',
             pass_context=True)
async def view_pool(ctx, pool):
    return await ctx.send("Here are the prizes that are inside " + pool + ": [INSERT PRIZES AND CHANCES TO GET THEM]")


@bot.command(descprition='Displays the desired number of prizes randomly chosen from the desired pool',
             brief='Get prizes from a specific Gocha Machine',
             pass_context=True)
async def summon_from(ctx, pool, number=1):
    return await ctx.send("I am getting " + str(number) + " of prizes for you from the " + pool +
                          "Gocha Machine... And I got [SHOW PRIZES WON]")


@bot.command(description='Will merge the second character into the first given that the characters are the same',
             brief='Merge two of the same prize together. The second will be consumed to make the first stronger',
             pass_context=True)
async def merge(ctx, character_one, character_two):
    return await ctx.send(character_one + " has been merged with " + character_two + " and is now stronger")


@bot.command(description='Displays a list of the prizes the user owns',
             brief='View collected prizes',
             pass_context=True)
async def view_collection(ctx):
    return await ctx.send("Let me gather your Collection real quick... "
                          "Here they are [DISPLAY LIST OF OWNED PRIZES]")


@bot.command(description='Adds more space for the user to collect more characters',
             brief='Adds more space in your Collection so you can collect more prizes',
             pass_context=True)
async def expand_collection(ctx):
    return await ctx.send("I have made your Collection larger")


@bot.command(description='Displays the stats of a prize that the user owns',
             brief='Shows the stats of a prize that you own',
             pass_context=True)
async def view_stats(ctx, prize):
    return await ctx.send("Let me find that prize for you... Here are the stats for the prize [DISPLAY STATS]")


@bot.command(description='Sends a prize that a user owns to gather materials',
             brief='Send a prize that you own on an Expedition to gather materials',
             pass_context=True)
async def collect_materials(ctx, character):
    return await ctx.send("Sending " + character + " to gather materials. Hopefully they find something nice!")


@bot.command(description='Displays all the characters that the user had sent gathering and the time remaining',
             brief='Show the prizes currently on Expeditions and the time remaining on them',
             pass_context=True)
async def view_expeditions(ctx):
    return await ctx.send("Here are your current Expeditions")


@bot.command(description='Adds the ability to have more characters go on expeditions',
             brief='Increase the amount of prizes allowed to go on Expeditions',
             pass_context=True)
async def expand_expeditions(ctx):
    return await ctx.send("More of your prizes can now go on Expeditions")


@bot.command(description='Displays what the user can get from expeditions',
             brief='Explains what Expeditions are and what you can get from them',
             pass_context=True)
async def expedition_details(ctx):
    return await ctx.send("Here is what Expeditions are: [INSERT DETAILED EXPLANATION]")


@bot.command(description='Will level up a character that the user owns by the desired amount',
             brief='Level up a prize that you own',
             pass_context=True)
async def level_up(ctx, prize, number=1):
    return await ctx.send("I have leveled up" + prize + " " + str(number) + " times for you")


@bot.command(description='Adds a level of Ascension to a character that the user owns',
             brief='Adds a level of Ascension to a prize that you own and resets their level back to 1',
             pass_context=True)
async def ascend(ctx, prize):
    return await ctx.send("I have ascended " + prize + " for you. It is now even stronger than before")


# "pool" is the focus group of [characters?] that the user wants to choose from
# Random with replacement; Wouldn't be fun if it were without replacement.
def choose_random(pool):
    return random.choice(pool)


@bot.event
async def on_ready():
    print('Bot logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


bot.run(TOKEN)
