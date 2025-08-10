"""
HackTwin Web Application
Main Flask application with Outreach Agent functionality
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Configure Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# MongoDB connection
try:
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client["hackathon_twin"]
    users_collection = db["users"]
    campaigns_collection = db["campaigns"]
    print("✅ Successfully connected to MongoDB")
except Exception as e:
    print(f"❌ Error connecting to MongoDB: {e}")

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

class OutreachAgent:
    """Outreach Agent functionality wrapped in a class"""
    
    @staticmethod
    def generate_personalized_email(user_data):
        """Generate a personalized email using Gemini AI"""
        prompt = f"""
        Generate a personalized email invite for the Hack-Nation Global AI Hackathon.
        Recipient: {user_data['name']}, Job Title: {user_data['job_title']}, Keywords/Skills: {', '.join(user_data['keywords'])}.
        
        Structure the email as follows:
        1. Greeting: Personalized and friendly, e.g., "Dear {user_data['name']},"
        2. Introduction: Briefly introduce Hack-Nation and the hackathon's mission
        3. Personalization: Highlight how their skills make them a great fit
        4. Call to Action: Include registration link: https://hack-nation.ai/
        5. Closing: Warm sign-off from the Hack-Nation team
        
        Keep the email concise (under 150 words), engaging, and professional.
        """
        
        try:
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"❌ Error generating email for {user_data['name']}: {e}")
            # Fallback template
            return f"""Dear {user_data['name']},

We're excited to invite you to the Hack-Nation Global AI Hackathon! 

Your expertise in {', '.join(user_data['keywords'])} makes you perfect for our AI-focused event.

Ready to hack the future? Register now at: https://hack-nation.ai/

Best regards,
The Hack-Nation Team"""

    @staticmethod
    def send_email(user_data, email_content):
        """Send email to a user"""
        try:
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = user_data['email']
            msg['Subject'] = f"Join Hack-Nation's Global AI Hackathon, {user_data['name']}!"
            
            msg.attach(MIMEText(email_content, 'plain'))
            
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.send_message(msg)
            
            return True, "Email sent successfully"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def get_pending_users():
        """Get users who haven't been contacted"""
        return list(users_collection.find({"status": {"$ne": "SENT"}}))

    @staticmethod
    def update_user_status(user_id, status, error_message=None):
        """Update user status in database"""
        update_data = {"status": status}
        if error_message:
            update_data["error_message"] = error_message
        
        users_collection.update_one(
            {"_id": user_id},
            {"$set": update_data}
        )

# Routes
@app.route('/')
def index():
    """Home page"""
    user_count = users_collection.count_documents({})
    pending_count = users_collection.count_documents({"status": {"$ne": "SENT"}})
    sent_count = users_collection.count_documents({"status": "SENT"})
    
    stats = {
        'total_users': user_count,
        'pending': pending_count,
        'sent': sent_count
    }
    
    return render_template('index.html', stats=stats)

@app.route('/outreach')
def outreach_dashboard():
    """Outreach Agent dashboard"""
    users = list(users_collection.find())
    return render_template('outreach.html', users=users)

@app.route('/api/users')
def api_users():
    """API endpoint to get all users"""
    users = list(users_collection.find())
    # Convert ObjectId to string for JSON serialization
    for user in users:
        user['_id'] = str(user['_id'])
    return jsonify(users)

@app.route('/api/generate-preview', methods=['POST'])
def generate_preview():
    """Generate email preview without sending"""
    try:
        user_data = request.json
        email_content = OutreachAgent.generate_personalized_email(user_data)
        return jsonify({
            'success': True,
            'email_content': email_content
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/send-campaign', methods=['POST'])
def send_campaign():
    """Send email campaign to all pending users"""
    try:
        test_mode = request.json.get('test_mode', True)
        pending_users = OutreachAgent.get_pending_users()
        
        if not pending_users:
            return jsonify({
                'success': False,
                'message': 'No pending users found'
            })
        
        results = []
        
        for user in pending_users:
            try:
                # Generate email content
                email_content = OutreachAgent.generate_personalized_email(user)
                
                if test_mode:
                    # Test mode - just generate preview
                    results.append({
                        'user': user['name'],
                        'status': 'preview_generated',
                        'email_content': email_content
                    })
                else:
                    # Production mode - send actual email
                    success, message = OutreachAgent.send_email(user, email_content)
                    
                    if success:
                        OutreachAgent.update_user_status(user['_id'], 'SENT')
                        results.append({
                            'user': user['name'],
                            'status': 'sent',
                            'message': message
                        })
                    else:
                        OutreachAgent.update_user_status(user['_id'], 'ERROR', message)
                        results.append({
                            'user': user['name'],
                            'status': 'error',
                            'message': message
                        })
                        
            except Exception as e:
                results.append({
                    'user': user['name'],
                    'status': 'error',
                    'message': str(e)
                })
        
        return jsonify({
            'success': True,
            'results': results,
            'mode': 'test' if test_mode else 'production'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/add-user', methods=['POST'])
def add_user():
    """Add a new user to the database"""
    try:
        user_data = request.json
        
        # Validate required fields
        required_fields = ['name', 'email', 'job_title', 'keywords']
        for field in required_fields:
            if field not in user_data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Prepare user document
        user_doc = {
            'name': user_data['name'],
            'email': user_data['email'],
            'job_title': user_data['job_title'],
            'keywords': user_data['keywords'] if isinstance(user_data['keywords'], list) else user_data['keywords'].split(','),
            'status': 'PENDING',
            'created_at': datetime.now()
        }
        
        # Insert into database
        result = users_collection.insert_one(user_doc)
        
        return jsonify({
            'success': True,
            'message': f'User {user_data["name"]} added successfully',
            'user_id': str(result.inserted_id)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/reset-statuses', methods=['POST'])
def reset_statuses():
    """Reset all user statuses to PENDING"""
    try:
        result = users_collection.update_many(
            {},
            {"$set": {"status": "PENDING"}, "$unset": {"error_message": ""}}
        )
        
        return jsonify({
            'success': True,
            'message': f'Reset {result.modified_count} user statuses to PENDING'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/insert-sample-users', methods=['POST'])
def insert_sample_users():
    """Insert sample users for testing"""
    try:
        sample_users = [
            {
                "name": "Alice Johnson",
                "email": "alice.johnson@example.com",
                "job_title": "Machine Learning Engineer",
                "keywords": ["Python", "TensorFlow", "Data Science", "AI"],
                "status": "PENDING",
                "created_at": datetime.now()
            },
            {
                "name": "Bob Chen",
                "email": "bob.chen@example.com", 
                "job_title": "Full Stack Developer",
                "keywords": ["JavaScript", "React", "Node.js", "MongoDB"],
                "status": "PENDING",
                "created_at": datetime.now()
            },
            {
                "name": "Carol Williams",
                "email": "carol.williams@example.com",
                "job_title": "Data Scientist",
                "keywords": ["Python", "Pandas", "Machine Learning", "Statistics"],
                "status": "PENDING",
                "created_at": datetime.now()
            }
        ]
        
        # Check if users already exist
        existing_count = users_collection.count_documents({})
        if existing_count == 0:
            users_collection.insert_many(sample_users)
            return jsonify({
                'success': True,
                'message': f'Inserted {len(sample_users)} sample users'
            })
        else:
            return jsonify({
                'success': False,
                'message': f'Users already exist ({existing_count} users found)'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("🚀 Starting HackTwin Web Application")
    print("📧 Outreach Agent Web Interface")
    print("🌐 Visit: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
