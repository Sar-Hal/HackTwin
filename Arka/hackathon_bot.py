import discord
from discord.ext import commands
import asyncio

# Replace with your bot token
BOT_TOKEN = '8'

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='create_test_server')
@commands.is_owner()  # Only the bot owner can run this
async def create_test_server(ctx):
    """Creates a dummy test server with all necessary channels"""
    try:
        # Create the server
        guild = await bot.create_guild(name="Hackathon Test Server")
        print(f"Created server: {guild.name} ({guild.id})")
        
        # Create categories and channels
        categories_and_channels = {
            "🏠 Information": ["welcome", "announcements", "rules", "faq"],
            "💬 General": ["general", "questions", "introductions"],
            "🤖 Bot Testing": ["bot-commands", "faq-test", "match-test"],
            "🚀 Projects": ["project-ideas", "team-formation"]
        }
        
        # Create each category and its channels
        for category_name, channel_names in categories_and_channels.items():
            # Create category
            category = await guild.create_category(category_name)
            print(f"Created category: {category.name}")
            
            # Create channels under this category
            for channel_name in channel_names:
                channel = await guild.create_text_channel(
                    name=channel_name,
                    category=category,
                    topic=f"Test channel for {channel_name}"
                )
                print(f"Created channel: #{channel.name}")
        
        # Create a voice channel
        await guild.create_voice_channel("General Voice", category=discord.utils.get(guild.categories, name="💬 General"))
        
        # Create basic roles
        roles = ["Admin", "Moderator", "Participant", "Mentor"]
        for role_name in roles:
            role = await guild.create_role(name=role_name)
            print(f"Created role: {role.name}")
        
        # Make the bot send a welcome message
        welcome_channel = discord.utils.get(guild.text_channels, name="welcome")
        if welcome_channel:
            await welcome_channel.send(
                "🚀 **Welcome to the Hackathon Test Server!**\n\n"
                "This is a dummy server for testing the Hackathon Helper Bot.\n"
                "Use `!ask` for FAQs and `!match` to find teammates!"
            )
        
        await ctx.send(f"Successfully created test server: {guild.name}")
    
    except Exception as e:
        await ctx.send(f"Error creating server: {e}")
        print(f"Error: {e}")

bot.run(BOT_TOKEN)