# Update the import path if 'mongo.py' is in the same directory or adjust as needed
from mongo import MongoDB
from models import Participant
from typing import List, Dict

class MatchMaker:
    def __init__(self, db: MongoDB):
        self.db = db
    
    async def find_matches(self, discord_id: str) -> List[Dict]:
        user = await self.db.find_participant(discord_id)
        if not user or not user.get('skills'):
            return []
            
        user_skills = [s['name'] for s in user['skills']]
        potential_matches = await self.db.find_similar_skills(user_skills)
        
        # Simple matching algorithm - can be enhanced
        matches = []
        for match in potential_matches:
            if match['discord_id'] != discord_id:
                common_skills = set(user_skills) & set(s['name'] for s in match['skills'])
                if common_skills:
                    matches.append({
                        'username': match['username'],
                        'skills': list(common_skills),
                        'common_interests': set(user.get('interests', [])) & set(match.get('interests', []))
                    })
        
        # Sort by number of common skills
        return sorted(matches, key=lambda x: len(x['skills']), reverse=True)