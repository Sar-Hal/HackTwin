import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import './App.css';

// Import components
import LoginPage from './components/LoginPage';
import HomePage from './components/HomePage';
import AdminPage from './components/AdminPage';
import ProblemStatements from './components/ProblemStatements';
import TeamDetails from './components/TeamDetails';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/admin" element={<AdminPage />} />
          <Route path="/problems" element={<ProblemStatements />} />
          <Route path="/teams" element={<TeamDetails />} />
        </Routes>
      </div>
  );
}

export default App;
