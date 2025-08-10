import os
import smtplib
from email.mime.text import MIMEText
from pymongo import MongoClient
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# MongoDB connection
try:
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client["hackathon_twin"]  # Database name
    users_collection = db["users"]  # Collection for user profiles
    print("✅ Successfully connected to MongoDB")
except Exception as e:
    print(f"❌ Error connecting to MongoDB: {e}")
    exit(1)

# SMTP setup (using Gmail for demo; use app password for security)
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")

# Validate environment variables
if not all([sender_email, sender_password, os.getenv("GEMINI_API_KEY"), os.getenv("MONGODB_URI")]):
    print("❌ Missing required environment variables. Please check your .env file.")
    print("Required: SENDER_EMAIL, SENDER_PASSWORD, GEMINI_API_KEY, MONGODB_URI")
    exit(1)

# Function to insert sample users (for testing)
def insert_sample_users():
    """Insert sample users into MongoDB for testing purposes"""
    sample_users = [
        {
            "name": "Alice Johnson",
            "email": "alice.johnson@example.com",
            "job_title": "Machine Learning Engineer",
            "keywords": ["Python", "TensorFlow", "Data Science", "AI"],
            "status": "PENDING"
        },
        {
            "name": "Bob Chen",
            "email": "bob.chen@example.com", 
            "job_title": "Full Stack Developer",
            "keywords": ["JavaScript", "React", "Node.js", "MongoDB"],
            "status": "PENDING"
        },
        {
            "name": "Carol Williams",
            "email": "carol.williams@example.com",
            "job_title": "Data Scientist",
            "keywords": ["Python", "Pandas", "Machine Learning", "Statistics"],
            "status": "PENDING"
        }
    ]
    
    # Check if users already exist
    existing_count = users_collection.count_documents({})
    if existing_count == 0:
        users_collection.insert_many(sample_users)
        print(f"✅ Inserted {len(sample_users)} sample users into MongoDB")
    else:
        print(f"📊 Found {existing_count} existing users in MongoDB")

# Function to generate personalized email using Gemini
def generate_personalized_email(user_data):
    """Generate a personalized email using Gemini AI"""
    # Structured prompt for personalized email generation
    prompt = f"""
    Generate a personalized email invite for the Hack-Nation Global AI Hackathon.
    Recipient: {user_data['name']}, Job Title: {user_data['job_title']}, Keywords/Skills: {', '.join(user_data['keywords'])}.
    
    Structure the email as follows:
    1. Greeting: Personalized and friendly, e.g., "Dear {user_data['name']},"
    2. Introduction: Briefly introduce Hack-Nation and the hackathon's mission (experiment with AI, build bridges, launch ventures).
    3. Personalization: Highlight how their skills ({', '.join(user_data['keywords'])}) make them a great fit, and mention AI-powered team matchmaking.
    4. Call to Action: Encourage them to join, with an opt-in for matchmaking.
    5. Closing: Warm sign-off from the Hack-Nation team.
    
    Keep the email concise (under 150 words), engaging, and professional.
    """
    
    try:
        # Generate content using Gemini
        model = genai.GenerativeModel("gemini-2.0-flash-exp")  # Use free-tier compatible model
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ Error generating email content for {user_data['name']}: {e}")
        # Return a fallback email template
        return f"""Dear {user_data['name']},

We're excited to invite you to the Hack-Nation Global AI Hackathon! 

Your expertise in {', '.join(user_data['keywords'])} makes you a perfect fit for our AI-focused event where innovators build bridges and launch ventures.

Join us for an amazing experience with AI-powered team matchmaking to connect you with like-minded developers.

Ready to hack the future? Sign up now!

Best regards,
The Hack-Nation Team"""

# Main outreach function
def run_outreach(test_mode=True):
    """
    Run the email outreach campaign
    Args:
        test_mode (bool): If True, only generate emails without sending them
    """
    # Insert sample users if none exist
    insert_sample_users()
    
    # Fetch users from MongoDB who haven't been contacted yet (status != "SENT")
    users = list(users_collection.find({"status": {"$ne": "SENT"}}))
    
    if not users:
        print("📭 No users found to send emails to.")
        return
    
    print(f"📧 Found {len(users)} users to contact")
    
    if test_mode:
        print("🧪 Running in TEST MODE - emails will be generated but not sent")
        for user in users:
            try:
                # Generate personalized email content
                email_content = generate_personalized_email(user)
                print(f"\n📝 Generated email for {user['name']} ({user['email']}):")
                print("-" * 50)
                print(email_content)
                print("-" * 50)
                
            except Exception as e:
                print(f"❌ Error generating email for {user['name']}: {str(e)}")
        return
    
    # Production mode - actually send emails
    if not sender_email or not sender_password:
        print("❌ Email credentials not configured. Please set SENDER_EMAIL and SENDER_PASSWORD in .env file")
        return
        
    try:
        # Set up SMTP connection
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            print("✅ Successfully connected to SMTP server")
            
            for user in users:
                try:
                    # Generate personalized email content
                    email_content = generate_personalized_email(user)
                    
                    # Create MIME message
                    msg = MIMEText(email_content)
                    msg["Subject"] = f"Join Hack-Nation's Global AI Hackathon, {user['name']}!"
                    msg["From"] = sender_email
                    msg["To"] = user["email"]
                    
                    # Send email
                    server.send_message(msg)
                    
                    # Update status in MongoDB
                    users_collection.update_one(
                        {"_id": user["_id"]},
                        {"$set": {"status": "SENT"}}
                    )
                    print(f"✅ Email sent to {user['name']} ({user['email']}) and status updated.")
                    
                except Exception as e:
                    print(f"❌ Error sending email to {user['name']}: {str(e)}")
                    # Update status to ERROR
                    users_collection.update_one(
                        {"_id": user["_id"]},
                        {"$set": {"status": "ERROR", "error_message": str(e)}}
                    )
                    
    except Exception as e:
        print(f"❌ SMTP connection error: {str(e)}")
        print("💡 Make sure you have:")
        print("   - Enabled 2-factor authentication on Gmail")
        print("   - Generated an App Password (not your regular password)")
        print("   - Set the correct SENDER_EMAIL and SENDER_PASSWORD in .env")

# Run the outreach
if __name__ == "__main__":
    print("🚀 Starting Hack-Nation Outreach Agent")
    print("=" * 50)
    
    # First run in test mode to see generated emails
    print("\n🧪 Testing email generation...")
    run_outreach(test_mode=True)
    
    # Uncomment the line below to actually send emails (after configuring email credentials)
    # run_outreach(test_mode=False)
    
    print("\n✨ Outreach campaign completed!")
    print("💡 To send actual emails:")
    print("   1. Configure SENDER_EMAIL and SENDER_PASSWORD in .env file")
    print("   2. Uncomment the line: run_outreach(test_mode=False)")
    print("   3. Comment out the test mode line")