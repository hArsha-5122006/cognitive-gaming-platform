import { useState, useEffect } from 'react';
import Login from './pages/Login';
import Signup from './pages/Signup';
import PatientHome from './pages/PatientHome';
import GameSelection from './pages/GameSelection';
import Reminders from './pages/Reminders';
import Progress from './pages/Progress';
import CaregiverDashboard from './pages/CaregiverDashboard';
import DailyRoutine from './pages/DailyRoutine';
import { api } from './services/api';
import { getLanguage, setLanguage } from './services/translations';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);
  const [currentPage, setCurrentPage] = useState('home');
  const [language, setLanguageState] = useState(getLanguage());
  const [isSignup, setIsSignup] = useState(false);
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      const t = localStorage.getItem('token');
      if (t) api.syncPendingResults(t);
    };
    const handleOffline = () => setIsOnline(false);
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

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
    setIsSignup(false);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    setCurrentPage('home');
  };

  const toggleLanguage = () => {
    const newLang = language === 'en' ? 'te' : 'en';
    setLanguage(newLang);
    setLanguageState(newLang);
  };

  if (!token || !user) {
    if (isSignup) return <Signup onSignupSuccess={() => setIsSignup(false)} />;
    return <Login onLogin={handleLogin} onSwitchToSignup={() => setIsSignup(true)} />;
  }

  if (user.role === 'caregiver' || user.role === 'admin') {
    return <CaregiverDashboard onLogout={handleLogout} />;
  }

  return (
    <div>
      {!isOnline && (
        <div className="bg-red-500 text-white text-center py-2 text-xl">
          You are offline. Games and reminders will be saved locally.
        </div>
      )}
      {currentPage === 'games' && <GameSelection onBack={() => setCurrentPage('home')} />}
      {currentPage === 'reminders' && <Reminders onBack={() => setCurrentPage('home')} />}
      {currentPage === 'progress' && <Progress onBack={() => setCurrentPage('home')} />}
      {currentPage === 'routine' && <DailyRoutine onBack={() => setCurrentPage('home')} />}
      {currentPage === 'home' && (
        <PatientHome
          onNavigate={setCurrentPage}
          onLogout={handleLogout}
          language={language}
          onToggleLanguage={toggleLanguage}
        />
      )}
    </div>
  );
}

export default App;
