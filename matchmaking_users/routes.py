"""
Flask routes for Matchmaking Users feature
Integration with main HackTwin application
"""

from flask import request, jsonify, render_template, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import tempfile

# Import the matchmaking system
from .matchmaker import MatchmakingSystem

class MatchmakingRoutes:
    """Flask routes for matchmaking functionality"""
    
    def __init__(self, app, users_collection):
        self.app = app
        self.users_collection = users_collection
        self.matchmaker = MatchmakingSystem()
        self.setup_routes()
        
        # Configure upload settings
        self.UPLOAD_FOLDER = 'uploads/resumes'
        self.ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
        self.MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
        
        # Create upload directory if it doesn't exist
        os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)
    
    def allowed_file(self, filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS
    
    def setup_routes(self):
        """Setup all matchmaking routes"""
        
        @self.app.route('/matchmaking')
        def matchmaking_dashboard():
            """Matchmaking dashboard page"""
            try:
                # Get all users with their match counts
                users = list(self.users_collection.find())
                
                # Get match statistics
                total_matches = 0
                users_with_resumes = 0
                users_with_skills = 0
                
                for user in users:
                    if user.get('resume_processed', False):
                        users_with_resumes += 1
                    
                    if user.get('keywords') and len(user['keywords']) > 0:
                        users_with_skills += 1
                    
                    # Get match count for this user
                    match_result = self.matchmaker.get_user_matches(user['_id'])
                    if match_result['success']:
                        user['match_count'] = len(match_result['matches'])
                        total_matches += user['match_count']
                    else:
                        user['match_count'] = 0
                
                stats = {
                    'total_users': len(users),
                    'users_with_resumes': users_with_resumes,
                    'users_with_skills': users_with_skills,
                    'total_matches': total_matches // 2,  # Divide by 2 as each match is counted twice
                    'avg_matches_per_user': (total_matches / len(users)) if users else 0
                }
                
                return render_template('matchmaking.html', users=users, stats=stats)
                
            except Exception as e:
                flash(f'Error loading matchmaking dashboard: {str(e)}', 'error')
                return redirect(url_for('dashboard'))
        
        @self.app.route('/matchmaking/add-user', methods=['POST'])
        def add_user_with_skills():
            """Add new user directly with skills (no resume required)"""
            try:
                data = request.json
                
                # Validate required fields
                required_fields = ['name', 'email', 'job_title']
                for field in required_fields:
                    if not data.get(field):
                        return jsonify({'success': False, 'message': f'{field} is required'})
                
                # Check if user already exists
                existing_user = self.users_collection.find_one({'email': data['email']})
                if existing_user:
                    return jsonify({'success': False, 'message': 'User with this email already exists'})
                
                # Create new user
                new_user = {
                    'name': data['name'],
                    'email': data['email'],
                    'job_title': data['job_title'],
                    'keywords': data.get('skills', []),  # Skills can be empty initially
                    'resume_processed': False,  # No resume uploaded yet
                    'created_date': datetime.now(),
                    'source': 'manual_entry'  # Mark as manually added
                }
                
                # Insert user
                result = self.users_collection.insert_one(new_user)
                user_id = result.inserted_id
                
                # Auto-trigger matchmaking if user has skills
                auto_match = data.get('auto_match', True)
                match_result = None
                
                if auto_match and new_user['keywords']:
                    match_result = self.matchmaker.find_and_notify_matches(str(user_id))
                
                return jsonify({
                    'success': True,
                    'message': f'User {data["name"]} added successfully',
                    'user_id': str(user_id),
                    'skills_count': len(new_user['keywords']),
                    'matchmaking': match_result
                })
                
            except Exception as e:
                return jsonify({'success': False, 'message': f'Error adding user: {str(e)}'})
        
        @self.app.route('/matchmaking/upload-resume', methods=['POST'])
        def upload_resume():
            """Handle resume upload and skill extraction"""
            try:
                # Check if user_id is provided
                user_id = request.form.get('user_id')
                if not user_id:
                    return jsonify({'success': False, 'message': 'User ID is required'})
                
                # Check if file is provided
                if 'resume' not in request.files:
                    return jsonify({'success': False, 'message': 'No file uploaded'})
                
                file = request.files['resume']
                
                if file.filename == '':
                    return jsonify({'success': False, 'message': 'No file selected'})
                
                if not self.allowed_file(file.filename):
                    return jsonify({
                        'success': False, 
                        'message': 'Invalid file type. Please upload PDF, DOCX, or TXT files.'
                    })
                
                # Save file temporarily
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                unique_filename = f"{user_id}_{timestamp}_{filename}"
                file_path = os.path.join(self.UPLOAD_FOLDER, unique_filename)
                
                file.save(file_path)
                
                try:
                    # Process resume and extract skills
                    result = self.matchmaker.process_resume_and_update_skills(user_id, file_path)
                    
                    # Clean up uploaded file
                    os.remove(file_path)
                    
                    if result['success']:
                        # Auto-trigger matchmaking after successful skill extraction
                        auto_match = request.form.get('auto_match', 'true').lower() == 'true'
                        
                        if auto_match:
                            match_result = self.matchmaker.find_and_notify_matches(user_id)
                            result['matchmaking'] = match_result
                    
                    return jsonify(result)
                    
                except Exception as e:
                    # Clean up file on error
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    raise e
                    
            except Exception as e:
                return jsonify({'success': False, 'message': f'Error processing resume: {str(e)}'})
        
        @self.app.route('/matchmaking/find-matches', methods=['POST'])
        def find_matches():
            """Find matches for a specific user"""
            try:
                user_id = request.json.get('user_id')
                similarity_threshold = float(request.json.get('similarity_threshold', 0.1))  # Lower threshold for skill overlap
                
                if not user_id:
                    return jsonify({'success': False, 'message': 'User ID is required'})
                
                result = self.matchmaker.find_and_notify_matches(user_id, similarity_threshold)
                return jsonify(result)
                
            except Exception as e:
                return jsonify({'success': False, 'message': f'Error finding matches: {str(e)}'})
        
        @self.app.route('/matchmaking/user-matches/<user_id>')
        def get_user_matches(user_id):
            """Get match history for a specific user"""
            try:
                result = self.matchmaker.get_user_matches(user_id)
                
                if result['success']:
                    # Enhance match data with user details
                    enhanced_matches = []
                    for match in result['matches']:
                        # Determine which user is the "other" user
                        other_user_id = match['user2_id'] if match['user1_id'] == user_id else match['user1_id']
                        
                        # Get other user details
                        other_user = self.users_collection.find_one({'_id': other_user_id})
                        
                        if other_user:
                            enhanced_match = {
                                'match_id': str(match['_id']),
                                'other_user': {
                                    'id': str(other_user['_id']),
                                    'name': other_user['name'],
                                    'email': other_user['email'],
                                    'job_title': other_user.get('job_title', 'N/A')
                                },
                                'similarity_score': match['similarity_score'],
                                'common_skills': match['common_skills'],
                                'match_date': match['match_date'].isoformat(),
                                'notifications_sent': match.get('notifications_sent', False)
                            }
                            enhanced_matches.append(enhanced_match)
                    
                    result['matches'] = enhanced_matches
                
                return jsonify(result)
                
            except Exception as e:
                return jsonify({'success': False, 'message': f'Error getting matches: {str(e)}'})
        
        @self.app.route('/matchmaking/bulk-match', methods=['POST'])
        def bulk_matchmaking():
            """Run matchmaking for all users with skills (resume processed or manually added)"""
            try:
                # Get all users who have skills (either from resume or manual entry)
                users_with_skills = list(self.users_collection.find({
                    'keywords': {'$exists': True, '$ne': []}
                }))
                
                if not users_with_skills:
                    return jsonify({
                        'success': False, 
                        'message': 'No users with skills found'
                    })
                
                total_matches = 0
                total_notifications = 0
                processed_users = 0
                
                for user in users_with_skills:
                    try:
                        result = self.matchmaker.find_and_notify_matches(user['_id'])
                        if result['success']:
                            total_matches += result.get('matches_found', 0)
                            total_notifications += result.get('notifications_sent', 0)
                            processed_users += 1
                    except Exception as e:
                        print(f"❌ Error processing user {user['name']}: {e}")
                        continue
                
                return jsonify({
                    'success': True,
                    'message': f'Bulk matchmaking completed',
                    'processed_users': processed_users,
                    'total_matches': total_matches,
                    'total_notifications': total_notifications
                })
                
            except Exception as e:
                return jsonify({'success': False, 'message': f'Error in bulk matchmaking: {str(e)}'})
        
        @self.app.route('/api/matchmaking/stats')
        def matchmaking_stats():
            """Get matchmaking statistics"""
            try:
                # Count users with resumes
                users_with_resumes = self.users_collection.count_documents({
                    'resume_processed': True
                })
                
                # Count total matches
                total_matches = self.matchmaker.matches_collection.count_documents({})
                
                # Get recent matches
                recent_matches = list(self.matchmaker.matches_collection.find().sort('match_date', -1).limit(5))
                
                # Calculate average similarity
                pipeline = [
                    {'$group': {
                        '_id': None,
                        'avg_similarity': {'$avg': '$similarity_score'},
                        'max_similarity': {'$max': '$similarity_score'},
                        'min_similarity': {'$min': '$similarity_score'}
                    }}
                ]
                similarity_stats = list(self.matchmaker.matches_collection.aggregate(pipeline))
                
                stats = {
                    'users_with_resumes': users_with_resumes,
                    'total_users': self.users_collection.count_documents({}),
                    'total_matches': total_matches,
                    'recent_matches': len(recent_matches),
                    'similarity_stats': similarity_stats[0] if similarity_stats else None
                }
                
                return jsonify({'success': True, 'stats': stats})
                
            except Exception as e:
                return jsonify({'success': False, 'message': f'Error getting stats: {str(e)}'})

# Function to integrate with main app
def setup_matchmaking_routes(app, users_collection):
    """Setup matchmaking routes in the main Flask app"""
    matchmaking_routes = MatchmakingRoutes(app, users_collection)
    return matchmaking_routes
