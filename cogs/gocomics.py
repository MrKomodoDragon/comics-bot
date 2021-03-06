import re
import discord
from discord import app_commands
from discord.ext import commands
import datetime
import bs4
from rapidfuzz import process
import typing

class GoComicsDate(typing.NamedTuple):
    year: int
    month: int
    day: int

class GoComicsDateTransformer(app_commands.Transformer):
    @classmethod
    async def transform(cls, interaction: discord.Interaction, value: str) -> typing.Optional[GoComicsDate]:
        if not re.fullmatch(r"^\d{4}(-|/)\d{1,2}(-|/)\d{1,2}", value):
            await interaction.response.send_message("The date format must be in yyyy-mm-dd format :).")
            return
        await interaction.response.send_message(interaction.locale.__str__())
        thing = re.split(r"(-|/)", value)
        return GoComicsDate(year=thing[0], month=thing[2], day=thing[4])

async def comicname_autocomplete(
interaction: discord.Interaction,
current: str,
) -> app_commands.Choice[str]:  # type:ignore
    choices = [
        "Aaggghhh",
        "The Academia Waltz",
        "Adam@Home",
        "Adult Children",
        "The Adventures of Business Cat",
        "Agnes",
        "AJ and Magnus",
        "Lalo Alcaraz",
        "Lalo Alcaraz en Español",
        "Ali's House",
        "Alley Oop",
        "Amanda the Great",
        "Nick Anderson",
        "Andertoons",
        "Andy Capp",
        "Angry Little Girls",
        "Animal Crackers",
        "Annie",
        "The Argyle Sweater",
        "Robert Ariail",
        "Arlo and Janis",
        "Ask Shagg",
        "Aunty Acid",
        "The Awkward Yeti",
        "B.C.",
        "Back to B.C.",
        "Baby Blues",
        "Back in the Day",
        "bacon",
        "Bad Machinery",
        "Bad Reporter",
        "Badlands",
        "Baldo",
        "Baldo en Español",
        "Ballard Street",
        "Banana Triangle",
        "Barkeater Lake",
        "The Barn",
        "Barney & Clyde",
        "Basic Instructions",
        "Batch Rejection",
        "Beanie the Brownie",
        "Bear with Me",
        "Beardo",
        "Ben",
        "Benitin y Eneas",
        "Clay Bennett",
        "Lisa Benson",
        "Steve Benson",
        "Berger & Wyse",
        "Berkeley Mews",
        "Betty",
        "BFGF Syndrome",
        "Big Nate",
        "Big Nate: First Class",
        "The Big Picture",
        "Big Top",
        "Bird and Moon",
        "Birdbrains",
        "Bleeker: The Rechargeable Dog",
        "Bliss",
        "Bloom County",
        "Bloom County 2019",
        "Bo Nanas",
        "Bob the Squirrel",
        "Chip Bok",
        "Boomerangs",
        "The Boondocks",
        "The Born Loser",
        "Matt Bors",
        "Bottomliners",
        "Bound and Gagged",
        "Bozo",
        "Break of Day",
        "Breaking Cat News",
        "Steve Breen",
        "Brevity",
        "Brewster Rockit",
        "Chris Britt",
        "Broom Hilda",
        "The Buckets",
        "Buckles",
        "Bully",
        "Buni",
        "El Café de Poncho",
        "Calvin and Hobbes",
        "Calvin and Hobbes en Español",
        "Tim Campbell",
        "Candorville",
        "Stuart Carlson",
        "Catana Comics",
        "Cathy Classics",
        "Cathy Commiserations",
        "Cat's Cafe",
        "Cattitude — Doggonit",
        "C'est la Vie",
        "Cheer Up, Emo Kid",
        "Chuck Draws Things",
        "Chuckle Bros",
        "Citizen Dog",
        "The City",
        "Claw",
        "Cleats",
        "Close to Home",
        "The Comic Strip That Has A Finale Every Day",
        "Compu-toon",
        "Cornered",
        "Cow and Boy Classics",
        "CowTown",
        "Crabgrass",
        "Crumb",
        "Cul de Sac",
        "Daddy's Home",
        "The Daily Drawing",
        "Jeff Danziger",
        "Dark Side of the Horse",
        "Matt Davies",
        "Deep Dark Fears",
        "John Deering",
        "DeFlocked",
        "Diamond Lil",
        "Dick Tracy",
        "Dilbert Classics",
        "Dilbert en Español",
        "The Dinette Set",
        "Dinosaur Comics",
        "Dog Eat Doug",
        "Dogs of C-Kennel",
        "Domestic Abuse",
        "Don Brutus",
        "Doodle for Food",
        "Doodle Town",
        "Doonesbury",
        "The Doozies",
        "Drabble",
        "Dumbwich Castle",
        "The Duplex",
        "Edge City",
        "Eek!",
        "The Elderberries",
        "Emmy Lou",
        "Endtown",
        "Everyday People Cartoons",
        "Eyebeam",
        "Eyebeam Classic",
        "F Minus",
        "False Knees",
        "Family Tree",
        "Farcus",
        "Fat Cats",
        "Flo and Friends",
        "The Flying McCoys",
        "Foolish Mortals",
        "For Better or For Worse",
        "For Heaven's Sake",
        "Four Eyes",
        "Fowl Language",
        "FoxTrot",
        "FoxTrot Classics",
        "FoxTrot en Español",
        "Francis",
        "Frank and Ernest",
        "Frazz",
        "Fred Basset",
        "Fred Basset en Español",
        "Free Range",
        "Freshly Squeezed",
        "Frog Applause",
        "The Fusco Brothers",
        "Garfield",
        "Garfield Classics",
        "Garfield en Español",
        "Gasoline Alley",
        "Gaturro",
        "Geech",
        "Get a Life",
        "Get Fuzzy",
        "Gil",
        "Gil Thorp",
        "Ginger Meggs",
        "Ginger Meggs en Español",
        "Glasbergen Cartoons",
        "G-Man Webcomics",
        "Goats",
        "Al Goodwyn Editorial Cartoons",
        "Bob Gorrell",
        "Grand Avenue",
        "Gray Matters",
        "Green Humour",
        "The Grizzwells",
        "Haircut Practice",
        "Half Full",
        "Walt Handelsman",
        "Phil Hands",
        "Harley",
        "Heart of the City",
        "Heathcliff",
        "Heathcliff en Español",
        "Joe Heller",
        "Rebecca Hendin",
        "Herb and Jamaal",
        "Herman",
        "Home and Away",
        "Hot Comics for Cool People",
        "The Humble Stumble",
        "Hutch Owen",
        "Imagine This",
        "Imogen Quest",
        "In Security",
        "In the Bleachers",
        "In the Sticks",
        "Ink Pen",
        "Invisible Bread",
        "It's All About You",
        "Jake Likes Onions",
        "Jane's World",
        "Studio Jantze",
        "Jim Benton Cartoons",
        "Joey Alison Sayers Comics",
        "Clay Jones",
        "JumpStart",
        "Junk Drawer",
        "Justo y Franco",
        "Kevin Kallaugher",
        "The K Chronicles",
        "Steve Kelley",
        "Kevin Necessary Editorial Cartoons",
        "Kid Beowulf",
        "Kitchen Capers",
        "Kliban",
        "Kliban's Cats",
        "The Knight Life",
        "La Cucaracha",
        "La Cucaracha en Español",
        "Lard's World Peace Tips",
        "Last Kiss",
        "Laughing Redhead Comics",
        "Lay Lines",
        "Learn to Speak Cat",
        "Mike Lester",
        "Liberty Meadows",
        "Life on Earth",
        "Li'l Abner",
        "Lio",
        "Lio en Español",
        "Little Dog Lost",
        "Little Fried Chicken and Sushi",
        "Little Nemo",
        "Liz Climo Cartoons",
        "Lola",
        "Lola en Español",
        "Long Story Short",
        "Looks Good on Paper",
        "Loose Parts",
        "Los Osorios",
        "Lost Sheep",
        "Luann",
        "Luann Againn",
        "Luann en Español",
        "Mike Luckovich",
        "Lucky Cow",
        "Lug Nuts",
        "Lukey McGarry’s TLDR",
        "Lunarbaboon",
        "Maintaining",
        "Making It",
        "Mannequin on the Moon",
        "Maria's Day",
        "Gary Markstein",
        "Marmaduke",
        "The Martian Confederacy",
        "M2Bulls",
        "Brian McFadden",
        "The Meaning of Lila",
        "Medium Large",
        "Messycow Comics",
        "Mexikid Stories",
        "The Middle Age",
        "The Middletons",
        "Mike du Jour",
        "Miss Peach",
        "Mo",
        "Moderately Confused",
        "Momma",
        "Monty",
        "Monty Diaros",
        "Jim Morin",
        "Motley Classics",
        "Mr. Lowe",
        "Mt. Pleasant ",
        "Mutt & Jeff",
        "My Dad is Dracula",
        "MythTickle",
        "Nancy",
        "Nancy Classics",
        "Nate el Grande",
        "Nest Heads",
        "NEUROTICA",
        "New Adventures of Queen Victoria",
        "Next Door Neighbors",
        "Nick and Zuzu",
        "Non Sequitur",
        "The Norm Classics",
        "Not Invented Here",
        "Nothing is Not Something",
        "Now Recharging",
        "Off the Mark",
        "Oh, Brother!",
        "Jack Ohman",
        "Pat Oliphant",
        "Ollie and Quentin",
        "On A Claire Day",
        "One Big Happy",
        "Ordinary Bill",
        "Origins of the Sunday Comics",
        "The Other Coast",
        "Our Super Adventure",
        "Out of the Gene Pool Re-Runs",
        "Outland",
        "Over the Hedge",
        "Overboard",
        "Overboard en Español",
        "Ozy and Millie",
        "Henry Payne",
        "PC and Pixel",
        "Peanuts",
        "Peanuts Begins",
        "Snoopy en Español",
        "Pearls Before Swine",
        "Periquita",
        "Perlas para los Cerdos",
        "Perry Bible Fellowship",
        "Joel Pett",
        "Petunia & Dre",
        "Phoebe and Her Unicorn",
        "Pibgorn",
        "Pibgorn Sketches",
        "Pickles",
        "Please Listen to Me",
        "Pluggers",
        "Pooch Cafe",
        "Poorcraft",
        "Poorly Drawn Lines",
        "Pot-Shots",
        "PreTeena",
        "Prickly City",
        "A Problem Like Jamal",
        "Questionable Quotebook",
        "Rabbits Against Magic",
        "Raising Duncan",
        "Ted Rall",
        "Michael Ramirez",
        "Marshall Ramsey",
        "Randolph Itch, 2 a.m.",
        "Real Life Adventures",
        "Reality Check",
        "Red and Rover",
        "Red Meat",
        "Richard's Poor Almanac",
        "Rip Haywire",
        "Ripley’s ¡Aunque Usted no lo Crea!",
        "Ripley's Believe It or Not",
        "Robbie and Bobby",
        "Rob Rogers",
        "Rose is Rose",
        "Rosebuds",
        "Rosebuds en Español",
        "Rubes",
        "Rudy Park",
        "Salt n Pepper",
        "Sarah's Scribbles",
        "Saturday Morning Breakfast Cereal",
        "Savage Chickens",
        "Scary Gary",
        "Scenes from a Multiverse",
        "Shen Comix",
        "Drew Sheneman",
        "Shirley and Son Classics",
        "Shoe",
        "Sketchshark Comics",
        "Skin Horse",
        "Skippy",
        "Small Potatoes",
        "Snow Sez",
        "Snowflakes",
        "Jen Sorensen",
        "Speed Bump",
        "Spirit of the Staircase",
        "Spot the Frog",
        "Jeff Stahler",
        "Scott Stantis",
        "Sticky Comics",
        "Stone Soup",
        "Stone Soup Classics",
        "Las Hermanas Stone",
        "Strange Brew",
        "Dana Summers",
        "Sunny Street",
        "Sunshine State",
        "Super-Fun-Pak Comix",
        "Swan Eaters",
        "Sweet and Sour Pork",
        "Sylvia",
        "Today's Szep",
        "Tank McNamara",
        "Tarzan",
        "Tarzán en Español",
        "@Tavicat",
        "Ten Cats",
        "Texts From Mittens",
        "That is Priceless",
        "That New Carl Smell",
        "Thatababy",
        "Thin Lines",
        "(th)ink",
        "Tiny Sepuku",
        "Tom Toles",
        "Tom the Dancing Bug",
        "Too Much Coffee Man",
        "Trucutu",
        "Truth Facts",
        "Tutelandia",
        "Two Party Opera",
        "Underpants and Overbites",
        "Understanding Chaos",
        "Unstrange Phenomena",
        "The Upside Down World of Gustave Verbeek",
        "Gary Varvel",
        "ViewsAfrica",
        "ViewsAmerica",
        "ViewsAsia",
        "ViewsBusiness",
        "ViewsEurope",
        "ViewsLatinAmerica",
        "ViewsMidEast",
        "Views of the World",
        "Viivi & Wagner",
        "Wallace the Brave",
        "The Wandering Melon",
        "Warped",
        "Watch Your Head",
        "Wawawiwa",
        "WaynoVision",
        "Wee Pals",
        "Widdershins",
        "Wide Open",
        "Signe Wilkinson",
        "Win, Lose, Drew",
        "Wizard of Id",
        "The Wizard of Id - Spanish",
        "Wizard of Id Classics",
        "Wondermark",
        "Working Daze",
        "Working It Out",
        "The Worried Well",
        "Worry Lines",
        "Wrong Hands",
        "W.T. Duck",
        "Matt Wuerker",
        "WuMo",
        "Wumo en Español",
        "Yaffle",
        "Yes, I'm Hot in This",
        "Zack Hill",
        "Zen Pencils",
        "Ziggy",
        "Ziggy en Español",
        "9 to 5",
        "9 Chickweed Lane",
        "1 and Done",
        "9 Chickweed Lane Classics",
    ]
    return [app_commands.Choice(name=i[0], value=i[0]) for i in process.extract(current, choices, limit=25)]  # type: ignore



class GoComics(app_commands.Group):
    def __init__(self, *args, **kwargs):
        self.bot = kwargs.pop("bot")
        super().__init__(*args, **kwargs)

    @app_commands.command()
    @app_commands.describe(comicname="The name of the comic you want to see")
    @app_commands.autocomplete(comicname=comicname_autocomplete) # type: ignore
    async def today(self, interaction: discord.Interaction, comicname: str):
        today = datetime.date.today().strftime("%Y/%m/%d")
        comicname = comicname.replace(" ", "").casefold()
        async with self.bot.session.get(
            f"https://gocomics.com/{comicname}/{today}"
        ) as r:
            if r.status == 404:
                await interaction.response.send_message("Comic not found :(")
            else:
                await interaction.response.defer()
                data = await r.text()
                parser = bs4.BeautifulSoup(data, "html.parser")
                comic = parser.find("picture", class_="item-comic-image")
                embed = discord.Embed(title=comic.img["alt"], color=0x0000FF, url=f"https://gocomics.com/{comicname}/{today}")  # type: ignore
                embed.set_image(url=comic.img["src"])  # type: ignore
                await interaction.followup.send(embed=embed)

    @app_commands.command()
    @app_commands.describe(comicname="The name of the comic you want to see", date="Date of the comic you want to se")
    @app_commands.autocomplete(comicname=comicname_autocomplete) # type: ignore
    async def archive(self, interaction: discord.Interaction, comicname: str, date: app_commands.Transform[GoComicsDate, GoComicsDateTransformer] ):
        date_ = f"{date.year}/{date.month}/{date.day}"
        comicname = comicname.replace(" ", "").casefold()
        async with self.bot.session.get(
            f"https://gocomics.com/{comicname}/{date_}"
        ) as r:
            if r.status == 404:
                await interaction.response.send_message("Comic not found :(")
            else:
                await interaction.response.defer()
                data = await r.text()
                parser = bs4.BeautifulSoup(data, "html.parser")
                comic = parser.find("picture", class_="item-comic-image")
                embed = discord.Embed(title=comic.img["alt"], color=0x0000FF, url=f"https://gocomics.com/{comicname}/{date_}")  # type: ignore
                embed.set_image(url=comic.img["src"])  # type: ignore
                await interaction.followup.send(embed=embed)



    


async def setup(bot: commands.Bot):
    bot.tree.add_command(
        GoComics(bot=bot, description="Group for commands related to GoComics"),
        guild=discord.Object(id=842459680436781078),
    )
