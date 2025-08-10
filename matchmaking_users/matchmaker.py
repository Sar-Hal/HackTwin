"""
HackTwin Matchmaking System
Advanced user matching based on skills extracted from resumes
"""

import os
import re
import time
import PyPDF2
import docx
import google.generativeai as genai
from pymongo import MongoClient
from bson import ObjectId
import numpy as np
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the API manager
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gemini_api_manager import api_manager

class SkillExtractor:
    """Extract skills from resume documents using Gemini AI"""
    
    def __init__(self):
        # No need to configure genai here - API manager handles it
        pass
    
    def extract_text_from_pdf(self, file_path):
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            print(f"❌ Error extracting PDF text: {e}")
            return ""
    
    def extract_text_from_docx(self, file_path):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"❌ Error extracting DOCX text: {e}")
            return ""
    
    def extract_text_from_file(self, file_path):
        """Extract text from various file formats"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            return self.extract_text_from_docx(file_path)
        elif file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def extract_skills_with_ai(self, resume_text):
        """Extract skills from resume text using Gemini AI"""
        prompt = f"""
        Analyze the following resume text and extract all technical skills, programming languages, 
        frameworks, tools, and technologies mentioned. 
        
        Return ONLY a comma-separated list of skills, no explanations or additional text.
        Focus on:
        - Programming languages (Python, JavaScript, Java, etc.)
        - Frameworks (React, Django, Flask, etc.)
        - Technologies (Docker, AWS, MongoDB, etc.)
        - Tools (Git, Jenkins, Kubernetes, etc.)
        - Soft skills (Leadership, Communication, etc.)
        
        Resume text:
        {resume_text}
        
        Skills (comma-separated):
        """
        
        try:
            print(f"🤖 Extracting skills with AI (with distributed keys)...")
            print("⏳ Applying rate limiting with key rotation (7 seconds)...")
            time.sleep(7)  # Reduced delay since we have multiple keys
            
            # Use the API manager to get a configured model with rotated key
            model = api_manager.get_configured_model("gemini-2.0-flash-exp")
            response = model.generate_content(prompt)
            skills_text = response.text.strip()
            
            # Clean and parse skills
            skills = [skill.strip() for skill in skills_text.split(',')]
            skills = [skill for skill in skills if skill and len(skill) > 1]
            
            print(f"✅ Successfully extracted {len(skills)} skills")
            return skills
        except Exception as e:
            print(f"❌ Error extracting skills with AI: {e}")
            print(f"⚠️  Using fallback pattern matching...")
            return self._fallback_skill_extraction(resume_text)
    
    def _fallback_skill_extraction(self, text):
        """Fallback skill extraction using pattern matching"""
        # Common technology patterns
        tech_patterns = [
            r'\b(?:Python|Java|JavaScript|TypeScript|C\+\+|C#|PHP|Ruby|Go|Rust|Swift)\b',
            r'\b(?:React|Angular|Vue|Django|Flask|Spring|Express|Laravel)\b',
            r'\b(?:AWS|Azure|GCP|Docker|Kubernetes|MongoDB|PostgreSQL|MySQL)\b',
            r'\b(?:Git|Jenkins|Docker|Terraform|Ansible|Linux|Windows)\b',
            r'\b(?:Machine Learning|AI|Data Science|DevOps|Frontend|Backend)\b'
        ]
        
        skills = set()
        for pattern in tech_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.update(matches)
        
        return list(skills)

class UserMatcher:
    """Match users based on skill overlap"""
    
    def __init__(self, db_collection):
        self.users_collection = db_collection
    
    def calculate_skill_similarity(self, user1_skills, user2_skills):
        """Calculate similarity based on common skills"""
        if not user1_skills or not user2_skills:
            return 0.0
        
        # Convert to lowercase for comparison
        skills1 = {skill.lower().strip() for skill in user1_skills}
        skills2 = {skill.lower().strip() for skill in user2_skills}
        
        # Find common skills
        common_skills = skills1.intersection(skills2)
        
        if not common_skills:
            return 0.0
        
        # Calculate overlap percentage based on smaller skill set
        smaller_set_size = min(len(skills1), len(skills2))
        similarity = len(common_skills) / smaller_set_size
        
        return similarity
    
    def find_similar_users(self, target_user_id, threshold=0.1, limit=10):
        """Find users with overlapping skills"""
        try:
            # Convert string ID to ObjectId if needed
            if isinstance(target_user_id, str):
                try:
                    target_user_id = ObjectId(target_user_id)
                except Exception as e:
                    print(f"❌ Invalid target_user_id format: {target_user_id}")
                    return []
            
            # Get target user
            target_user = self.users_collection.find_one({"_id": target_user_id})
            if not target_user or 'keywords' not in target_user:
                print(f"❌ Target user not found or has no keywords: {target_user_id}")
                return []
            
            target_skills = target_user['keywords']
            if not target_skills:
                print("❌ Target user has empty skills list")
                return []
            
            print(f"🎯 Looking for users with skills similar to: {target_skills}")
            
            similar_users = []
            
            # Get all other users with skills
            other_users = self.users_collection.find({
                "_id": {"$ne": target_user_id},
                "keywords": {"$exists": True, "$ne": []}
            })
            
            for user in other_users:
                if 'keywords' in user and user['keywords']:
                    # Calculate skill overlap
                    similarity = self.calculate_skill_similarity(target_skills, user['keywords'])
                    
                    if similarity >= threshold:
                        # Find actual common skills (preserve original case)
                        target_lower = {s.lower().strip(): s for s in target_skills}
                        user_lower = {s.lower().strip(): s for s in user['keywords']}
                        common_skill_keys = set(target_lower.keys()).intersection(set(user_lower.keys()))
                        common_skills = [target_lower[key] for key in common_skill_keys]
                        
                        print(f"✅ Match found: {user.get('name', 'Unknown')} - {len(common_skills)} common skills: {common_skills}")
                        
                        similar_users.append({
                            'user': user,
                            'similarity': similarity,
                            'common_skills': common_skills,
                            'overlap_count': len(common_skills)
                        })
            
            # Sort by number of common skills first, then by similarity
            similar_users.sort(key=lambda x: (x['overlap_count'], x['similarity']), reverse=True)
            
            print(f"🎉 Found {len(similar_users)} total matches")
            return similar_users[:limit]
            
        except Exception as e:
            print(f"❌ Error finding similar users: {e}")
            return []

class MatchmakingNotifier:
    """Send email notifications for user matches"""
    
    def __init__(self):
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def generate_consolidated_match_email(self, user, all_matches):
        """Generate ONE email with ALL matches for a user - MUCH more efficient!"""
        
        # Calculate total matches and format match details
        total_matches = len(all_matches)
        
        if total_matches == 0:
            return None
            
        # Format match details for the email
        match_details = []
        for i, match_data in enumerate(all_matches, 1):
            matched_user = match_data['user']
            similarity_percent = int(match_data['similarity'] * 100)
            common_skills = match_data['common_skills']
            
            match_details.append(f"""
{i}. {matched_user['name']} - {matched_user['job_title']}
   📧 Email: {matched_user['email']}
   🎯 Skill Match: {similarity_percent}%
   🔗 Common Skills: {', '.join(common_skills[:3])}{'...' if len(common_skills) > 3 else ''}
            """.strip())
        
        matches_text = '\n\n'.join(match_details)
        
        prompt = f"""
        Generate a personalized email for a hackathon participant about ALL their potential teammates.
        
        Recipient: {user['name']} ({user.get('job_title', 'Participant')})
        Total Matches Found: {total_matches}
        
        Match Details:
        {matches_text}
        
        Structure the email as follows:
        1. Exciting Greeting: Celebrate finding multiple potential teammates
        2. Overview: Mention the total number of matches found
        3. Team Options: Present the matches with their details (names, emails, skill percentages)
        4. Next Steps: Encourage connecting via Discord: https://discord.gg/cq7DPV67
        5. Team Formation Tips: Brief advice on choosing teammates
        6. Closing: Enthusiastic sign-off from Hack-Nation team
        
        Keep it engaging, professional, and under 300 words.
        Make them excited about the multiple options available!
        """
        
        try:
            print(f"🤖 Generating consolidated match email for {user['name']} ({total_matches} matches)...")
            print("⏳ Applying rate limiting with key rotation (6 seconds)...")
            time.sleep(6)  # One API call instead of N calls per user!
            
            # Use the API manager to get a configured model with rotated key
            model = api_manager.get_configured_model("gemini-2.0-flash-exp")
            response = model.generate_content(prompt)
            
            print(f"✅ Consolidated match email generated successfully")
            return response.text
        except Exception as e:
            print(f"❌ Error generating consolidated match email: {e}")
            print(f"⚠️  Using fallback consolidated template...")
            # Fallback template
            return f"""Dear {user['name']},

🎉 Fantastic news! We've found {total_matches} potential teammates for the Hack-Nation Global AI Hackathon!

Your Potential Team Members:

{matches_text}

These participants have been carefully matched based on complementary skills and experience levels. Each represents an excellent opportunity for collaboration!

🚀 Next Steps:
1. Review the matches above
2. Join our Discord community: https://discord.gg/cq7DPV67  
3. Reach out to teammates that interest you
4. Start planning your winning project!

💡 Pro Tip: Great teams combine diverse skills. Consider teammates who complement your expertise!

Ready to build something amazing together?

Best regards,
The Hack-Nation Team

P.S. The best hackathon projects come from great teamwork - choose wisely! 🏆"""
    
    def send_consolidated_match_notification(self, user_email, email_content, total_matches):
        """Send consolidated match notification email with ALL matches"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = user_email
            msg['Subject'] = f"🚀 {total_matches} Potential Teammates Found - Choose Your Dream Team!"
            
            msg.attach(MIMEText(email_content, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"✅ Consolidated match notification sent successfully ({total_matches} matches)")
            return True
        except Exception as e:
            print(f"❌ Error sending consolidated match notification: {e}")
            return False
        """Send match notification email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = user_email
            msg['Subject'] = f"🚀 Potential Teammate Found: Meet {matched_user_name}!"
            
            msg.attach(MIMEText(email_content, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"❌ Error sending match notification: {e}")
            return False

class MatchmakingSystem:
    """Main matchmaking system coordinator"""
    
    def __init__(self):
        # MongoDB connection
        self.client = MongoClient(os.getenv("MONGODB_URI"))
        self.db = self.client["hackathon_twin"]
        self.users_collection = self.db["users"]
        self.matches_collection = self.db["matches"]  # Store match history
        
        # Initialize components
        self.skill_extractor = SkillExtractor()
        self.matcher = UserMatcher(self.users_collection)
        self.notifier = MatchmakingNotifier()
    
    def process_resume_and_update_skills(self, user_id, resume_file_path):
        """Process uploaded resume and update user skills"""
        try:
            print(f"🔍 Processing resume for user_id: {user_id}")
            
            # Convert string ID to ObjectId if needed
            if isinstance(user_id, str):
                try:
                    user_id = ObjectId(user_id)
                except Exception as e:
                    print(f"❌ Invalid user_id format: {user_id}")
                    return {"success": False, "message": f"Invalid user ID format: {user_id}"}
            
            # Extract text from resume
            print(f"📄 Extracting text from: {resume_file_path}")
            resume_text = self.skill_extractor.extract_text_from_file(resume_file_path)
            
            if not resume_text:
                print("❌ No text extracted from resume")
                return {"success": False, "message": "Could not extract text from resume"}
            
            print(f"✅ Extracted {len(resume_text)} characters from resume")
            
            # Extract skills using AI
            print("🤖 Extracting skills with AI...")
            extracted_skills = self.skill_extractor.extract_skills_with_ai(resume_text)
            
            if not extracted_skills:
                print("❌ No skills extracted by AI")
                return {"success": False, "message": "No skills could be extracted from resume"}
            
            print(f"✅ AI extracted {len(extracted_skills)} skills: {extracted_skills}")
            
            # Get current user data
            user = self.users_collection.find_one({"_id": user_id})
            if not user:
                print(f"❌ User not found with ID: {user_id}")
                return {"success": False, "message": "User not found"}
            
            print(f"👤 Found user: {user.get('name', 'Unknown')}")
            
            # Merge with existing skills (avoid duplicates)
            existing_skills = user.get('keywords', [])
            print(f"📝 Existing skills: {existing_skills}")
            
            # Combine and deduplicate skills (case-insensitive)
            all_skills = existing_skills + extracted_skills
            seen_lower = set()
            updated_skills = []
            
            for skill in all_skills:
                skill_lower = skill.lower().strip()
                if skill_lower not in seen_lower and skill.strip():
                    seen_lower.add(skill_lower)
                    updated_skills.append(skill.strip())
            
            print(f"🔄 Updated skills: {updated_skills}")
            
            # Update user in database
            update_result = self.users_collection.update_one(
                {"_id": user_id},
                {
                    "$set": {
                        "keywords": updated_skills,
                        "resume_processed": True,
                        "resume_processed_date": datetime.now()
                    }
                }
            )
            
            if update_result.modified_count > 0:
                print(f"✅ Successfully updated user skills in database")
            else:
                print(f"⚠️ No database changes made (maybe skills were the same)")
            
            return {
                "success": True,
                "message": f"Successfully extracted {len(extracted_skills)} skills",
                "extracted_skills": extracted_skills,
                "total_skills": len(updated_skills)
            }
            
        except Exception as e:
            print(f"❌ Error processing resume: {e}")
            return {"success": False, "message": f"Error processing resume: {str(e)}"}
    
    def find_and_notify_matches(self, user_id, similarity_threshold=0.1):
        """Find matches for user and send ONE CONSOLIDATED notification - MUCH more efficient!"""
        try:
            print(f"🔍 Finding matches for user_id: {user_id}")
            
            # Convert string ID to ObjectId if needed
            if isinstance(user_id, str):
                try:
                    user_id = ObjectId(user_id)
                except Exception as e:
                    print(f"❌ Invalid user_id format: {user_id}")
                    return {"success": False, "message": f"Invalid user ID format: {user_id}"}
            
            user = self.users_collection.find_one({"_id": user_id})
            if not user:
                print(f"❌ User not found with ID: {user_id}")
                return {"success": False, "message": "User not found"}
            
            print(f"👤 Finding matches for: {user.get('name', 'Unknown')} with skills: {user.get('keywords', [])}")
            
            # Find similar users
            similar_users = self.matcher.find_similar_users(user_id, similarity_threshold)
            
            if not similar_users:
                return {
                    "success": True,
                    "message": "No matches found above similarity threshold",
                    "matches_found": 0,
                    "notifications_sent": 0
                }
            
            print(f"🎉 Found {len(similar_users)} total matches")
            
            # CONSOLIDATED APPROACH: Generate ONE email with ALL matches
            email_content = self.notifier.generate_consolidated_match_email(user, similar_users)
            
            notifications_sent = 0
            if email_content and self.notifier.send_consolidated_match_notification(
                user['email'], email_content, len(similar_users)
            ):
                notifications_sent = 1  # Only ONE email sent instead of N emails!
                print(f"✅ Sent consolidated email with {len(similar_users)} matches to {user['name']}")
            
            # Record matches in database (but don't duplicate notifications)
            match_records = []
            for match in similar_users:
                matched_user = match['user']
                similarity = match['similarity']
                common_skills = match['common_skills']
                
                match_record = {
                    "user1_id": user_id,
                    "user2_id": matched_user['_id'],
                    "similarity_score": similarity,
                    "common_skills": common_skills,
                    "match_date": datetime.now(),
                    "consolidated_notification_sent": True
                }
                match_records.append(match_record)
            
            # Store match records
            if match_records:
                self.matches_collection.insert_many(match_records)
                print(f"📝 Stored {len(match_records)} match records in database")
            
            return {
                "success": True,
                "message": f"Found {len(similar_users)} matches, sent 1 consolidated notification",
                "matches_found": len(similar_users),
                "notifications_sent": notifications_sent,
                "api_calls_saved": len(similar_users) - 1  # This many API calls saved!
            }
            
        except Exception as e:
            print(f"❌ Error in find_and_notify_matches: {e}")
            return {
                "success": False,
                "message": f"Error finding matches: {str(e)}",
                "matches_found": 0,
                "notifications_sent": 0
            }
    
    def get_user_matches(self, user_id):
        """Get match history for a user"""
        try:
            matches = list(self.matches_collection.find({
                "$or": [
                    {"user1_id": user_id},
                    {"user2_id": user_id}
                ]
            }).sort("match_date", -1))
            
            return {"success": True, "matches": matches}
        except Exception as e:
            print(f"❌ Error getting user matches: {e}")
            return {"success": False, "message": str(e)}

# Usage example and testing
if __name__ == "__main__":
    # Initialize the matchmaking system
    matchmaker = MatchmakingSystem()
    
    print("🚀 HackTwin Matchmaking System initialized!")
    print("Ready to process resumes and find teammate matches!")
