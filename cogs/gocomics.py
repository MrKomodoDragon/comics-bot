import discord
from discord import app_commands
from discord.ext import commands
import datetime
import bs4

class GoComics(app_commands.Group):
	@app_commands.command()
	async def today(self, interaction: discord.Interaction, comicname: str):
		today = datetime.date.today().strftime("%Y/%m/%d")
		async with interaction.client.session.get(f"https://gocomics.com/{comicname}/{today}") as r:
			if r.status == 404:
				await interaction.message.reply("Comic not found :(")
			else:
				await interaction.response.defer()
				data = await r.text()
				parser = bs4.BeautifulSoup(data, "html.parser")
				comic = parser.find("picture", class_="item-comic-image")
				embed = discord.Embed(title=comic.img['alt'], color=0x0000FF, url=f"https://gocomics.com/{comicname}/{today}")
				await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
	bot.tree.add_command(GoComics(description="Group for commands related to GoComics"), guild=discord.Object(id=842459680436781078))
	await bot.tree.sync(guild=discord.Object(id=842459680436781078))
