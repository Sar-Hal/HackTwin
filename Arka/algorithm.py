# Update the import path if 'mongo.py' is in the same directory or adjust as needed
from mongo import MongoDB
from models import Participant
from typing import List, Dict

class MatchMaker:
    def __init__(self, db: MongoDB):
        self.db = db
    
    async def auto_match_teams(self, guild):
        """Automatically match participants into balanced teams based on skills"""
        import discord  # Ensure discord is imported

        try:
            # Get all participants looking for teams
            participants = await self.db.participants.find({
                "looking_for_team": True,
                "team_id": None
            }).to_list(None)
            
            if not participants:
                print("No participants looking for teams")
                return

            # Enhanced grouping algorithm
            teams = []
            skill_matrix = {}
            
            # Build skill matrix and participant index
            for p in participants:
                for skill in p['skills']:
                    if skill['name'] not in skill_matrix:
                        skill_matrix[skill['name']] = []
                    skill_matrix[skill['name']].append({
                        'participant': p,
                        'level': skill['level']
                    })
            
            # Sort skills by rarity (least common first)
            sorted_skills = sorted(skill_matrix.items(), key=lambda x: len(x[1]))
            
            # Create balanced teams (3-5 members each)
            team_size = min(max(3, len(participants) // 5), 5)  # Target 3-5 per team
            used_participants = set()
            
            for skill, skilled_participants in sorted_skills:
                # Filter out already assigned participants
                available = [p for p in skilled_participants 
                            if p['participant']['discord_id'] not in used_participants]
                
                if not available:
                    continue
                    
                # Create new team if needed
                if not teams or len(teams[-1]['members']) >= team_size:
                    teams.append({
                        'skills': set(),
                        'members': []
                    })
                
                # Add participants to current team
                for participant in available[:team_size - len(teams[-1]['members'])]:
                    teams[-1]['members'].append(participant['participant'])
                    teams[-1]['skills'].update(s['name'] for s in participant['participant']['skills'])
                    used_participants.add(participant['participant']['discord_id'])

            # Create Discord teams
            for i, team in enumerate(teams):
                if len(team['members']) < 3:  # Skip incomplete teams
                    continue
                    
                team_name = f"Team-{i+1}-{''.join(s[:2] for s in sorted(team['skills'])[:3])}"
                
                try:
                    # Create team role
                    role = await guild.create_role(
                        name=team_name,
                        color=discord.Color.random(),
                        mentionable=True
                    )
                    
                    # Create private channel
                    overwrites = {
                        guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        role: discord.PermissionOverwrite(
                            read_messages=True,
                            send_messages=True,
                            embed_links=True
                        )
                    }
                    
                    channel = await guild.create_text_channel(
                        name=team_name.lower().replace(' ', '-'),
                        overwrites=overwrites,
                        topic=f"Team channel for {team_name} | Skills: {', '.join(sorted(team['skills']))}"
                    )
                    
                    # Add members and update database
                    for member in team['members']:
                        discord_member = guild.get_member(int(member['discord_id']))
                        if discord_member:
                            await discord_member.add_roles(role)
                            await self.db.participants.update_one(
                                {"discord_id": member['discord_id']},
                                {"$set": {
                                    "team_id": str(role.id),
                                    "looking_for_team": False
                                }}
                            )
                    
                    # Send rich welcome message
                    embed = discord.Embed(
                        title=f"Welcome to {team_name}!",
                        description="Your team has been automatically formed based on skill compatibility.",
                        color=role.color
                    )
                    embed.add_field(
                        name="Team Skills",
                        value=', '.join(sorted(team['skills'])),
                        inline=False
                    )
                    embed.add_field(
                        name="Members",
                        value='\n'.join([f"<@{m['discord_id']}>" for m in team['members']]),
                        inline=False
                    )
                    embed.add_field(
                        name="Channel",
                        value=f"This is your private team channel. Use it to collaborate!",
                        inline=False
                    )
                    embed.set_footer(text="Use !help in this channel for team-specific commands")
                    
                    await channel.send(embed=embed)
                    
                    # Create initial team introduction thread
                    thread = await channel.create_thread(
                        name="Introduce Yourselves",
                        auto_archive_duration=1440  # 1 day
                    )
                    await thread.send(
                        "Please introduce yourself with:\n"
                        "- Your name\n"
                        "- Your skills\n"
                        "- What you'd like to work on\n"
                        "- Your availability"
                    )
                    
                except discord.Forbidden:
                    print(f"Missing permissions to create team in {guild.name}")
                except discord.HTTPException as e:
                    print(f"Error creating team in {guild.name}: {e}")
                    
        except Exception as e:
            print(f"Error in auto_match_teams: {str(e)}")
            raise