"""
Demo script for HackTwin Matchmaking System
Test the matchmaking functionality with sample data
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

def create_sample_resume():
    """Create a sample resume file for testing"""
    sample_resume_content = """
    John Doe
    Senior Software Engineer
    
    TECHNICAL SKILLS:
    • Programming Languages: Python, JavaScript, TypeScript, Java
    • Web Frameworks: React, Django, Flask, Express.js
    • Databases: MongoDB, PostgreSQL, MySQL
    • Cloud Platforms: AWS, Docker, Kubernetes
    • Tools: Git, Jenkins, Linux, VS Code
    • AI/ML: Machine Learning, TensorFlow, PyTorch
    • Other: DevOps, Agile, Scrum, Leadership
    
    EXPERIENCE:
    Senior Software Engineer at TechCorp (2020-Present)
    • Led development of microservices architecture using Python and Docker
    • Implemented machine learning models for recommendation systems
    • Managed team of 5 developers using Agile methodologies
    
    Software Engineer at StartupXYZ (2018-2020)
    • Built full-stack web applications using React and Django
    • Optimized database queries reducing response time by 40%
    • Deployed applications on AWS using containerization
    
    EDUCATION:
    Master of Science in Computer Science
    Bachelor of Engineering in Software Engineering
    
    CERTIFICATIONS:
    • AWS Certified Solutions Architect
    • Certified Kubernetes Administrator
    """
    
    # Create uploads directory if it doesn't exist
    uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads', 'resumes')
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Write sample resume
    resume_path = os.path.join(uploads_dir, 'sample_resume.txt')
    with open(resume_path, 'w', encoding='utf-8') as f:
        f.write(sample_resume_content)
    
    return resume_path

def test_skill_extraction():
    """Test skill extraction functionality"""
    print("🧪 Testing Skill Extraction...")
    
    from matchmaker import SkillExtractor
    
    extractor = SkillExtractor()
    
    # Create sample resume
    resume_path = create_sample_resume()
    
    try:
        # Extract text from resume
        text = extractor.extract_text_from_file(resume_path)
        print(f"✅ Extracted {len(text)} characters from resume")
        
        # Extract skills
        skills = extractor.extract_skills_with_ai(text)
        print(f"✅ Extracted {len(skills)} skills:")
        for i, skill in enumerate(skills, 1):
            print(f"   {i}. {skill}")
        
        return skills
        
    except Exception as e:
        print(f"❌ Error in skill extraction: {e}")
        return []
    finally:
        # Clean up
        if os.path.exists(resume_path):
            os.remove(resume_path)

def test_user_matching():
    """Test user matching functionality"""
    print("\n🧪 Testing User Matching...")
    
    from matchmaker import UserMatcher
    from pymongo import MongoClient
    
    try:
        # Connect to MongoDB
        client = MongoClient(os.getenv("MONGODB_URI"))
        db = client["hackathon_twin"]
        users_collection = db["users"]
        
        matcher = UserMatcher(users_collection)
        
        # Test with sample skills
        user1_skills = ["Python", "Django", "React", "AWS", "Docker"]
        user2_skills = ["JavaScript", "React", "Node.js", "MongoDB", "Docker"]
        user3_skills = ["Java", "Spring", "Angular", "PostgreSQL", "Jenkins"]
        
        # Calculate similarities
        sim1_2 = matcher.calculate_skill_similarity(user1_skills, user2_skills)
        sim1_3 = matcher.calculate_skill_similarity(user1_skills, user3_skills)
        sim2_3 = matcher.calculate_skill_similarity(user2_skills, user3_skills)
        
        print(f"✅ Similarity User1-User2: {sim1_2:.3f}")
        print(f"✅ Similarity User1-User3: {sim1_3:.3f}")
        print(f"✅ Similarity User2-User3: {sim2_3:.3f}")
        
    except Exception as e:
        print(f"❌ Error in user matching: {e}")

def test_full_system():
    """Test the complete matchmaking system"""
    print("\n🚀 Testing Complete Matchmaking System...")
    
    from matchmaker import MatchmakingSystem
    
    try:
        system = MatchmakingSystem()
        print("✅ Matchmaking system initialized successfully")
        
        # Test with existing users
        from pymongo import MongoClient
        client = MongoClient(os.getenv("MONGODB_URI"))
        db = client["hackathon_twin"]
        users_collection = db["users"]
        
        user_count = users_collection.count_documents({})
        print(f"✅ Found {user_count} users in database")
        
        if user_count > 0:
            # Get first user
            first_user = users_collection.find_one()
            if first_user:
                print(f"✅ Testing with user: {first_user.get('name', 'Unknown')}")
                
                # Get user matches (without sending notifications for testing)
                matches = system.matcher.find_similar_users(first_user['_id'], threshold=0.1)
                print(f"✅ Found {len(matches)} potential matches")
                
                for i, match in enumerate(matches[:3], 1):
                    matched_user = match['user']
                    similarity = match['similarity']
                    common_skills = match['common_skills']
                    print(f"   {i}. {matched_user['name']} - Similarity: {similarity:.3f}")
                    print(f"      Common skills: {', '.join(common_skills)}")
        
    except Exception as e:
        print(f"❌ Error in full system test: {e}")

def main():
    """Run all tests"""
    print("🎯 HackTwin Matchmaking System Demo")
    print("=" * 50)
    
    # Test skill extraction
    extracted_skills = test_skill_extraction()
    
    # Test user matching
    test_user_matching()
    
    # Test full system
    test_full_system()
    
    print("\n✅ Demo completed!")
    print("\n📋 Next Steps:")
    print("1. Start the Flask app: python app.py")
    print("2. Go to http://localhost:5000/matchmaking")
    print("3. Upload resumes and test the matchmaking feature")

if __name__ == "__main__":
    main()
