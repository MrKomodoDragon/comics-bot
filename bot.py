import toml
import discord
from core.custombot import ComicsBot
from discord.ext import commands
import jishaku

intents = discord.Intents.default()
intents.message_content = True
bot = ComicsBot(command_prefix="comix ", help_command=commands.MinimalHelpCommand(), intents=intents)
bot.run(toml.load("config.toml")['token'])