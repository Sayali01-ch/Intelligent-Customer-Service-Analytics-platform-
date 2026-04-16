import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Dashboard from './components/Dashboard';
import Login from './components/Login';
import Register from './components/Register';
import Analysis from './components/Analysis';
import History from './components/History';
import Navbar from './components/Navbar';

function App() {
  const [isAuthenticated, setIsAuthenticated] = React.useState(false);
  const [user, setUser] = React.useState(null);

  React.useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
      // You might want to validate the token here
    }
  }, []);

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {isAuthenticated && <Navbar user={user} setIsAuthenticated={setIsAuthenticated} />}
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={
              isAuthenticated ? <Dashboard /> : <Login setIsAuthenticated={setIsAuthenticated} setUser={setUser} />
            } />
            <Route path="/register" element={<Register />} />
            <Route path="/analysis" element={isAuthenticated ? <Analysis /> : <Login setIsAuthenticated={setIsAuthenticated} setUser={setUser} />} />
            <Route path="/history" element={isAuthenticated ? <History /> : <Login setIsAuthenticated={setIsAuthenticated} setUser={setUser} />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;