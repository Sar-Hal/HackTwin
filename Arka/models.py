from pydantic import BaseModel
from typing import List, Optional

class Skill(BaseModel):
    name: str
    level: int  # 1-5

class Participant(BaseModel):
    discord_id: str
    username: str
    email: Optional[str]
    skills: List[Skill]
    interests: List[str]
    looking_for_team: bool = True
    team_id: Optional[str]
    onboarding_complete: bool = False

class Team(BaseModel):
    name: str
    members: List[str]  # Discord IDs
    required_skills: List[str]
    project_idea: Optional[str]