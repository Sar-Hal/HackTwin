import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    MONGO_URI = os.getenv('MONGODB_DISCORD', 'mongodb+srv://Hacktwin:Rivu2004@cluster0.oadcf6k.mongodb.net/')
    DATABASE_NAME = 'hackathon_bot'
    EMBEDDING_MODEL = 'BAAI/bge-small-en-v1.5'
    LLM_MODEL = 'mistralai/Mistral-7B-Instruct-v0.1'
    FAQ_FILE = 'faqs.txt'
    