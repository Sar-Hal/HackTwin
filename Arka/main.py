import discord
from discord.ext import commands
from config import Config
from mongo import MongoDB
from rag import RAGSystem
from algorithm import MatchMaker

class HackathonBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix='!', intents=intents)
        
        self.config = Config()
        self.db = MongoDB(self.config)
        self.faq = RAGSystem(self.config)
        self.matcher = MatchMaker(self.db)
        
    async def setup_hook(self):
        await self.load_extension('onboarding.welcome')
        await self.load_extension('onboarding.verification')

bot = HackathonBot()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def ask(ctx, *, question):
    """Ask a question about the hackathon"""
    answer = await bot.faq.generate_answer(question)
    await ctx.send(f"**Q:** {question}\n**A:** {answer}")

@bot.command()
async def match(ctx):
    """Find potential teammates"""
    matches = await bot.matcher.find_matches(ctx.author.id)
    if matches:
        response = "**Potential Teammates:**\n" + "\n".join(
            f"- {m['username']} (Skills: {', '.join(m['skills'])})"
            for m in matches[:5]
        )
    else:
        response = "No matches found yet. Try again later!"
    await ctx.send(response)

if __name__ == '__main__':
    bot.run(bot.config.DISCORD_TOKEN)