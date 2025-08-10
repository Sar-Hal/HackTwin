"""
HackTwin Matchmaking Users Package
Advanced teammate matching system based on AI-extracted skills
"""

from .matchmaker import MatchmakingSystem, SkillExtractor, UserMatcher, MatchmakingNotifier
from .routes import setup_matchmaking_routes

__version__ = "1.0.0"
__author__ = "HackTwin Team"

__all__ = [
    'MatchmakingSystem',
    'SkillExtractor', 
    'UserMatcher',
    'MatchmakingNotifier',
    'setup_matchmaking_routes'
]
