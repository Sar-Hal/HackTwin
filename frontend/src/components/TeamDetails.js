import React, { useState } from 'react';

const TeamDetails = () => {
  const [teams, setTeams] = useState([
    {
      id: 1,
      name: "Tech Wizards",
      members: [
        { id: 1, name: "John Doe", role: "Team Lead", skills: ["Python", "AI/ML", "React"] },
        { id: 2, name: "Jane Smith", role: "Frontend Developer", skills: ["React", "TypeScript", "UI/UX"] },
        { id: 3, name: "Mike Johnson", role: "Backend Developer", skills: ["Node.js", "MongoDB", "AWS"] }
      ],
      problem: "AI Healthcare Assistant",
      progress: "In Progress"
    }
  ]);

  const [soloParticipants, setSoloParticipants] = useState([
    {
      id: 1,
      name: "Alice Cooper",
      skills: ["Python", "Data Science", "TensorFlow"],
      problem: "Smart Education Platform",
      progress: "Started"
    },
    {
      id: 2,
      name: "Bob Wilson",
      skills: ["Java", "Spring Boot", "MySQL"],
      problem: "Sustainable City Planner",
      progress: "Planning"
    }
  ]);

  return (
    <div className="team-details">
      <h1>Team & Participant Details</h1>

      <section className="teams-section">
        <h2>Teams</h2>
        {teams.map(team => (
          <div key={team.id} className="team-card">
            <h3>{team.name}</h3>
            <p><strong>Problem Statement:</strong> {team.problem}</p>
            <p><strong>Progress:</strong> {team.progress}</p>
            
            <div className="members-list">
              <h4>Team Members</h4>
              <div className="members-grid">
                {team.members.map(member => (
                  <div key={member.id} className="member-card">
                    <h5>{member.name}</h5>
                    <p><strong>Role:</strong> {member.role}</p>
                    <div className="skills">
                      <strong>Skills:</strong>
                      <div className="skill-tags">
                        {member.skills.map((skill, index) => (
                          <span key={index} className="skill-tag">{skill}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </section>

      <section className="solo-section">
        <h2>Solo Participants</h2>
        <div className="solo-grid">
          {soloParticipants.map(participant => (
            <div key={participant.id} className="solo-card">
              <h3>{participant.name}</h3>
              <p><strong>Problem Statement:</strong> {participant.problem}</p>
              <p><strong>Progress:</strong> {participant.progress}</p>
              <div className="skills">
                <strong>Skills:</strong>
                <div className="skill-tags">
                  {participant.skills.map((skill, index) => (
                    <span key={index} className="skill-tag">{skill}</span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default TeamDetails;
