import { useState, useEffect } from 'react';
import Login from './pages/Login';
import PatientHome from './pages/PatientHome';
import GameSelection from './pages/GameSelection';
import Reminders from './pages/Reminders';
import Progress from './pages/Progress';
import CaregiverDashboard from './pages/CaregiverDashboard';
import { api } from './services/api';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);
  const [currentPage, setCurrentPage] = useState('home');

  useEffect(() => {
    if (token) {
      api.getMe(token)
        .then(setUser)
        .catch(() => {
          localStorage.removeItem('token');
          setToken(null);
        });
    }
  }, [token]);

  const handleLogin = (newToken) => {
    setToken(newToken);
    setCurrentPage('home');
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    setCurrentPage('home');
  };

  if (!token || !user) {
    return <Login onLogin={handleLogin} />;
  }

  if (user.role === 'caregiver' || user.role === 'admin') {
    return <CaregiverDashboard onLogout={handleLogout} />;
  }

  switch (currentPage) {
    case 'games':
      return <GameSelection onBack={() => setCurrentPage('home')} />;
    case 'reminders':
      return <Reminders onBack={() => setCurrentPage('home')} />;
    case 'progress':
      return <Progress onBack={() => setCurrentPage('home')} />;
    default:
      return <PatientHome onNavigate={setCurrentPage} onLogout={handleLogout} />;
  }
}

export default App;