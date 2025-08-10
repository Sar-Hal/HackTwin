"""
HackTwin Web Application
Main Flask application with Outreach Agent functionality
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import os
import smtplib
from email.mime.text import MIMEText
from pymongo import MongoClient
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
import threading
import time

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')

# Configure Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# MongoDB connection
try:
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client["hackathon_twin"]
    users_collection = db["users"]
    campaigns_collection = db["campaigns"]  # New collection for campaign tracking
    print("✅ Successfully connected to MongoDB")
except Exception as e:
    print(f"❌ Error connecting to MongoDB: {e}")

# SMTP setup
smtp_server = "smtp.gmail.com"
smtp_port = 587

class OutreachAgent:
    """Outreach Agent class for managing email campaigns"""
    
    def __init__(self):
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
    
    def insert_sample_users(self):
        """Insert sample users if none exist"""
        existing_count = users_collection.count_documents({})
        if existing_count == 0:
            sample_users = [
                {
                    "name": "Alice Johnson",
                    "email": "alice.johnson@example.com",
                    "job_title": "Machine Learning Engineer",
                    "keywords": ["Python", "TensorFlow", "Data Science", "AI"],
                    "status": "PENDING",
                    "created_at": datetime.utcnow()
                },
                {
                    "name": "Bob Chen",
                    "email": "bob.chen@example.com", 
                    "job_title": "Full Stack Developer",
                    "keywords": ["JavaScript", "React", "Node.js", "MongoDB"],
                    "status": "PENDING",
                    "created_at": datetime.utcnow()
                },
                {
                    "name": "Carol Williams",
                    "email": "carol.williams@example.com",
                    "job_title": "Data Scientist",
                    "keywords": ["Python", "Pandas", "Machine Learning", "Statistics"],
                    "status": "PENDING",
                    "created_at": datetime.utcnow()
                }
            ]
            users_collection.insert_many(sample_users)
            return len(sample_users)
        return existing_count
    
    def generate_personalized_email(self, user_data):
        """Generate personalized email using Gemini AI"""
        prompt = f"""
        Generate a personalized email invite for the Hack-Nation Global AI Hackathon.
        Recipient: {user_data['name']}, Job Title: {user_data['job_title']}, Keywords/Skills: {', '.join(user_data['keywords'])}.
        
        Structure the email as follows:
        1. Greeting: Personalized and friendly, e.g., "Dear {user_data['name']},"
        2. Introduction: Briefly introduce Hack-Nation and the hackathon's mission (experiment with AI, build bridges, launch ventures).
        3. Personalization: Highlight how their skills ({', '.join(user_data['keywords'])}) make them a great fit, and mention AI-powered team matchmaking.
        4. Call to Action: Encourage them to join with the registration link: https://hack-nation.ai/
        5. Community: Invite them to join our Discord community for networking and updates: https://discord.gg/cq7DPV67
        6. Closing: Warm sign-off from the Hack-Nation team.
        
        IMPORTANT: Include both the registration link https://hack-nation.ai/ and Discord invite https://discord.gg/cq7DPV67 in the email.
        Keep the email concise (under 150 words), engaging, and professional.
        """
        
        try:
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"❌ Error generating email content for {user_data['name']}: {e}")
            # Return fallback template
            return f"""Dear {user_data['name']},

We're excited to invite you to the Hack-Nation Global AI Hackathon! 

Your expertise in {', '.join(user_data['keywords'])} makes you a perfect fit for our AI-focused event where innovators build bridges and launch ventures.

Join us for an amazing experience with AI-powered team matchmaking to connect you with like-minded developers.

Ready to hack the future? Register now at: https://hack-nation.ai/

🚀 Join our Discord community for networking, updates, and team formation: https://discord.gg/cq7DPV67

Best regards,
The Hack-Nation Team"""
    
    def send_campaign(self, test_mode=True):
        """Send email campaign"""
        # Insert sample users if none exist
        self.insert_sample_users()
        
        # Get pending users
        users = list(users_collection.find({"status": {"$ne": "SENT"}}))
        
        if not users:
            return {"success": False, "message": "No users found to send emails to."}
        
        campaign_id = campaigns_collection.insert_one({
            "created_at": datetime.utcnow(),
            "total_users": len(users),
            "test_mode": test_mode,
            "status": "RUNNING"
        }).inserted_id
        
        results = {
            "campaign_id": str(campaign_id),
            "total_users": len(users),
            "sent": 0,
            "failed": 0,
            "emails": []
        }
        
        if test_mode:
            # Test mode - generate emails without sending
            for user in users:
                try:
                    email_content = self.generate_personalized_email(user)
                    results["emails"].append({
                        "name": user["name"],
                        "email": user["email"],
                        "content": email_content,
                        "status": "GENERATED"
                    })
                    results["sent"] += 1
                except Exception as e:
                    results["emails"].append({
                        "name": user["name"],
                        "email": user["email"],
                        "error": str(e),
                        "status": "ERROR"
                    })
                    results["failed"] += 1
        else:
            # Production mode - actually send emails
            if not self.sender_email or not self.sender_password:
                return {"success": False, "message": "Email credentials not configured"}
            
            try:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(self.sender_email, self.sender_password)
                    
                    for user in users:
                        try:
                            email_content = self.generate_personalized_email(user)
                            
                            msg = MIMEText(email_content)
                            msg["Subject"] = f"Join Hack-Nation's Global AI Hackathon, {user['name']}!"
                            msg["From"] = self.sender_email
                            msg["To"] = user["email"]
                            
                            server.send_message(msg)
                            
                            # Update user status
                            users_collection.update_one(
                                {"_id": user["_id"]},
                                {"$set": {"status": "SENT", "sent_at": datetime.utcnow()}}
                            )
                            
                            results["emails"].append({
                                "name": user["name"],
                                "email": user["email"],
                                "status": "SENT"
                            })
                            results["sent"] += 1
                            
                        except Exception as e:
                            users_collection.update_one(
                                {"_id": user["_id"]},
                                {"$set": {"status": "ERROR", "error_message": str(e)}}
                            )
                            results["emails"].append({
                                "name": user["name"],
                                "email": user["email"],
                                "error": str(e),
                                "status": "ERROR"
                            })
                            results["failed"] += 1
                            
            except Exception as e:
                return {"success": False, "message": f"SMTP connection error: {str(e)}"}
        
        # Update campaign status
        campaigns_collection.update_one(
            {"_id": campaign_id},
            {"$set": {
                "status": "COMPLETED",
                "completed_at": datetime.utcnow(),
                "sent": results["sent"],
                "failed": results["failed"]
            }}
        )
        
        results["success"] = True
        return results

# Initialize the outreach agent
outreach_agent = OutreachAgent()

# Routes
@app.route('/')
def index():
    """Main dashboard"""
    # Get stats
    total_users = users_collection.count_documents({})
    pending_users = users_collection.count_documents({"status": "PENDING"})
    sent_users = users_collection.count_documents({"status": "SENT"})
    error_users = users_collection.count_documents({"status": "ERROR"})
    
    recent_campaigns = list(campaigns_collection.find().sort("created_at", -1).limit(5))
    
    stats = {
        "total_users": total_users,
        "pending_users": pending_users,
        "sent_users": sent_users,
        "error_users": error_users,
        "recent_campaigns": recent_campaigns
    }
    
    return render_template('dashboard.html', stats=stats)

@app.route('/outreach')
def outreach():
    """Outreach Agent page"""
    users = list(users_collection.find().sort("created_at", -1))
    return render_template('outreach.html', users=users)

@app.route('/api/campaign/test', methods=['POST'])
def test_campaign():
    """Run test campaign (generate emails without sending)"""
    try:
        results = outreach_agent.send_campaign(test_mode=True)
        return jsonify(results)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/campaign/send', methods=['POST'])
def send_campaign():
    """Send actual email campaign"""
    try:
        results = outreach_agent.send_campaign(test_mode=False)
        return jsonify(results)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/users/add', methods=['POST'])
def add_user():
    """Add new user"""
    try:
        data = request.json
        user = {
            "name": data["name"],
            "email": data["email"],
            "job_title": data["job_title"],
            "keywords": data["keywords"],
            "status": "PENDING",
            "created_at": datetime.utcnow()
        }
        result = users_collection.insert_one(user)
        return jsonify({"success": True, "user_id": str(result.inserted_id)})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/users/reset', methods=['POST'])
def reset_users():
    """Reset all user statuses to PENDING"""
    try:
        result = users_collection.update_many(
            {},
            {"$set": {"status": "PENDING"}, "$unset": {"error_message": "", "sent_at": ""}}
        )
        return jsonify({"success": True, "modified": result.modified_count})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/users')
def users_page():
    """Users management page"""
    users = list(users_collection.find().sort("created_at", -1))
    return render_template('users.html', users=users)

@app.route('/campaigns')
def campaigns_page():
    """Campaign history page"""
    campaigns = list(campaigns_collection.find().sort("created_at", -1))
    return render_template('campaigns.html', campaigns=campaigns)

if __name__ == '__main__':
    print("🚀 Starting HackTwin Web Application")
    print("=" * 50)
    print("🌐 Access the application at: http://localhost:5000")
    print("📧 Outreach Agent at: http://localhost:5000/outreach")
    print("👥 Users Management at: http://localhost:5000/users")
    print("📊 Campaign History at: http://localhost:5000/campaigns")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
