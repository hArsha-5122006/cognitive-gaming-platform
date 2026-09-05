import { useState, useEffect } from 'react';
import { t } from '../services/translations';

// Static routine items (English/Telugu)
const ROUTINE_ITEMS = [
  { id: 1, time: '7:00 AM', emoji: '☀️', label: 'Morning Wake-up', teLabel: 'ఉదయం నిద్రలేవడం' },
  { id: 2, time: '8:00 AM', emoji: '🍳', label: 'Breakfast', teLabel: 'అల్పాహారం' },
  { id: 3, time: '10:00 AM', emoji: '💊', label: 'Medicine', teLabel: 'మందులు' },
  { id: 4, time: '12:00 PM', emoji: '💧', label: 'Drink Water', teLabel: 'నీరు త్రాగడం' },
  { id: 5, time: '1:00 PM', emoji: '🍚', label: 'Lunch', teLabel: 'భోజనం' },
  { id: 6, time: '5:00 PM', emoji: '🚶', label: 'Walk', teLabel: 'నడక' },
  { id: 7, time: '8:00 PM', emoji: '🍲', label: 'Dinner', teLabel: 'రాత్రి భోజనం' },
  { id: 8, time: '10:00 PM', emoji: '😴', label: 'Sleep', teLabel: 'నిద్ర' },
];

const getDateKey = () => new Date().toISOString().split('T')[0]; // YYYY-MM-DD

function DailyRoutine({ onBack }) {
  const [completed, setCompleted] = useState({});
  const [language, setLanguage] = useState(localStorage.getItem('language') || 'en');

  useEffect(() => {
    const todayKey = getDateKey();
    const saved = JSON.parse(localStorage.getItem('routine_' + todayKey)) || {};
    setCompleted(saved);
  }, []);

  const toggleComplete = (id) => {
    setCompleted(prev => {
      const newState = { ...prev, [id]: !prev[id] };
      localStorage.setItem('routine_' + getDateKey(), JSON.stringify(newState));
      return newState;
    });
  };

  const allDone = ROUTINE_ITEMS.every(item => completed[item.id]);
  const progress = ROUTINE_ITEMS.filter(item => completed[item.id]).length;

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 p-4 md:p-8">
      <button
        onClick={onBack}
        className="mb-6 bg-white bg-opacity-70 hover:bg-opacity-100 text-gray-700 text-lg px-4 py-2 rounded-lg shadow transition"
      >
        ← {t('back_to_games')}
      </button>

      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-2xl shadow-xl p-6">
          <h1 className="text-4xl font-bold text-emerald-800 text-center mb-2">
            {language === 'en' ? "Today's Routine" : 'నేటి దినచర్య'}
          </h1>
          <p className="text-center text-xl text-gray-600 mb-6">
            {language === 'en' ? `${progress} of ${ROUTINE_ITEMS.length} completed` : `${ROUTINE_ITEMS.length}లో ${progress} పూర్తయ్యాయి`}
          </p>

          {allDone && (
            <div className="bg-green-100 border border-green-300 rounded-xl p-3 mb-6 text-center text-xl text-green-800">
              {language === 'en' ? 'Great job! All activities completed!' : 'చాలా బాగా! అన్ని పనులు పూర్తయ్యాయి!'}
            </div>
          )}

          <div className="space-y-3">
            {ROUTINE_ITEMS.map((item) => {
              const isCompleted = completed[item.id];
              return (
                <div
                  key={item.id}
                  className={`flex items-center justify-between p-4 rounded-xl border-2 transition ${
                    isCompleted
                      ? 'bg-green-50 border-green-300'
                      : 'bg-gray-50 border-gray-200 hover:border-emerald-300'
                  }`}
                >
                  <div className="flex items-center gap-4">
                    <span className="text-3xl">{item.emoji}</span>
                    <div>
                      <p className="text-2xl font-semibold text-gray-800">
                        {language === 'en' ? item.label : item.teLabel}
                      </p>
                      <p className="text-lg text-gray-500">{item.time}</p>
                    </div>
                  </div>
                  <button
                    onClick={() => toggleComplete(item.id)}
                    className={`w-10 h-10 rounded-full flex items-center justify-center text-2xl transition ${
                      isCompleted
                        ? 'bg-green-500 text-white'
                        : 'bg-white border-2 border-gray-300 text-transparent hover:border-green-500'
                    }`}
                  >
                    ✓
                  </button>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

export default DailyRoutine;