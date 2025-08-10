import React, { useState, useEffect } from 'react';

const AdminPage = () => {
  const [users, setUsers] = useState([]);
  const [problems, setProblems] = useState([]);
  
  // Mock data (replace with actual API calls later)
  const mockUsers = [
    { id: 1, name: "John Doe", team: "Tech Wizards", role: "Team Lead" },
    { id: 2, name: "Jane Smith", team: "Tech Wizards", role: "Member" },
    { id: 3, name: "Bob Solo", team: null, role: "Solo Participant" },
  ];

  const mockProblems = [
    {
      id: 1,
      title: "AI Healthcare Assistant",
      description: "Create an AI-powered healthcare assistant that can help patients...",
      difficulty: "Hard",
      category: "Healthcare"
    },
    {
      id: 2,
      title: "Smart Education Platform",
      description: "Develop an intelligent education platform that adapts to student learning...",
      difficulty: "Medium",
      category: "Education"
    }
  ];

  useEffect(() => {
    // Simulating API calls
    setUsers(mockUsers);
    setProblems(mockProblems);
  }, []);

  return (
    <div className="admin-page">
      <h1>Admin Dashboard</h1>
      
      <section className="users-section">
        <h2>Registered Users</h2>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Team</th>
              <th>Role</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map(user => (
              <tr key={user.id}>
                <td>{user.name}</td>
                <td>{user.team || "Solo"}</td>
                <td>{user.role}</td>
                <td>
                  <button>Edit</button>
                  <button>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section className="problems-section">
        <h2>Problem Statements</h2>
        <button>Add New Problem</button>
        {problems.map(problem => (
          <div key={problem.id} className="problem-card">
            <h3>{problem.title}</h3>
            <p><strong>Category:</strong> {problem.category}</p>
            <p><strong>Difficulty:</strong> {problem.difficulty}</p>
            <p>{problem.description}</p>
            <div className="actions">
              <button>Edit</button>
              <button>Delete</button>
            </div>
          </div>
        ))}
      </section>
    </div>
  );
};

export default AdminPage;
