#!/usr/bin/python3

import argparse
import os
import sys

import discord
import yaml


SCRIPT_NAME = "senddiscord"

MAX_ATTACHMENTS = 10  # External limitation

CONFIG_DIR = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
CONFIG_FILE = f"{CONFIG_DIR}/{SCRIPT_NAME}.yaml"

# Read configurations
try:
    with open(CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    config = {}

channel_aliases = config.get("channel_aliases", {})

# Read command-line arguments
def channel(value):
    return channel_aliases.get(value) or int(value)


parser = argparse.ArgumentParser(
    description="Send things from your terminal to Discord"
)
parser.add_argument(
    "channel", type=channel, help="the output channel (ID or alias)"
)
parser.add_argument("--token", help="sets the Discord auth token")
parser.add_argument(
    "--attach",
    help="attaches a file to the message (repeatable)",
    action="append",
    default=[],
)
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

# Check attachments
if len(args.attach) > MAX_ATTACHMENTS:
    print(
        f"Too many attachments. Cannot send more than {MAX_ATTACHMENTS}.",
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
    await channel.send(
        content=sys.stdin.read(),
        files=[discord.File(file) for file in args.attach],
    )
    await client.close()


client.run(token)
