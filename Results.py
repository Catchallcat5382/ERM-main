import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# Load .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
RESULTS_CHANNEL_ID = int(os.getenv("RESULTS_CHANNEL_ID", 0))  # Channel for results
GUILD_ID = int(os.getenv("GUILD_ID", 0))  # Guild ID for slash commands

# Bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="-", intents=intents)

# Function to build embed
def make_embed(user: discord.User, result: str, reason: str, color: discord.Color, divider_color: str):
    embed = discord.Embed(
        title=f"Application {result}",
        description=f"{user.mention}'s application has been **{result}**.\n\n"
                    f"{divider_color}\n\n"
                    f"**Reason:** {reason}",
        color=color
    )
    return embed

# ---------------- SLASH COMMANDS ----------------

@bot.tree.command(name="accept", description="Accept an application")
@app_commands.describe(
    user="User to accept",
    reason="Reason for acceptance"
)
async def accept(interaction: discord.Interaction, user: discord.User, reason: str):
    embed = make_embed(
        user=user,
        result="Passed",
        reason=reason,
        color=discord.Color.green(),
        divider_color="━━━━━━━━━━━━━━━━━━━━━"  # ✅ green-ish divider
    )

    channel = interaction.guild.get_channel(RESULTS_CHANNEL_ID)
    if not channel:
        await interaction.response.send_message("⚠️ Results channel not found. Check `.env`.", ephemeral=True)
        return

    await channel.send(content=f"{user.mention}", embed=embed)
    await interaction.response.send_message(f"✅ Application accepted for {user.mention}", ephemeral=True)


@bot.tree.command(name="deny", description="Deny an application")
@app_commands.describe(
    user="User to deny",
    reason="Reason for denial"
)
async def deny(interaction: discord.Interaction, user: discord.User, reason: str):
    embed = make_embed(
        user=user,
        result="Failed",
        reason=reason,
        color=discord.Color.red(),
        divider_color="━━━━━━━━━━━━━━━━━━━━━"  # ✅ red-ish divider
    )

    channel = interaction.guild.get_channel(RESULTS_CHANNEL_ID)
    if not channel:
        await interaction.response.send_message("⚠️ Results channel not found. Check `.env`.", ephemeral=True)
        return

    await channel.send(content=f"{user.mention}", embed=embed)
    await interaction.response.send_message(f"❌ Application denied for {user.mention}", ephemeral=True)

# ---------------- PREFIX COMMANDS ----------------

@bot.command(name="accept")
async def accept_prefix(ctx, user: discord.Member, *, reason: str):
    """Usage: -accept @user <reason>"""
    embed = make_embed(
        user=user,
        result="Passed",
        reason=reason,
        color=discord.Color.green(),
        divider_color="━━━━━━━━━━━━━━━━━━━━━"
    )
    channel = ctx.guild.get_channel(RESULTS_CHANNEL_ID)
    if not channel:
        await ctx.send("⚠️ Results channel not found. Check `.env`.")
        return
    await channel.send(content=f"{user.mention}", embed=embed)
    await ctx.send(f"✅ Application accepted for {user.mention}")


@bot.command(name="deny")
async def deny_prefix(ctx, user: discord.Member, *, reason: str):
    """Usage: -deny @user <reason>"""
    embed = make_embed(
        user=user,
        result="Failed",
        reason=reason,
        color=discord.Color.red(),
        divider_color="━━━━━━━━━━━━━━━━━━━━━"
    )
    channel = ctx.guild.get_channel(RESULTS_CHANNEL_ID)
    if not channel:
        await ctx.send("⚠️ Results channel not found. Check `.env`.")
        return
    await channel.send(content=f"{user.mention}", embed=embed)
    await ctx.send(f"❌ Application denied for {user.mention}")

# ---------------- READY EVENT ----------------

@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=guild)  # ✅ Sync commands only to this guild
    print(f"✅ Logged in as {bot.user} | Slash commands synced to guild {GUILD_ID}")

bot.run(TOKEN)
