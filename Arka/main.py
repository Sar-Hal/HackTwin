import discord
from discord.ext import commands
from discord import Intents
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize bot with required intents
intents = Intents.all()  # Enable all intents
intents.messages = True
intents.message_content = True
intents.members = True
intents.guilds = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user}')
    print(f'Invite URL: https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=277025770560&scope=bot%20applications.commands')

@bot.event
async def on_guild_join(guild):
    """Auto-create channels and roles when bot joins a server"""
    try:
        # Create roles
        roles = {
            "Hackathon Participant": discord.Colour.green(),
            "Team Lead": discord.Colour.blue(),
            "Mentor": discord.Colour.gold(),
            "Organizer": discord.Colour.red()
        }
        
        created_roles = {}
        for name, color in roles.items():
            role = await guild.create_role(name=name, color=color)
            created_roles[name] = role

        # Create channels under a category
        category = await guild.create_category("Hackathon")
        
        channel_types = {
            "text": guild.create_text_channel,
            "voice": guild.create_voice_channel
        }
        
        channels = [
            ("welcome", "text"),
            ("announcements", "text"),
            ("team-formation", "text"),
            ("help-desk", "text"),
            ("matchmaking", "text"),
            ("voice-chat", "voice")
        ]
        
        for name, channel_type in channels:
            await channel_types[channel_type](name, category=category)

        # Send welcome message
        welcome_channel = discord.utils.get(guild.text_channels, name="welcome")
        if welcome_channel:
            embed = discord.Embed(
                title="Hackathon Bot Ready!",
                description="I'll help manage your hackathon!\n\n"
                           "**Key Commands:**\n"
                           "`!setup` - Create your profile\n"
                           "`!ask` - Get hackathon info\n"
                           "`!match` - Find teammates\n"
                           "`!help` - Show all commands",
                color=discord.Color.blue()
            )
            await welcome_channel.send(embed=embed)
            
    except discord.Forbidden:
        print(f"Missing permissions in server: {guild.name}")
    except Exception as e:
        print(f"Error setting up server {guild.name}: {str(e)}")

@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == bot.user:
        return

    # Auto-response to certain keywords
    keywords = {
        "hello": "Hi there! Type `!help` to see what I can do!",
        "help": "Check out `!ask` for FAQs or `!match` to find teammates!",
        "deadline": "Submission deadline is Friday at 5PM! Use `!ask deadline` for details.",
        "hi": "Hello! Use `!setup` to get started with the hackathon!",
        "thanks": "You're welcome! Happy hacking! 🚀"
    }
    
    content_lower = message.content.lower()
    for keyword, response in keywords.items():
        if keyword in content_lower:
            await message.channel.send(response)
            break

    # Process commands
    await bot.process_commands(message)

@bot.command()
async def setup(ctx):
    """Start the profile setup process"""
    embed = discord.Embed(
        title="Profile Setup",
        description="Let's get you set up for the hackathon!\n\n"
                   "Please check your DMs to complete your profile.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)
    
    try:
        # Start DM conversation
        await ctx.author.send("Let's set up your profile!\n\n"
                            "What are your top 3 skills? (e.g., Python, JavaScript, UI Design)")
    except discord.Forbidden:
        await ctx.send(f"{ctx.author.mention}, I couldn't DM you. Please enable DMs from server members!")

@bot.command()
async def ask(ctx, *, question):
    """Ask a question about the hackathon"""
    # In a real implementation, this would use your RAG system
    responses = {
        "deadline": "The submission deadline is Friday at 5PM EST.",
        "prizes": "1st place: $1000, 2nd place: $500, 3rd place: $250",
        "rules": "1. No cheating\n2. Be respectful\n3. Have fun!",
        "team size": "Teams can have 3-5 members."
    }
    
    answer = responses.get(question.lower(), "I don't have information about that. Please ask an organizer.")
    await ctx.send(f"**Q:** {question}\n**A:** {answer}")

@bot.command()
async def match(ctx):
    """Find potential teammates"""
    # In a real implementation, this would use your matching algorithm
    mock_matches = [
        {"name": "Alice", "skills": ["Python", "ML"]},
        {"name": "Bob", "skills": ["JavaScript", "UI/UX"]},
        {"name": "Charlie", "skills": ["Backend", "DevOps"]}
    ]
    
    embed = discord.Embed(
        title="Potential Teammates",
        description="Here are some participants you might want to team up with:",
        color=discord.Color.purple()
    )
    
    for match in mock_matches[:3]:  # Show top 3 matches
        embed.add_field(
            name=match["name"],
            value=f"Skills: {', '.join(match['skills'])}",
            inline=False
        )
    
    embed.set_footer(text="Use !team invite @user to form a team")
    await ctx.send(embed=embed)

if __name__ == '__main__':
    bot.run(os.getenv('DISCORD_TOKEN'))