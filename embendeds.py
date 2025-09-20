import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load token and guild id from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Sync slash commands on startup
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"✅ Synced {len(synced)} commands to guild {GUILD_ID}")
    except Exception as e:
        print(f"❌ Error syncing: {e}")

# Slash command for embed creation/editing
@bot.tree.command(name="embed", description="Send or edit an embed", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(
    channel_id="Channel ID where the embed goes",
    title="Title of the embed",
    description="Main text of the embed",
    color="Color in hex (example: #ff0000)",
    footer="Footer text",
    image_url="Image URL (optional)",
    image_position="top or bottom placement"
)
async def embed_command(
    interaction: discord.Interaction,
    channel_id: str,
    title: str,
    description: str,
    color: str,
    footer: str = None,
    image_url: str = None,
    image_position: str = "bottom"
):
    try:
        # Convert hex to int for color
        embed_color = int(color.replace("#", ""), 16)

        embed = discord.Embed(
            title=title,
            description=description,
            color=embed_color
        )

        if footer:
            embed.set_footer(text=footer)

        if image_url:
            if image_position.lower() == "top":
                embed.set_thumbnail(url=image_url)
            else:
                embed.set_image(url=image_url)

        channel = bot.get_channel(int(channel_id))
        if not channel:
            await interaction.response.send_message("❌ Invalid channel ID", ephemeral=True)
            return

        await channel.send(embed=embed)
        await interaction.response.send_message("✅ Embed sent successfully!", ephemeral=True)

    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


bot.run(TOKEN)