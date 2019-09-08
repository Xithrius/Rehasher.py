"""
>> Xythrion
> Copyright (c) 2019 Xithrius
> MIT license, Refer to LICENSE for more info


This is the main Python file for the discord.py bot, as all important attributes,
checks, and background tasks are created here.

Example:
    First time usage (do it every so often to keep updated packages):
        $ py -3 -m pip install --user -r requirements.txt
    To run the bot:
        $ py -3 bot.py

Todo:
    * Literally rewrite the repository

"""


import collections
import json
import asyncio
import aiohttp

from discord.ext import commands as comms

from modules.output import path, ds, get_extensions


class Robot(comms.Bot):
    """Creating connections, attributes, and background tasks.
    
    Preface: When ctx is args, it gives context on where the method was called, such as channel, member, and guild.
    
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #: Opening the config json file
        with open(path('config', 'config.json'), 'r', encoding='utf8') as f:
            config = json.load(f)

        #: Giving self.config recursive attributes from config.json
        self.config = json.loads(json.dumps(config), object_hook=lambda d: collections.namedtuple('config', d.keys())(*d.values()))

        #: Create async loop
        self.loop = asyncio.get_event_loop()

        future = asyncio.gather()
        
        #: Create tasks
        self.loop.create_task(self.create_tasks())
        self.loop.run_until_complete(future)

        # self.request_limiter = asyncio.new_event_loop()

        ds.s('Got here too.')

    """ Bot-specific functions """

    async def load_extensions(self):
        ds.w('Loading extensions...')
        broken_extensions = []
        for extension in get_extensions(self.config.blocked_extensions):
            try:
                self.unload_extension(extension)
                self.load_extension(extension)
            except Exception as e:
                broken_extensions.append(f'{type(e).__name__}: {e}')
        extension_status = await self.load_extensions()
        if extension_status:
            for extension in extension_status:
                ds.w(extension_status)

    """ Tasks """

    async def create_tasks(self):
        self.s = aiohttp.ClientSession()
        ds.r('Connections established.')

        self.connection_loop = asyncio.get_running_loop()
        self.connection_loop.create_task(self.test_services())
        result = await self.connection_loop.run_in_executor(None, self.test_services)

    async def test_services(self):
        """ """
        while not self.is_closed():
            await asyncio.sleep(60)
            print('test_services')

    """ Events """

    async def on_ready(self):
        ds.r('Startup completed.')

    async def close(self):
        """ Safely closes connections """
        try:
            await self.s.close()
            self.c.close()
        except Exception as e:
            pass
        await super().close()


class RobotCog(comms.Cog):
    """Essential commands for using the bot."""

    def __init__(self, bot):
        #: Robot(comms.Bot) as a class attribute
        self.bot = bot

    @comms.command(alias=['reload', 'refresh', 'r'])
    async def reload(self, ctx):
        extension_status = await self.load_extensions()
        if extension_status:
            for extension in extension_status:
                ds.w(extension)
        else:
            ds.s('Reloaded all cogs.')

    @comms.command(alias=['disconnect', 'dc', 'exit'])
    async def exit(self, ctx):
        """Logs out the bot.

        Returns:
            A possible timeout error.

        """
        ds.w('Logging out...')
        await ctx.bot.logout()


class InfoCog(comms.Cog):
    """Cog is meant to give information about owner and bot interactions."""

    def __init__(self, bot):
        #: Robot(comms.Bot) as a class attribute
        self.bot = bot

    @comms.command()
    async def invite(self, ctx):
        """Gives the invite link of this bot. It is not 'essential', but it's still useful.
        
        Returns:
            The invite link so the bot can be invited to a server.
        
        """
        await ctx.send(f'https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=32885952')

    @comms.command()
    async def about(self, ctx):
        """Returns information about this bot's origin
        
        Returns:
            An embed object with links to creator's information and bot's repository.
        
        """
        info = {
            'Twitter': 'https://twitter.com/_Xithrius',
            'Github': 'https://github.com/Xithrius/Xythrion'
        }
        embed = discord.Embed(title='Project creation date: March 30, 2019', description='\n'.join(f'[`{k}`]({v})' for k, v in info.items()), colour=self.bot.ec)
        await ctx.send(embed=embed)

    @comms.command()
    async def website(self, ctx):
        """Returns website for the bot (this replaced the README).
        
        Returns:
            An embed object containing the website link for the bot.
        
        """
        embed = discord.Embed(description='`https://xithrius.github.io/Xythrion/`')
        await ctx.send(embed=embed)


if __name__ == "__main__":
    bot = Robot(command_prefix=comms.when_mentioned_or('.'))
    bot.add_cog(RobotCog(bot))
    bot.add_cog(InfoCog(bot))
    bot.run(bot.config.discord, bot=True, reconnect=True)
