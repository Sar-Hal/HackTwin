import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    DATABASE_NAME = 'hackathon_bot'
    EMBEDDING_MODEL = 'BAAI/bge-small-en-v1.5'
    LLM_MODEL = 'mistralai/Mistral-7B-Instruct-v0.1'
    FAQ_FILE = 'data/faqs.txt'