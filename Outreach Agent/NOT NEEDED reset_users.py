"""
MongoDB Utility Script for Outreach Agent
This script helps you manage users in the MongoDB database
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# MongoDB connection
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["hackathon_twin"]
users_collection = db["users"]

def reset_user_statuses():
    """Reset all user statuses to PENDING"""
    result = users_collection.update_many(
        {},
        {"$set": {"status": "PENDING"}, "$unset": {"error_message": ""}}
    )
    print(f"✅ Reset {result.modified_count} user statuses to PENDING")

if __name__ == "__main__":
    print("🔄 Resetting user statuses to PENDING...")
    reset_user_statuses()
    print("✅ Done! You can now run the agent to see email previews.")
