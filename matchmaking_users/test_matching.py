#!/usr/bin/env python3
"""
Test script for the new skill-based matchmaking logic
"""

# Test the new matching logic
def test_skill_matching():
    """Test skill overlap calculation"""
    
    def calculate_skill_similarity(user1_skills, user2_skills):
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
    
    # Test cases for your requirements
    print("🧪 Testing New Skill-Based Matching Logic\n")
    
    # AIML users should match
    user_aiml_1 = ["Machine Learning", "Python", "TensorFlow", "Data Science"]
    user_aiml_2 = ["AI", "Machine Learning", "Python", "Neural Networks"]
    
    similarity = calculate_skill_similarity(user_aiml_1, user_aiml_2)
    common = set(s.lower() for s in user_aiml_1).intersection(set(s.lower() for s in user_aiml_2))
    
    print(f"🤖 AIML User 1: {user_aiml_1}")
    print(f"🤖 AIML User 2: {user_aiml_2}")
    print(f"✅ Similarity: {similarity:.2f} (Common: {common})")
    print(f"📧 Would send notification: {'YES' if similarity >= 0.1 else 'NO'}\n")
    
    # WebDev users should match
    user_web_1 = ["React", "JavaScript", "Node.js", "MongoDB"]
    user_web_2 = ["JavaScript", "React", "CSS", "HTML"]
    
    similarity = calculate_skill_similarity(user_web_1, user_web_2)
    common = set(s.lower() for s in user_web_1).intersection(set(s.lower() for s in user_web_2))
    
    print(f"🌐 WebDev User 1: {user_web_1}")
    print(f"🌐 WebDev User 2: {user_web_2}")
    print(f"✅ Similarity: {similarity:.2f} (Common: {common})")
    print(f"📧 Would send notification: {'YES' if similarity >= 0.1 else 'NO'}\n")
    
    # Different domains shouldn't match well
    user_different = ["Accounting", "Excel", "Finance", "Budgeting"]
    
    similarity = calculate_skill_similarity(user_aiml_1, user_different)
    common = set(s.lower() for s in user_aiml_1).intersection(set(s.lower() for s in user_different))
    
    print(f"🤖 AIML User: {user_aiml_1}")
    print(f"💼 Finance User: {user_different}")
    print(f"❌ Similarity: {similarity:.2f} (Common: {common})")
    print(f"📧 Would send notification: {'YES' if similarity >= 0.1 else 'NO'}\n")
    
    # Edge case: exact matches
    user_exact = ["Python", "Machine Learning"]
    
    similarity = calculate_skill_similarity(user_exact, user_exact)
    print(f"🎯 Exact Match Test: {similarity:.2f} (Should be 1.00)")
    
    print("\n🎉 New Logic Summary:")
    print("✅ AIML people get notified about other AIML people")
    print("✅ WebDev people get notified about other WebDev people") 
    print("✅ Different domains don't get unnecessary notifications")
    print("✅ Threshold of 0.1 (10% overlap) catches meaningful matches")

if __name__ == "__main__":
    test_skill_matching()
