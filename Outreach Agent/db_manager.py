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

def view_all_users():
    """View all users in the database"""
    users = list(users_collection.find())
    print(f"\n📊 Total users in database: {len(users)}")
    print("=" * 80)
    
    for user in users:
        print(f"Name: {user['name']}")
        print(f"Email: {user['email']}")
        print(f"Job Title: {user['job_title']}")
        print(f"Skills: {', '.join(user['keywords'])}")
        print(f"Status: {user['status']}")
        if 'error_message' in user:
            print(f"Error: {user['error_message']}")
        print("-" * 40)

def reset_user_statuses():
    """Reset all user statuses to PENDING"""
    result = users_collection.update_many(
        {},
        {"$set": {"status": "PENDING"}, "$unset": {"error_message": ""}}
    )
    print(f"✅ Reset {result.modified_count} user statuses to PENDING")

def add_new_user():
    """Add a new user to the database"""
    print("\n📝 Adding new user:")
    name = input("Enter name: ")
    email = input("Enter email: ")
    job_title = input("Enter job title: ")
    keywords = input("Enter skills (comma-separated): ").split(',')
    keywords = [skill.strip() for skill in keywords]
    
    user = {
        "name": name,
        "email": email,
        "job_title": job_title,
        "keywords": keywords,
        "status": "PENDING"
    }
    
    users_collection.insert_one(user)
    print(f"✅ Added user: {name}")

def delete_all_users():
    """Delete all users from the database"""
    confirm = input("⚠️  Are you sure you want to delete ALL users? (type 'YES' to confirm): ")
    if confirm == "YES":
        result = users_collection.delete_many({})
        print(f"🗑️  Deleted {result.deleted_count} users")
    else:
        print("❌ Operation cancelled")

def export_users():
    """Export all users to a JSON file"""
    users = list(users_collection.find())
    # Convert ObjectId to string for JSON serialization
    for user in users:
        user['_id'] = str(user['_id'])
    
    with open('users_export.json', 'w') as f:
        json.dump(users, f, indent=2)
    
    print(f"✅ Exported {len(users)} users to users_export.json")

def main():
    """Main menu"""
    while True:
        print("\n🛠️  MongoDB User Management")
        print("=" * 40)
        print("1. View all users")
        print("2. Reset user statuses to Pending")
        print("3. Add new user")
        print("4. Delete all users")
        print("5. Export users to JSON")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            view_all_users()
        elif choice == '2':
            reset_user_statuses()
        elif choice == '3':
            add_new_user()
        elif choice == '4':
            delete_all_users()
        elif choice == '5':
            export_users()
        elif choice == '6':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    print("🚀 Connecting to MongoDB...")
    try:
        # Test connection
        users_collection.count_documents({})
        print("✅ Successfully connected to MongoDB")
        main()
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
