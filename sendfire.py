"""
fire.py

Simple Discord bot script (or lightweight bot module) that demonstrates
assigning a role to new human members who join a specific guild. The
target guild is read from `CUSTOM_GUILD_ID` in the project's `.env` file.

Edit the configuration section below to set your role by ID or name
and ensure your bot token and intents are configured in the environment.

Notes:
- This uses discord.py and python-dotenv. Ensure the Members intent is
  enabled in the Discord developer portal for your bot.
"""

import os
import logging
from dotenv import load_dotenv
import discord
from discord.ext import commands

# ---------------------------
# Configuration (edit here)
# ---------------------------
load_dotenv()  # loads variables from .env in repo root

# The guild ID is read from .env as CUSTOM_GUILD_ID. Example in .env:
# CUSTOM_GUILD_ID=1411496830243573933
CUSTOM_GUILD_ID = 1411496830243573933
if os.getenv("CUSTOM_GUILD_ID"):
	try:
		CUSTOM_GUILD_ID = int(os.getenv("CUSTOM_GUILD_ID"))
	except ValueError:
		CUSTOM_GUILD_ID = None

# Choose one of the two approaches below to identify the role(s) you want
# to grant. Preferred: provide numeric role IDs in ROLE_IDS. You can also
# provide role names in ROLE_NAMES as a fallback or in addition.
# Examples:
# ROLE_IDS = [987654321012345678, 123456789012345678]
# ROLE_NAMES = ["Player", "Member"]
ROLE_IDS = [1411711276173758494, 1411685303726641162]            # list of ints; preferred when available
ROLE_NAMES = ["Player"] # list of exact role name strings

# Token selection: prefer development token, then production. You can
# also set BOT_TOKEN directly in the environment if you prefer.
BOT_TOKEN = os.getenv("DEVELOPMENT_BOT_TOKEN") or os.getenv("PRODUCTION_BOT_TOKEN") or os.getenv("BOT_TOKEN")


# ---------------------------
# Bot setup
# ---------------------------
intents = discord.Intents.default()
intents.members = True  # required to receive member join events

bot = commands.Bot(command_prefix="!", intents=intents)


# ---------------------------
# Events
# ---------------------------
@bot.event
async def on_ready():
	logging.info(f"Bot ready: {bot.user} (id={bot.user.id})")


@bot.event
async def on_member_join(member: discord.Member):
	"""Assign a configured role when a human (non-bot) member joins the
	configured guild.

	Behavior contract:
	- Input: a discord.Member object provided by discord.py when someone joins.
	- Output: attempts to add the configured role to the member if all checks pass.
	- Error modes: logs and returns if config is missing, role not found, or
	  permission errors occur.
	"""

	# 1) Ensure the CUSTOM_GUILD_ID is set and matches this join event
	if CUSTOM_GUILD_ID is None:
		logging.warning("CUSTOM_GUILD_ID not set in environment; skipping role assignment.")
		return
	if member.guild.id != CUSTOM_GUILD_ID:
		# Not the configured server; ignore
		return

	# 2) Ignore bots
	if member.bot:
		logging.info(f"Ignored bot account joining: {member}")
		return

	# 3) Resolve multiple roles by ID and by name
	roles_to_assign = []
	# by ID
	for rid in ROLE_IDS:
		try:
			rid_int = int(rid)
		except Exception:
			logging.warning(f"Invalid role id in ROLE_IDS: {rid!r}; skipping")
			continue
		r = member.guild.get_role(rid_int)
		if r:
			roles_to_assign.append(r)

	# by name (avoid duplicates)
	for name in ROLE_NAMES:
		if not name:
			continue
		r = discord.utils.get(member.guild.roles, name=name)
		if r and r not in roles_to_assign:
			roles_to_assign.append(r)

	if not roles_to_assign:
		logging.warning(f"No roles found for ROLE_IDS={ROLE_IDS} ROLE_NAMES={ROLE_NAMES}; cannot assign to {member}.")
		return

	# 4) Attempt to add all roles at once
	try:
		await member.add_roles(*roles_to_assign, reason="Automatic role assignment on join")
		logging.info(f"Assigned roles {[r.name for r in roles_to_assign]} to member {member} in guild {member.guild.id}.")
	except Exception as exc:
		logging.exception(f"Failed to assign roles '{roles_to_assign}' to {member}: {exc}")


# ---------------------------
# Commands (placeholder)
# ---------------------------
# Add bot command handlers here. Example:
# @bot.command(name='ping')
# async def ping(ctx):
#     await ctx.send('pong')


# ---------------------------
# Utilities & helpers (placeholder)
# ---------------------------
# Add any helper functions below.

def run2():
    try:
        bot.run(BOT_TOKEN)
    except Exception as e:
        # Sentry removed: log to terminal and re-raise
        logging.exception("Unhandled exception while running the bot")
        raise

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

	if not BOT_TOKEN:
		logging.error("No bot token found. Set DEVELOPMENT_BOT_TOKEN or PRODUCTION_BOT_TOKEN or BOT_TOKEN in the environment.")
	else:
		# Important: ensure the Members intent is enabled for your bot in the
		# Discord developer portal and the bot has permissions to manage roles
		# in the target guild. Run this file directly to start the bot process.
		bot.run(BOT_TOKEN)