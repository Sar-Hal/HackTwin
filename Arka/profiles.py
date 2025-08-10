import discord
from discord.ext import commands
from mongo import MongoDB
from models import Participant

class ProfileManager:
    def __init__(self, db: MongoDB):
        self.db = db
    
    async def create_profile(self, ctx: commands.Context):
        """Interactive profile creation via DM"""
        def check(m):
            return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)
        
        await ctx.author.send("Let's set up your profile! What are your top 3 skills? (e.g., Python, Design, ML)")
        
        try:
            skills_msg = await self.bot.wait_for('message', check=check, timeout=120)
            skills = [s.strip() for s in skills_msg.content.split(',')[:3]]
            
            # Continue with other profile fields...
            
            participant = Participant(
                discord_id=str(ctx.author.id),
                username=ctx.author.name,
                skills=[{'name': s, 'level': 3} for s in skills],
                looking_for_team=True
            )
            
            await self.db.save_participant(participant.dict())
            await ctx.author.send("Profile created successfully!")
            
        except TimeoutError:
            await ctx.author.send("Profile creation timed out. Please try again with !setup")