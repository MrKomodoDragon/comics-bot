import toml
import discord
from discord.ext import commands
import jishaku

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="comix ", help_command=commands.MinimalHelpCommand())
bot.run(toml.load("config.toml")['token'])