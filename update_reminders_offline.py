from pathlib import Path

content = '''import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { t } from '../services/translations';

const TYPE_EMOJI = {
  medicine: '💊',
  hydration: '💧',
  activity: '🚶',
  appointment: '🏥'
};

function Reminders({ onBack }) {
  const [reminders, setReminders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [language, setLanguage] = useState(localStorage.getItem('language') || 'en');

  const loadReminders = async () => {
    try {
      const token = localStorage.getItem('token');
      const data = await api.getReminders(token);
      setReminders(data);
      api.cacheReminders(data);
      setError('');
    } catch (err) {
      console.error(err);
      // Use cached reminders if offline
      const cached = api.getCachedReminders();
      if (cached.length > 0) {
        setReminders(cached);
        setError('Offline mode: showing cached reminders.');
      } else {
        setError('Failed to load reminders.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReminders();
  }, []);

  const handleComplete = async (id) => {
    try {
      const token = localStorage.getItem('token');
      const updated = await api.completeReminder(token, id);
      setReminders(prev => prev.map(r => r.id === id ? updated : r));
      api.cacheReminders(reminders.map(r => r.id === id ? updated : r));
    } catch (err) {
      console.error(err);
      setError('Failed to update reminder.');
    }
  };

  const formatTime = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleString(language === 'en' ? 'en-US' : 'te-IN', {
      weekday: 'short', hour: '2-digit', minute: '2-digit'
    });
  };

  const activeReminders = reminders.filter(r => !r.is_completed);
  const completedReminders = reminders.filter(r => r.is_completed);

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <button
        onClick={onBack}
        className="mb-6 bg-gray-200 hover:bg-gray-300 text-xl px-4 py-2 rounded-lg"
      >
        ← {t('back_to_games')}
      </button>

      <h1 className="text-4xl font-bold text-blue-800 mb-8">{t('reminders')}</h1>

      {loading && <p className="text-2xl text-gray-600">Loading...</p>}
      {error && <p className="text-red-600 text-xl mb-4">{error}</p>}

      {!loading && !error && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
            {activeReminders.map((r) => (
              <div
                key={r.id}
                className={`bg-white p-4 rounded-xl shadow-md flex items-center justify-between ${
                  r.is_completed ? 'opacity-60' : ''
                }`}
              >
                <div className="flex items-center gap-4">
                  <span className="text-4xl">{TYPE_EMOJI[r.reminder_type] || '📌'}</span>
                  <div>
                    <p className="text-2xl font-semibold text-gray-800">{r.title}</p>
                    <p className="text-lg text-gray-500">{formatTime(r.scheduled_time)}</p>
                    {r.description && <p className="text-sm text-gray-400">{r.description}</p>}
                  </div>
                </div>
                <button
                  onClick={() => handleComplete(r.id)}
                  className="w-10 h-10 rounded-full bg-green-100 border-2 border-green-300 text-green-600 text-2xl flex items-center justify-center hover:bg-green-200 transition"
                >
                  ✓
                </button>
              </div>
            ))}
          </div>

          {completedReminders.length > 0 && (
            <div>
              <h2 className="text-2xl font-bold text-gray-600 mb-4">Completed</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {completedReminders.map((r) => (
                  <div key={r.id} className="bg-gray-50 p-4 rounded-xl shadow-sm flex items-center gap-4 opacity-70">
                    <span className="text-3xl">{TYPE_EMOJI[r.reminder_type] || '📌'}</span>
                    <div>
                      <p className="text-xl font-semibold text-gray-500 line-through">{r.title}</p>
                      <p className="text-sm text-gray-400">{formatTime(r.scheduled_time)}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default Reminders;
'''

path = Path("frontend/src/pages/Reminders.jsx")
path.write_text(content.strip(), encoding='utf-8')
print("Reminders.jsx updated with offline caching!")
