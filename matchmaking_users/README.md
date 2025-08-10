# 🤝 HackTwin Matchmaking Users Feature

Advanced AI-powered teammate matching system for hackathon participants based on skills extracted from resumes.

## 🌟 Features

### 1. **Resume Processing & Skill Extraction**
- **Multi-format Support**: PDF, DOCX, and TXT files
- **AI-Powered Extraction**: Uses Gemini AI to intelligently extract technical skills
- **Fallback System**: Pattern-matching backup if AI fails
- **Skill Merging**: Combines with existing user skills (no duplicates)

### 2. **Advanced Matching Algorithm**
- **TF-IDF Vectorization**: Converts skills to numerical vectors
- **Cosine Similarity**: Calculates precise similarity scores
- **Configurable Threshold**: Adjustable minimum similarity requirements
- **Common Skills Detection**: Identifies shared expertise areas

### 3. **Automated Notifications**
- **Bidirectional Emails**: Both users get notified about the match
- **Personalized Content**: AI-generated emails with match details
- **Discord Integration**: Includes Discord invite for team formation
- **Match History**: Tracks all connections in database

### 4. **Web Interface**
- **Interactive Dashboard**: Real-time statistics and user management
- **Bulk Operations**: Process multiple users simultaneously
- **Match Visualization**: View user connections and compatibility scores
- **Resume Upload**: Drag-and-drop file handling

## 📁 File Structure

```
matchmaking_users/
├── __init__.py           # Package initialization
├── matchmaker.py         # Core matching system
├── routes.py            # Flask route handlers
├── demo.py              # Testing and demonstration script
├── requirements.txt     # Additional dependencies
└── README.md           # This documentation
```

## 🔧 Core Components

### `SkillExtractor`
Extracts skills from resume documents using AI and pattern matching.

```python
extractor = SkillExtractor()
skills = extractor.extract_skills_with_ai(resume_text)
```

### `UserMatcher`
Calculates similarity between users based on their skills.

```python
matcher = UserMatcher(users_collection)
matches = matcher.find_similar_users(user_id, threshold=0.3)
```

### `MatchmakingNotifier`
Sends personalized email notifications about matches.

```python
notifier = MatchmakingNotifier()
notifier.send_match_notification(user_email, content, matched_user)
```

### `MatchmakingSystem`
Main coordinator that orchestrates the entire process.

```python
system = MatchmakingSystem()
result = system.process_resume_and_update_skills(user_id, file_path)
```

## 🚀 API Endpoints

### `/matchmaking`
**GET** - Main matchmaking dashboard with statistics and user management

### `/matchmaking/upload-resume`
**POST** - Upload and process resume file
```json
{
  "user_id": "string",
  "resume": "file",
  "auto_match": "boolean"
}
```

### `/matchmaking/find-matches`
**POST** - Find matches for specific user
```json
{
  "user_id": "string",
  "similarity_threshold": "float"
}
```

### `/matchmaking/user-matches/<user_id>`
**GET** - Get match history for user

### `/matchmaking/bulk-match`
**POST** - Run matchmaking for all users with resumes

### `/api/matchmaking/stats`
**GET** - Get matchmaking system statistics

## 🎯 Usage Examples

### 1. Upload Resume and Auto-Match
```javascript
const formData = new FormData();
formData.append('user_id', 'user123');
formData.append('resume', fileInput.files[0]);
formData.append('auto_match', 'true');

fetch('/matchmaking/upload-resume', {
    method: 'POST',
    body: formData
});
```

### 2. Find Matches Manually
```javascript
fetch('/matchmaking/find-matches', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        user_id: 'user123',
        similarity_threshold: 0.4
    })
});
```

### 3. Get User Match History
```javascript
fetch('/matchmaking/user-matches/user123')
    .then(response => response.json())
    .then(data => console.log(data.matches));
```

## 📊 Database Schema

### Users Collection (Enhanced)
```json
{
  "_id": "ObjectId",
  "name": "string",
  "email": "string",
  "job_title": "string",
  "keywords": ["skill1", "skill2", ...],
  "resume_processed": "boolean",
  "resume_processed_date": "datetime"
}
```

### Matches Collection (New)
```json
{
  "_id": "ObjectId",
  "user1_id": "ObjectId",
  "user2_id": "ObjectId",
  "similarity_score": "float",
  "common_skills": ["skill1", "skill2", ...],
  "match_date": "datetime",
  "notifications_sent": "boolean"
}
```

## 🔍 Matching Algorithm Details

### 1. **Skill Extraction Process**
1. Extract text from uploaded resume
2. Send text to Gemini AI with structured prompt
3. Parse and clean extracted skills
4. Merge with existing user skills
5. Update user profile in database

### 2. **Similarity Calculation**
1. Convert skill lists to text strings
2. Create TF-IDF vectors using scikit-learn
3. Calculate cosine similarity between vectors
4. Apply threshold filtering
5. Rank by similarity score

### 3. **Notification Process**
1. Generate personalized email content using AI
2. Include match details and common skills
3. Add Discord invite for team formation
4. Send to both matched users
5. Record match in database

## 🛡️ Error Handling

- **File Upload Validation**: Size limits, format checking
- **AI Service Fallbacks**: Pattern matching if Gemini fails
- **Database Resilience**: Connection error handling
- **Email Delivery**: SMTP failure recovery
- **User Input Sanitization**: Secure file handling

## 📈 Performance Considerations

- **File Size Limits**: 16MB maximum upload size
- **Batch Processing**: Efficient bulk operations
- **Database Indexing**: Optimized queries for matching
- **Caching**: Skill vectors cached for repeated comparisons
- **Async Operations**: Background processing for large datasets

## 🔒 Security Features

- **Secure File Upload**: Filename sanitization and validation
- **Input Validation**: All user inputs validated and sanitized
- **Database Security**: Parameterized queries prevent injection
- **Email Privacy**: User emails only used for notifications
- **File Cleanup**: Temporary files automatically removed

## 🎨 UI/UX Features

### Dashboard Statistics
- Total users and processed resumes
- Match statistics and averages
- System status indicators
- Quick action buttons

### User Management
- Upload resumes for any user
- View individual match histories
- Run matchmaking for specific users
- Bulk operations for all users

### Interactive Elements
- Real-time notifications
- Progress indicators
- Error message handling
- Responsive design

## 🧪 Testing

Run the demo script to test all components:

```bash
cd matchmaking_users
python demo.py
```

The demo will test:
- Skill extraction from sample resume
- Similarity calculations
- Database connectivity
- Full system integration

## 🔧 Configuration

### Environment Variables Required
```env
MONGODB_URI=mongodb://localhost:27017/
GEMINI_API_KEY=your_gemini_api_key
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
FLASK_SECRET_KEY=your_secret_key
```

### Similarity Threshold Tuning
- **0.1-0.2**: Very permissive matching
- **0.3-0.4**: Balanced matching (recommended)
- **0.5-0.7**: Strict matching
- **0.8+**: Very strict matching

## 🚀 Integration with Main App

The matchmaking feature integrates seamlessly with the main HackTwin application:

1. **Navigation**: Added to sidebar and dashboard
2. **Database**: Uses existing MongoDB connection
3. **Authentication**: Leverages existing user system
4. **UI**: Consistent with existing design
5. **APIs**: RESTful endpoints for frontend integration

## 📝 Future Enhancements

- **Team Size Preferences**: Match based on desired team size
- **Timezone Matching**: Consider geographical locations
- **Experience Level Matching**: Junior/Senior compatibility
- **Project Type Preferences**: Match based on project interests
- **Real-time Chat**: Integrated messaging system
- **Advanced Analytics**: Match success tracking
- **ML Model Training**: Improve matching with historical data

## 🤝 Contributing

To add new features to the matchmaking system:

1. Create new functions in `matchmaker.py`
2. Add corresponding routes in `routes.py`
3. Update the web interface in `templates/matchmaking.html`
4. Add tests to `demo.py`
5. Update this documentation

## 📞 Support

For issues or questions about the matchmaking system:
- Check the demo script output for debugging
- Verify all environment variables are set
- Ensure all dependencies are installed
- Check MongoDB connection and collections
