import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = discord.utils.get(member.guild.text_channels, name='welcome')
        rules = """
        **Welcome to our Hackathon Server!**
        1. Be respectful to everyone
        2. No spam in channels
        3. Keep discussions relevant
        """
        
        embed = discord.Embed(
            title=f"Welcome {member.name}!",
            description=rules,
            color=discord.Color.green()
        )
        await welcome_channel.send(embed=embed)
        await member.send("Please complete your profile with !setup to get started!")

async def setup(bot):
    await bot.add_cog(Welcome(bot))