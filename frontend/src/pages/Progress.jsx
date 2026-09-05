import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { t } from '../services/translations';

function Progress({ onBack }) {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [language, setLanguage] = useState(localStorage.getItem('language') || 'en');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      setError('Not logged in');
      setLoading(false);
      return;
    }
    // For patient role, we need patient id. We'll use 1 for demo, or from /me? We'll fetch /me first.
    api.getMe(token)
      .then(user => {
        // Patient ID is not in user; we need to fetch via patient endpoint? We'll assume id=1 for now.
        const patientId = 1; // hardcoded for demo; later we can link.
        return api.getAnalytics(token, patientId);
      })
      .then(data => {
        setAnalytics(data);
        setError('');
      })
      .catch(err => {
        console.error(err);
        setError('Failed to load progress data.');
      })
      .finally(() => setLoading(false));
  }, []);

  const renderLineChart = () => {
    if (!analytics || !analytics.trend || analytics.trend.length < 2) return null;
    const points = analytics.trend;
    const width = 500;
    const height = 200;
    const maxAcc = 100;
    const minAcc = 0;
    const xStep = width / (points.length - 1);
    const coords = points.map((p, i) => ({
      x: i * xStep,
      y: height - ((p.accuracy - minAcc) / (maxAcc - minAcc)) * height,
      date: p.date,
      acc: p.accuracy,
    }));
    const polylinePoints = coords.map(c => `${c.x},${c.y}`).join(' ');
    return (
      <svg viewBox={`0 0 ${width} ${height + 20}`} className="w-full h-64">
        <line x1="0" y1={height} x2={width} y2={height} stroke="#ccc" />
        <line x1="0" y1="0" x2="0" y2={height} stroke="#ccc" />
        <polyline
          points={polylinePoints}
          fill="none"
          stroke="#3B82F6"
          strokeWidth="3"
        />
        {coords.map((c, i) => (
          <g key={i}>
            <circle cx={c.x} cy={c.y} r="4" fill="#3B82F6" />
            <text x={c.x} y={height + 15} fontSize="10" textAnchor="middle" fill="#666">
              {c.date.slice(5)}
            </text>
          </g>
        ))}
      </svg>
    );
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <button
        onClick={onBack}
        className="mb-6 bg-gray-200 hover:bg-gray-300 text-xl px-4 py-2 rounded-lg"
      >
        ← {t('back_to_games')}
      </button>

      <h1 className="text-4xl font-bold text-blue-800 mb-8">{t('my_progress')}</h1>

      {loading && <p className="text-2xl text-gray-600">Loading...</p>}
      {error && <p className="text-red-600 text-xl">{error}</p>}

      {!loading && !error && analytics && (
        <div className="space-y-8">
          {/* Line chart */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Accuracy Trend</h2>
            {renderLineChart() || <p className="text-gray-500">Not enough data to show trend.</p>}
          </div>

          {/* Category scores */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Category Performance</h2>
            {analytics.category_trend && Object.keys(analytics.category_trend).length > 0 ? (
              <div className="space-y-3">
                {Object.entries(analytics.category_trend).map(([cat, score]) => (
                  <div key={cat} className="flex items-center gap-4">
                    <span className="text-xl capitalize text-gray-700 w-32">{cat}</span>
                    <div className="flex-1 bg-gray-200 rounded-full h-5">
                      <div className="bg-blue-500 h-5 rounded-full" style={{ width: `${score}%` }}></div>
                    </div>
                    <span className="text-xl font-semibold text-gray-800">{score}%</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No category data available.</p>
            )}
          </div>

          {/* Session history */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Recent Sessions</h2>
            {analytics.sessions && analytics.sessions.length > 0 ? (
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {analytics.sessions.slice().reverse().map((s, idx) => (
                  <div key={idx} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <div>
                      <p className="text-lg font-semibold text-gray-800">{s.game_name}</p>
                      <p className="text-sm text-gray-500">{s.date}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-lg font-bold text-gray-700">Accuracy: {s.accuracy ? (s.accuracy * 100).toFixed(1) + '%' : 'N/A'}</p>
                      <p className="text-sm text-gray-500">Score: {s.score}</p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No sessions yet.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default Progress;
