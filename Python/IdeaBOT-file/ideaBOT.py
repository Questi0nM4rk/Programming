#! /usr/bin/python

import random
import logging
import json
# Discord
import discord
from discord import app_commands
# dotenv
from dotenv import load_dotenv
from os import getenv

# Change this your chosed file, that will hold all the ideas and info... note that the file does not have to be created prio to running this bot
FILENAME = ""

# -------------------------DOTENV stuff-------------------------
load_dotenv()
TOKEN = getenv("DISCORD_TOKEN")
GUILD_ID = getenv("GUILD_ID")
# Add the guild ids in which the slash command will appear.
# If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.

# -------------------------Discord bot stuff-------------------------
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# -------------------------file stuff-------------------------
"""
json format:
    [
        {},
        {
            "name": "name",
            "subject": "subject",
            "creator": "creator",
            "difficulty": "difficulty",
            "description": "description",
            "project": ""
        },
        {}
    ]
"""


async def file_init():
    with open(FILENAME, "w") as f:
        pass

    
async def append_to_file(content: dict) -> None:
    Ljson = []
    with open(FILENAME, "r") as f:
        Ljson = json.load(f)
    
    Ljson.append(content)
    
    with open(FILENAME, "w") as f:
        json.dump(Ljson, f, indent=4)


async def update_file(indx: str, get: str, content: dict) -> None:
    data = []
    with open(FILENAME, "r") as f:
        data = json.load(f)
        for i in range(len(data)):
            if data[i][indx] == get:
                data[i] = content
    
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)
        

async def update_one(indx: str, get: str, what: str, to: str) -> None:
    data = []
    with open(FILENAME, "r") as f:
        data = json.load(f)
        for i in range(len(data)):
            if data[i][indx] == get:
                data[i][what] = to
    
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)
        

async def del_from_file(indx: str, get: str) -> None:
    data = []
    with open(FILENAME, "r") as f:
        data = json.load(f)
        for i in range(len(data)):
            if data[i][indx] == get:
                del data[i]
    
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)


async def get_from_file(indx: str, get: str) -> list:
    ret = []
    with open(FILENAME, "r") as f:
        data = json.load(f)
        for d in data:
            if d[indx] == get:
                ret.append(d)
    return ret

async def get_everything() -> None:
    ret = []
    with open(FILENAME, "r") as f:
        data = json.load(f)
        for d in data:
            ret.append(d)
    return ret
  

# -------------------------ON READY-------------------------
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    
    try:
        f = open(FILENAME, "r")
    except:
        file_init()
    
    logging.info("READY!") # LOG


# ===================================IDEAS===================================
# -------------------------ADD-------------------------
@tree.command(name="add", description="Create an idea", guild=discord.Object(id=GUILD_ID))
async def add_cmd(interaction, name: str, subject: str, difficulty: int, description: str):
    creator = interaction.user.name

    logging.info(f"Creating idea `{name}` with values: `subject={subject}, difficulty={difficulty}, description={description}`") # LOG

    name = name.lower()
    result = await get_from_file("name", name.lower)

    if len(result) == 0:
        di = {
            "name": name,
            "subject": subject,
            "creator": creator,
            "difficulty": difficulty,
            "description": description,
            "project": ""
        }
        await append_to_file(di)

        await interaction.response.send_message(f"Created a new idea `{name}`")
    else:
        await interaction.response.send_message(f"Your idea `{result[0]['name']}` already exists and was created by **{result[0]['creator']}**")


# -------------------------EDIT-------------------------
@tree.command(name="edit", description="Edit an idea", guild=discord.Object(id=GUILD_ID))
@app_commands.autocomplete(name=name_autocomplete)
async def edit_cmd(interaction, name: str, rename: str = None, subject: str = None, difficulty: str = None, description: str = None):
    name = name.lower()
    vars = ""
    if rename is not None:
        vars += f"name='{rename}', "
    if subject is not None:
        vars += f"subject='{subject}', "
    if difficulty is not None:
        vars += f"difficulty={difficulty}, "
    if description is not None:
        vars += f"description='{description}', "

    logging.info(f"Editing idea `{name}` to `{vars[:-2]}`") # LOG

    if vars != '':
        await update_file("name", name, vars[:-2])

    await interaction.response.send_message(f"Edited `{name}`")


# -------------------------DELETE-------------------------
@tree.command(name="del", description="Delete an idea", guild=discord.Object(id=GUILD_ID))
@app_commands.autocomplete(name=name_autocomplete)
async def delete_cmd(interaction, name: str):
    logging.info(f"Deleting idea `{name}`") # LOG
    name = name.lower()
    chan = await get_from_file("name", name)
    channel = client.get_channel(chan[0]["project"])
    if channel is not None: await channel.delete()

    await del_from_file("name", name)

    await interaction.response.send_message(f"Deleted `{name}`")


# -------------------------SHOW-------------------------
@tree.command(name="show", description="Show a specific idea", guild=discord.Object(id=GUILD_ID))
@app_commands.autocomplete(name=name_autocomplete)
async def show_cmd(interaction, name: str):
    logging.info(f"Showing idea `{name}`") # LOG
    name = name.lower()
    result = await get_from_file("name", name)
    result = result[0]
    msg = (f"**Showing idea** `{name}`"
        f"\n**Subject:** `{result['subject']}`"
        f"\n**Creator:** `{result['creator']}`"
        f"\n**Difficulty:** `{result['difficulty']}`"
        f"\n**Description:** `{result['description']}`")
    await interaction.response.send_message(msg)


# -------------------------LIST-------------------------
@tree.command(name="list", description="List all ideas", guild=discord.Object(id=GUILD_ID))
async def list_cmd(interaction):
    logging.info(f"Listing all ideas") # LOG
    result = await get_everything()
    msg = "**A list of ideas:**\n"
    await interaction.response.send_message(msg + f"```\n{table(result)}```")


# ===================================PROJECTS===================================
# -------------------------RANDOM-------------------------
@tree.command(name="random", description="Pick a random project", guild=discord.Object(id=GUILD_ID))
async def random_cmd(interaction, difficulty: int = None):
    logging.info(f"Picking random project") # LOG
    if difficulty is None:
        result = await get_everything()
    else:
        result = await get_from_file("difficulty", difficulty)
    
    if result != []:
        rnm = random.randint(1, len(result))-1
        await interaction.response.send_message(f"```\n{table([result[rnm]])}```")
    else:
        await interaction.response.send_message("**Project with this difficulty doesn't exist**")


# -------------------------CREATE PROJECT-------------------------
@tree.command(name="create_project", description="Creates a project from an idea", guild=discord.Object(id=GUILD_ID))
@app_commands.autocomplete(name=name_autocomplete)
async def create_project(interaction, name: str):
    g = interaction.guild
    name = name.lower()
    result = await get_from_file("name", name)
    ids = result[0]['name']
    if result[0]['project'] is None:
        logging.info(f"Creating project from `{name}` in channel `{str(ids)}`") # LOG
        category = discord.utils.get(g.categories, name=CATEGORY_NAME)
        channel = await g.create_text_channel(name=ids, category=category)
        
        await update_one("name", name, "project", channel.id)

        await interaction.response.send_message(
            "The idea **" + str(ids) + "** was turned into a project and channel was created in **" + CATEGORY_NAME + "**")
        description = result[0]["description"]
        await channel.send("**The description:**\n" + f"```{description}```\n=============================================")
    else:
        await interaction.response.send_message(f"`{result[0]['name']}` is already a project")


client.run(TOKEN)

