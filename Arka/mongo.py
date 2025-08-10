from pymongo import MongoClient
from config import MONGODB_URI, DB_NAME

class MongoDB:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[DB_NAME]
        self.users = self.db.users
        self.teams = self.db.teams
        
    async def save_participant(self, participant_data):
        return self.participants.update_one(
            {'discord_id': participant_data['discord_id']},
            {'$set': participant_data},
            upsert=True
        )
        
    async def find_participant(self, discord_id):
        return self.participants.find_one({'discord_id': discord_id})
    
    async def find_similar_skills(self, skills):
        return self.participants.find({
            'skills': {'$in': skills},
            'looking_for_team': True
        }).limit(10)