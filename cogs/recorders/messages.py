"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info
"""


import asyncpg
from collections import defaultdict
import json

from discord.ext import commands as comms
import discord

from modules.output import path


class Message_Recorder(comms.Cog):
    """Fetching map information from Google."""

    def __init__(self, bot):

        #: Setting Robot(comms.Bot) as a class attribute
        self.bot = bot

    """ Commands """

    @comms.command(enabled=False, hidden=True)
    @comms.is_owner()
    async def rl(self, ctx):
        """ONLY USE THIS COMMAND IF DATABASE IS DELETED."""
        self.messages = []
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                try:
                    messages = await channel.history(limit=None).flatten()
                    self.messages.extend(messages)
                except discord.errors.Forbidden:
                    pass
        self.user_records = {}
        for message in self.messages:
            if message.author.id not in self.user_records.keys():
                self.user_records[message.author.id] = [0, 0, 0, 0]
            y = self.user_records[message.author.id]
            if message.attachments:
                for f in message.attachments:
                    f = f.filename[-4:]
                    if f in ['.jpg', '.png']:
                        y[1] += 1
                    elif f in ['.gif', '.mp4']:
                        y[2] += 1
                    elif f in ['.mp3', '.flv']:
                        y[3] += 1
            else:
                y[0] += 1
            self.user_records[message.author.id] = y
        for user_id, records in self.user_records.items():
            await self.bot.conn.execute('''INSERT INTO Messages(identification, messages, images, videos, audios) VALUES($1, $2, $3, $4, $5)''', user_id, *records)


def setup(bot):
    bot.add_cog(Message_Recorder(bot))