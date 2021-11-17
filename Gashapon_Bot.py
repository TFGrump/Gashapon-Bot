from discord.ext.commands import Bot

bot = Bot(command_prefix="~")
TOKEN = ''


async def on_ready():
    print('Bot logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def hi(ctx):
    await ctx.send('hi')


bot.run(TOKEN)
