from pymongo import MongoClient
from config import Config
from .models import Participant, Team

class MongoDB:
    def __init__(self, config):
        self.client = MongoClient(config.MONGO_URI)
        self.db = self.client[config.DATABASE_NAME]
        self.participants = self.db.participants
        self.teams = self.db.teams
        self.faq_embeddings = self.db.faq_embeddings
        
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