from discord.ext import commands
from discord import Embed
import database as db

bot = commands.Bot(command_prefix="~")
bot.load_extension('profile')
bot.load_extension('summoning')
bot.load_extension('characters')
bot.load_extension('expeditions')
TOKEN = ''

database = db.open_db('test.db')


@bot.event
async def on_ready():
    print('Bot logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


bot.run(TOKEN)
