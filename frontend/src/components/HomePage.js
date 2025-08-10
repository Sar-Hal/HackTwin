import React from 'react';
import { Link } from 'react-router-dom';
import { useLocation } from 'react-router-dom';

// Static fallback data
const problems = [
  { id: 1, title: 'AI for Social Good', details: 'Build an AI solution to address a social issue.' },
  { id: 2, title: 'Fintech Innovation', details: 'Create a fintech app for seamless payments.' },
];
const hackathonTiming = {
  start: '2025-08-15T09:00:00',
  end: '2025-08-16T18:00:00',
};

export default function HomePage() {
  const location = useLocation();
  const { username = 'Guest', role = 'user' } = location.state || {};
  // For demo, assume solo if username ends with '1', else team
  const isSolo = username.endsWith('1');
  return (
    <div className="home-container">
      <h2>Welcome, {username} ({role})</h2>
      <div>Team Status: {isSolo ? 'Solo' : 'Team'}</div>
      <h3>Problem Statements</h3>
      <ul>
        {problems.map(p => (
          <li key={p.id}>
            <strong>{p.title}</strong>: {p.details}
          </li>
        ))}
      </ul>
      <h3>Hackathon Timing</h3>
      <div>Start: {new Date(hackathonTiming.start).toLocaleString()}</div>
      <div>End: {new Date(hackathonTiming.end).toLocaleString()}</div>
    </div>
  );
} 