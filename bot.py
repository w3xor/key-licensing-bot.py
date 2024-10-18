# updates coming soon for more commands.
# made by @3298x on discord
# https://discord.gg/WqJ2jdBYnr
import discord
from discord import app_commands
import requests

# Configuration
DISCORD_TOKEN = '' # add in your discord bot token
CRYPTOLENS_ACCESS_TOKEN = ''  # add in your cryptolens api token
PRODUCT_ID = '' # cryptolens product id
ROLE_ID = 123456 # replace with allowed role id  

# Create bot instance
intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    await tree.sync()
    print(f'Logged in as {bot.user}')

@tree.command(name="createkey", description="Create a new license key.")
@app_commands.describe(period="period in days", max_no_of_machines="hwid lock 1=yes 0=no", no_of_keys="Number of keys")
async def create_key(interaction: discord.Interaction, period: int, max_no_of_machines: int, no_of_keys: int):
    # Check if the user has the required role
    if ROLE_ID not in [role.id for role in interaction.user.roles]:
        await interaction.response.send_message("dont got perms fn", ephemeral=True)
        return

    # Make the API request to create a key
    url = f"https://api.cryptolens.io/api/key/CreateKey?token={CRYPTOLENS_ACCESS_TOKEN}&ProductId={PRODUCT_ID}&Period={period}&MaxNoOfMachines={max_no_of_machines}&NoOfKeys={no_of_keys}"
    
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        keys = data.get('keys', [])
        if keys:
            key_list = "\n".join([key['key'] for key in keys])
            await interaction.response.send_message(f"Generated Key(s):\n{key_list}")
        else:
            await interaction.response.send_message("api being weird but key was generated")
    else:
        await interaction.response.send_message(f"Error: {response.text}")

# Run the bot
bot.run(DISCORD_TOKEN)
