import discord
from discord import app_commands
from discord.ext import commands
import datetime
import bs4

class GoComics(app_commands.Group):
	def __init__(self, *args, **kwargs):
		self.bot = kwargs.pop("bot")
		super().__init__(*args, **kwargs)
	@app_commands.command()
	@app_commands.describe(comicname="The name of the comic you want to see")
	async def today(self, interaction: discord.Interaction, comicname: str):
		today = datetime.date.today().strftime("%Y/%m/%d")
		comicname = comicname.replace(" ", "").casefold()
		async with self.bot.session.get(f"https://gocomics.com/{comicname}/{today}") as r:
			if r.status == 404:
				await interaction.response.send_message("Comic not found :(")
			else:
				await interaction.response.defer()
				data = await r.text()
				parser = bs4.BeautifulSoup(data, "html.parser")
				comic = parser.find("picture", class_="item-comic-image")
				embed = discord.Embed(title=comic.img['alt'], color=0x0000FF, url=f"https://gocomics.com/{comicname}/{today}") #type: ignore
				embed.set_image(url=comic.img['src']) #type: ignore
				await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
	bot.tree.add_command(GoComics(bot=bot, description="Group for commands related to GoComics"), guild=discord.Object(id=842459680436781078))

