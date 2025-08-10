# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from rag import RAGSystem
from mongo import MongoDB
import asyncio
import traceback

# Load environment variables
load_dotenv()

class HackathonBot(commands.Bot):
    def __init__(self):
        # Set up intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        
        # Initialize the bot
        super().__init__(command_prefix='!', intents=intents)
        
        # Initialize systems
        self.rag_system = RAGSystem()
        self.db = MongoDB()
        
        # Remove default help command
        self.remove_command('help')

    async def setup_hook(self):
        print("Setting up bot commands...")
        self.setup_commands()

    def setup_commands(self):
        @self.command(name='ask')
        async def ask(ctx, *, question=None):
            """Ask a question about the hackathon"""
            if not question:
                embed = discord.Embed(
                    title="❓ How to Ask Questions",
                    description="Please include your question after the command. For example:\n"
                               "`!ask When is the submission deadline?`\n"
                               "`!ask How do I get mentoring help?`\n"
                               "`!ask What API credits are available?`",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
                return

            print(f"Processing question from {ctx.author}: {question}")
            
            async with ctx.typing():
                try:
                    answer = await self.rag_system.get_answer(question)
                    print(f"Got answer: {answer[:100]}...")
                    
                    embed = discord.Embed(
                        title="🤖 Hackathon FAQ",
                        description=answer,
                        color=discord.Color.green()
                    )
                    embed.set_footer(text="If this doesn't fully answer your question, try asking in a different way!")
                    await ctx.send(embed=embed)
                    
                except Exception as e:
                    print(f"Error processing question: {str(e)}")
                    print(traceback.format_exc())
                    await ctx.send("Sorry, I encountered an error while processing your question. Please try again!")

        @self.command(name='help')
        async def help_command(ctx):
            """Show help message with available commands"""
            embed = discord.Embed(
                title="🚀 Hackathon Bot Commands",
                description="Here's how I can help you:",
                color=discord.Color.blue()
            )
            
            commands_info = {
                "!ask <question>": "Get answers about the hackathon\nExample: `!ask When is the deadline?`",
                "!help": "Show this help message"
            }
            
            for command, description in commands_info.items():
                embed.add_field(name=command, value=description, inline=False)
            
            embed.set_footer(text="Have questions? Just ask! I'm here to help! 😊")
            await ctx.send(embed=embed)

    async def on_ready(self):
        """Called when the bot is ready"""
        print(f'Bot is ready! Logged in as {self.user}')
        print(f'Invite URL: https://discord.com/api/oauth2/authorize?client_id={self.user.id}&permissions=277025770560&scope=bot%20applications.commands')

    async def on_command_error(self, ctx, error):
        """Handle command errors"""
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.command.name == 'ask':
                embed = discord.Embed(
                    title="❓ How to Ask Questions",
                    description="Please include your question after the command. For example:\n"
                               "`!ask When is the submission deadline?`\n"
                               "`!ask How do I get mentoring help?`\n"
                               "`!ask What API credits are available?`",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("Command not found. Use `!help` to see available commands!")
        else:
            print(f"An error occurred: {str(error)}")
            print(traceback.format_exc())
            await ctx.send("Sorry, something went wrong. Please try again!")

async def main():
    """Main entry point for the bot"""
    async with HackathonBot() as bot:
        await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot shutdown requested")
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        print(traceback.format_exc())