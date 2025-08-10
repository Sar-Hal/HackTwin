import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Discord Bot Configuration
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    
    # MongoDB Configuration
    MONGO_URI = os.getenv('MONGODB_ARKA', 'mongodb+srv://username:password@cluster.mongodb.net/')
    DATABASE_NAME = 'hackathon_bot'
    
    # Gemini API Keys Configuration (multiple keys for load balancing)
    GEMINI_API_KEY1 = os.getenv('GEMINI_API_KEY1')
    GEMINI_API_KEY2 = os.getenv('GEMINI_API_KEY2')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')  # Fallback
    
    # Model Configuration
    EMBEDDING_MODEL = 'BAAI/bge-small-en-v1.5'
    LLM_MODEL = 'mistralai/Mistral-7B-Instruct-v0.1'
    FAQ_FILE = 'faqs.txt'
    