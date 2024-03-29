# senddiscord

`senddiscord` is a CLI tool to send things from your terminal to Discord.


## Usage

Example: Post the output of a command along with an attached file.
```sh
fortune | senddiscord 123456789123456789 --attach cat.jpg
```

For up-to-date usage instructions:
```sh
senddiscord -h
```


## Setup

### Installation

1. Install the Python dependencies listed in [requirements.txt].
2. Install/symlink `senddiscord.py` as `senddiscord` somewhere on your `PATH`.
3. [Create a Discord bot](https://discordpy.readthedocs.io/en/stable/discord.html)
4. [Configure](#configuration) `senddiscord` to use your bot's auth token.


## Configuration

Configurations are read from `~/.config/senddiscord.yaml` (unless you've
set `XDG_CONFIG_HOME` to point elsewhere).

### Token

Your auth token can be configured using the `token` configuration key.

Example:
```yaml
token: qfRhyfLk5olJHPsVaRGIVGGs.N7MdDP.v8O7BVuyGVtrhrnwjY5W3S-pn4C
```

You are recommended to limit the file permissions such that other users cannot
access your token. Example: `chmod 600 ~/.config/senddiscord.yaml`.

Alternatively, you can set the token with the `--token` option or with an
environment variable named `DISCORD_TOKEN`. Beware of the security implications
of passing secrets on the command-line.

### Channel aliases

You may configure mnemonic channel aliases to use in place of channel IDs.

Example:
```yaml
channel_aliases:
  general: 123456789123456789
  foobar: 987654321987654321
```
