"""
> Xythrion: Graphing manipulated data through Discord.py.

Copyright (c) 2020 Xithrius.
MIT license, Refer to LICENSE for more info.
"""


from xythrion.bot import Xythrion
from xythrion.extensions.administration.development import Development
from xythrion.extensions.administration.warnings import Warnings


def setup(bot: Xythrion) -> None:
    """The necessary function for loading in extensions within this folder."""
    bot.add_cog(Development(bot))
    bot.add_cog(Warnings(bot))
