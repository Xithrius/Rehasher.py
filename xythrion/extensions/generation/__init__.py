from xythrion.bot import Xythrion
from xythrion.extensions.generation.graphing import Graphing
from xythrion.extensions.generation.predicting import Predicting
from xythrion.extensions.generation.qrcode import QRCode
from xythrion.extensions.generation.randoms import Randoms


def setup(bot: Xythrion) -> None:
    """The necessary function for loading in cogs within this folder."""
    bot.add_cog(Graphing(bot))
    bot.add_cog(Predicting(bot))
    bot.add_cog(QRCode(bot))
    bot.add_cog(Randoms(bot))
