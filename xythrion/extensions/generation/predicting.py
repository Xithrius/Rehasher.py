from typing import Union

from discord.ext.commands import Cog, Context, command

from xythrion.bot import Xythrion
from xythrion.utils import DefaultEmbed


class Predicting(Cog):
    """Predicting the future from data sets and models."""

    def __init__(self, bot: Xythrion) -> None:
        self.bot = bot

    @command(name='trump_tweet', aliases=('predict_trump', 'ttwitter',))
    async def predict_trump_tweet_stats(self, ctx: Context, tweet: Union[str, int]) -> None:
        """Attempts to predict the amount of retweets and likes on a tweet."""
        async with ctx.typing():
            retweets, likes = await self.bot.loop.run_in_executor(None, self.bot.model.run_model, tweet)

        embed = DefaultEmbed(description=f'Prediction: this tweet has {retweets} retweets and {likes} likes.')

        await ctx.send(embed=embed)
