import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import CEODashboard from './pages/CEODashboard';
import './App.css';

// Simple authentication wrapper
const ProtectedRoute = ({ children, isAuthenticated }) => {
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

function App() {
  // Using localStorage to persist login state simply
  const [isAuthenticated, setIsAuthenticated] = useState(
    localStorage.getItem('isAuthenticated') === 'true'
  );

  const handleLogin = () => {
    setIsAuthenticated(true);
    localStorage.setItem('isAuthenticated', 'true');
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    localStorage.removeItem('isAuthenticated');
  };

  return (
    <Router>
      <div className="app-container">
        <Routes>
          <Route path="/login" element={
            isAuthenticated ? <Navigate to="/ceo" replace /> : <Login onLogin={handleLogin} />
          } />
          
          <Route path="/ceo" element={
            <ProtectedRoute isAuthenticated={isAuthenticated}>
              <CEODashboard onLogout={handleLogout} />
            </ProtectedRoute>
          } />
          
          {/* Redirect all other routes to CEO Dashboard if authenticated, else login */}
          <Route path="*" element={
            <Navigate to={isAuthenticated ? "/ceo" : "/login"} replace />
          } />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
