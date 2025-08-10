from discord.ext import commands
from mongo import MongoDB
from config import config  # Make sure config is imported from your config module

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = MongoDB(config())
    
    @commands.command()
    async def verify(self, ctx, email: str):
        """Verify your student email"""
        # Add actual verification logic
        await self.db.participants.update_one(
            {'discord_id': str(ctx.author.id)},
            {'$set': {'email': email, 'verified': True}}
        )
        await ctx.send("Verification complete! You now have full access.")

async def setup(bot):
    await bot.add_cog(Verification(bot))