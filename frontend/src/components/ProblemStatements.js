import React from 'react';

const ProblemStatements = () => {
  // Static problem statement data
  const problems = [
    {
      id: 1,
      title: "AI Healthcare Assistant",
      description: "Create an AI-powered healthcare assistant that can help patients with basic health queries, appointment scheduling, and medication reminders.",
      difficulty: "Hard",
      category: "Healthcare",
      requirements: [
        "Must use advanced NLP for understanding patient queries",
        "Real-time response capabilities",
        "HIPAA compliance considerations",
        "Multi-language support"
      ],
      resources: [
        "Access to medical terminology dataset",
        "Healthcare APIs documentation",
        "Cloud credits worth $1000"
      ]
    },
    {
      id: 2,
      title: "Smart Education Platform",
      description: "Develop an intelligent education platform that adapts to student learning patterns and provides personalized learning paths.",
      difficulty: "Medium",
      category: "Education",
      requirements: [
        "AI-driven learning path generation",
        "Progress tracking and analytics",
        "Interactive learning modules",
        "Support for multiple subjects"
      ],
      resources: [
        "Education content APIs",
        "ML model templates",
        "Cloud hosting credits"
      ]
    },
    {
      id: 3,
      title: "Sustainable City Planner",
      description: "Create an AI tool that helps city planners optimize urban development for sustainability and efficiency.",
      difficulty: "Medium",
      category: "Smart Cities",
      requirements: [
        "Data visualization capabilities",
        "Integration with GIS systems",
        "Resource optimization algorithms",
        "Climate impact analysis"
      ],
      resources: [
        "City planning datasets",
        "Environmental impact APIs",
        "Visualization libraries"
      ]
    }
  ];

  return (
    <div className="problem-statements">
      <h1>Hackathon Problem Statements</h1>
      <div className="problems-grid">
        {problems.map(problem => (
          <div key={problem.id} className="problem-card">
            <div className="card-header">
              <h2>{problem.title}</h2>
              <span className={`difficulty ${problem.difficulty.toLowerCase()}`}>
                {problem.difficulty}
              </span>
            </div>
            <div className="card-category">{problem.category}</div>
            <p className="description">{problem.description}</p>
            <div className="requirements">
              <h3>Requirements</h3>
              <ul>
                {problem.requirements.map((req, index) => (
                  <li key={index}>{req}</li>
                ))}
              </ul>
            </div>
            <div className="resources">
              <h3>Resources Provided</h3>
              <ul>
                {problem.resources.map((resource, index) => (
                  <li key={index}>{resource}</li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProblemStatements;
