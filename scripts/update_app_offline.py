from pathlib import Path

content = '''import { useState, useEffect } from 'react';
import Login from './pages/Login';
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
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      // Sync pending results when back online
      const t = localStorage.getItem('token');
      if (t) {
        api.syncPendingResults(t).then(() => {
          console.log('Pending results synced.');
        });
      }
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
    return <Login onLogin={handleLogin} />;
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
      {(() => {
        switch (currentPage) {
          case 'games':
            return <GameSelection onBack={() => setCurrentPage('home')} />;
          case 'reminders':
            return <Reminders onBack={() => setCurrentPage('home')} />;
          case 'progress':
            return <Progress onBack={() => setCurrentPage('home')} />;
          case 'routine':
            return <DailyRoutine onBack={() => setCurrentPage('home')} />;
          default:
            return <PatientHome onNavigate={setCurrentPage} onLogout={handleLogout} language={language} onToggleLanguage={toggleLanguage} />;
        }
      })()}
    </div>
  );
}

export default App;
'''

path = Path("frontend/src/App.jsx")
path.write_text(content.strip(), encoding='utf-8')
print("App.jsx updated with offline banner and sync!")
