from pathlib import Path

base = Path("frontend/src")
base.mkdir(parents=True, exist_ok=True)

files = {
"services/api.js": '''const API_BASE_URL = 'http://localhost:8000';

export const api = {
  async login(email, password) {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    const res = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData,
    });
    if (!res.ok) throw new Error('Login failed');
    return res.json();
  },
  async getMe(token) {
    const res = await fetch(`${API_BASE_URL}/api/auth/me`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    if (!res.ok) throw new Error('Not authenticated');
    return res.json();
  }
};
''',
"pages/Login.jsx": '''import { useState } from 'react';
import { api } from '../services/api';

function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const data = await api.login(email, password);
      localStorage.setItem('token', data.access_token);
      onLogin(data.access_token);
    } catch (err) {
      setError('Login failed. Please check your email and password.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-blue-50">
      <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md">
        <h1 className="text-4xl font-bold text-center text-blue-800 mb-6">Welcome</h1>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-2xl text-gray-700 mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full p-4 text-2xl border-2 border-gray-300 rounded-xl focus:outline-none focus:border-blue-500"
              placeholder="Enter your email"
              required
            />
          </div>
          <div>
            <label className="block text-2xl text-gray-700 mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full p-4 text-2xl border-2 border-gray-300 rounded-xl focus:outline-none focus:border-blue-500"
              placeholder="Enter your password"
              required
            />
          </div>
          {error && <p className="text-red-600 text-xl">{error}</p>}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white text-2xl font-bold py-4 rounded-xl disabled:opacity-50"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
''',
"pages/PatientHome.jsx": '''function PatientHome({ onNavigate, onLogout }) {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <header className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-bold text-blue-800">Hello!</h1>
        <button
          onClick={onLogout}
          className="bg-red-500 hover:bg-red-600 text-white text-xl px-6 py-3 rounded-xl"
        >
          Logout
        </button>
      </header>
      <main className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <button
          onClick={() => onNavigate('games')}
          className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition text-center"
        >
          <span className="text-6xl">🧠</span>
          <p className="text-3xl font-semibold mt-4 text-gray-800">Play Games</p>
        </button>
        <button
          onClick={() => onNavigate('reminders')}
          className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition text-center"
        >
          <span className="text-6xl">💊</span>
          <p className="text-3xl font-semibold mt-4 text-gray-800">Reminders</p>
        </button>
        <button
          onClick={() => onNavigate('progress')}
          className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition text-center"
        >
          <span className="text-6xl">📊</span>
          <p className="text-3xl font-semibold mt-4 text-gray-800">My Progress</p>
        </button>
      </main>
    </div>
  );
}

export default PatientHome;
''',
"pages/GameSelection.jsx": '''function GameSelection({ onBack }) {
  const games = [
    { name: 'Memory Game', emoji: '🧠' },
    { name: 'Sequence Game', emoji: '🔢' },
    { name: 'Attention Game', emoji: '🎯' },
    { name: 'Pattern Game', emoji: '🔷' },
  ];

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <button
        onClick={onBack}
        className="mb-6 bg-gray-200 hover:bg-gray-300 text-xl px-4 py-2 rounded-lg"
      >
        ← Back
      </button>
      <h1 className="text-4xl font-bold text-blue-800 mb-8">Choose a Game</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {games.map((game) => (
          <button
            key={game.name}
            className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition text-center"
            onClick={() => alert(`${game.name} coming soon!`)}
          >
            <span className="text-6xl">{game.emoji}</span>
            <p className="text-3xl font-semibold mt-4 text-gray-800">{game.name}</p>
          </button>
        ))}
      </div>
    </div>
  );
}

export default GameSelection;
''',
"pages/Reminders.jsx": '''function Reminders({ onBack }) {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <button
        onClick={onBack}
        className="mb-6 bg-gray-200 hover:bg-gray-300 text-xl px-4 py-2 rounded-lg"
      >
        ← Back
      </button>
      <h1 className="text-4xl font-bold text-blue-800 mb-8">Reminders</h1>
      <div className="bg-white p-6 rounded-2xl shadow-lg">
        <p className="text-2xl text-gray-700">No reminders yet. This feature is coming soon.</p>
      </div>
    </div>
  );
}

export default Reminders;
''',
"pages/Progress.jsx": '''function Progress({ onBack }) {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <button
        onClick={onBack}
        className="mb-6 bg-gray-200 hover:bg-gray-300 text-xl px-4 py-2 rounded-lg"
      >
        ← Back
      </button>
      <h1 className="text-4xl font-bold text-blue-800 mb-8">My Progress</h1>
      <div className="bg-white p-6 rounded-2xl shadow-lg">
        <p className="text-2xl text-gray-700">Your progress will appear here after you play games.</p>
      </div>
    </div>
  );
}

export default Progress;
''',
"pages/CaregiverDashboard.jsx": '''function CaregiverDashboard({ onLogout }) {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <header className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-bold text-blue-800">Caregiver Dashboard</h1>
        <button
          onClick={onLogout}
          className="bg-red-500 hover:bg-red-600 text-white text-xl px-6 py-3 rounded-xl"
        >
          Logout
        </button>
      </header>
      <div className="bg-white p-6 rounded-2xl shadow-lg">
        <p className="text-2xl text-gray-700">Patient monitoring and analytics will be displayed here.</p>
      </div>
    </div>
  );
}

export default CaregiverDashboard;
''',
"App.jsx": '''import { useState, useEffect } from 'react';
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
'''
}

for filename, content in files.items():
    filepath = base / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content.strip(), encoding='utf-8')
    print(f"Written {filepath}")
print("All frontend files written successfully.")
