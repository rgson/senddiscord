#!/usr/bin/python3

import argparse
import os
import sys

import discord
import yaml


SCRIPT_NAME = "senddiscord"

CONFIG_DIR = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
CONFIG_FILE = f"{CONFIG_DIR}/{SCRIPT_NAME}.yaml"

# Read configurations
try:
    with open(CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    config = {}

# Read command-line arguments
parser = argparse.ArgumentParser(
    description="Send things from your terminal to Discord"
)
parser.add_argument("channel", type=int, help="the output channel's ID")
parser.add_argument("--token", help="sets the Discord auth token")
args = parser.parse_args()

# Identify the token
token = args.token or os.environ.get("DISCORD_TOKEN") or config.get("token")
if not token:
    print(
        "Missing Discord auth token.\n"
        f'Set it with the "--token" option, a "DISCORD_TOKEN" environment variable, or a "token" configuration option in {CONFIG_FILE}.',
        file=sys.stderr,
    )
    sys.exit(1)

# Configure the Discord client
client = discord.Client()

# Mentions are not properly supported. Avoid unintentional mentions.
client.allowed_mentions = discord.AllowedMentions(
    everyone=False, users=False, roles=False
)


@client.event
async def on_ready():
    channel = client.get_channel(args.channel)
    await channel.send(sys.stdin.read())
    await client.close()


client.run(token)
