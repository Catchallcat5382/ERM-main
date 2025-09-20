# bot_template.py
import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import logging

# -------------------------
# Load .env variables
# -------------------------
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
RESULTS_CHANNEL_ID = int(os.getenv("RESULTS_CHANNEL"))
EMBED_IMAGE_URL = os.getenv("EMBED_IMAGE_URL")  # Image shown in the embed

# -------------------------
# Channel mentions for accept instructions
# -------------------------
GROUP_ACCESS_CHANNEL = "<#1418994380114755604>"  # Replace with your group-access channel ID
MOD_HANDBOOK_CHANNEL = "<#1412902953571844136>"  # Replace with your mod-handbook channel ID

# -------------------------
# Bot setup
# -------------------------
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)  # Prefix placeholder only
tree = bot.tree

@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    tree.copy_global_to(guild=guild)
    await tree.sync(guild=guild)
    print(f"Bot is ready! Slash commands synced to guild {GUILD_ID}")

# -------------------------
# Shared helper function
# -------------------------
async def send_application_result(
    target_user: discord.Member,
    staff_mention: str,
    reason: str,
    accepted: bool,
):
    """Sends the accept/deny message to the results channel with embed and user mention outside."""
    channel = bot.get_channel(RESULTS_CHANNEL_ID)
    if not channel:
        print(f"❌ Could not find channel with ID {RESULTS_CHANNEL_ID}")
        return

    color = discord.Color.green() if accepted else discord.Color.red()
    status_text = "Accepted" if accepted else "Denied"

    # Embed
    embed = discord.Embed(
        title=target_user.name,
        description=f"Your application was {status_text.lower()} by:\n{staff_mention}",
        color=color,
    )
    embed.add_field(name="Reason:", value=reason, inline=False)

    if accepted:
        # Extra instructions for accepted users
        instructions = (
            f"To get started, submit a Group-Request in {GROUP_ACCESS_CHANNEL}\n"
            f"Additionally: Read {MOD_HANDBOOK_CHANNEL}\n\n"
            f"Reminder that you are NOT allowed on duty until you got trained!"
        )
        embed.add_field(name="Instructions:", value=instructions, inline=False)
        embed.add_field(name=status_text, value="\u200b", inline=False)
        embed.set_footer(text="Good application!")
    else:
        embed.add_field(name=status_text, value="\u200b", inline=False)
        embed.set_footer(text="You may reapply after the cooldown has run out.")

    # Add profile picture of target user in top right
    embed.set_thumbnail(url=target_user.display_avatar.url)
    # Set the main image
    embed.set_image(url=EMBED_IMAGE_URL)

    # Send the user mention outside the embed
    await channel.send(f"{target_user.mention}", embed=embed)

# -------------------------
# ACCEPT COMMAND
# -------------------------
@tree.command(name="accept", description="Accept a user's application request")
@app_commands.describe(user="User to accept", reason="Reason for acceptance")
async def accept_slash(interaction: discord.Interaction, user: discord.Member, reason: str):
    await send_application_result(user, interaction.user.mention, reason, accepted=True)
    # No response to the user
    # await interaction.response.send_message(...) removed

# -------------------------
# DENY COMMAND
# -------------------------
@tree.command(name="deny", description="Deny a user's application request")
@app_commands.describe(user="User to deny", reason="Reason for denial")
async def deny_slash(interaction: discord.Interaction, user: discord.Member, reason: str):
    await send_application_result(user, interaction.user.mention, reason, accepted=False)
    # No response to the user

# -------------------------
# Run Bot
# -------------------------
bot.run(TOKEN)


def run2():
    try:
        bot.run(TOKEN)
    except Exception as e:
        # Sentry removed: log to terminal and re-raise
        logging.exception("Unhandled exception while running the bot")
        raise

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

	if not TOKEN:
		logging.error("No bot token found. Set DEVELOPMENT_BOT_TOKEN or PRODUCTION_BOT_TOKEN or BOT_TOKEN in the environment.")
	else:
		# Important: ensure the Members intent is enabled for your bot in the
		# Discord developer portal and the bot has permissions to manage roles
		# in the target guild. Run this file directly to start the bot process.
		bot.run(TOKEN)