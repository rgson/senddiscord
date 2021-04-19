#!/usr/bin/python3

import argparse
import os
import sys

import discord


parser = argparse.ArgumentParser(
    description="Send things from your terminal to Discord"
)
parser.add_argument("channel", type=int, help="the output channel's ID")
parser.add_argument("--token", help="sets the Discord auth token")
args = parser.parse_args()


token = args.token or os.environ.get("DISCORD_TOKEN")
if not token:
    print(
        "Missing Discord auth token.\n"
        "Use the --token option or set the DISCORD_TOKEN environment variable.",
        file=sys.stderr,
    )
    sys.exit(1)


client = discord.Client()


@client.event
async def on_ready():
    channel = client.get_channel(args.channel)
    await channel.send(sys.stdin.read())
    await client.close()


client.run(token)
