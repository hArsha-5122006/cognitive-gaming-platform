import { useState, useEffect } from 'react';
import { api } from '../services/api';

function DailyRoutine({ onBack }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newTitle, setNewTitle] = useState('');
  const [newTime, setNewTime] = useState('');

  const loadRoutine = async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await fetch('http://localhost:8000/api/daily-routine/', {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error('Failed to fetch routine');
      const data = await res.json();
      setItems(data);
      setError('');
    } catch (err) {
      console.error(err);
      setError('Failed to load routine.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRoutine();
  }, []);

  const toggleComplete = async (id) => {
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:8000/api/daily-routine/${id}/complete`, {
        method: 'PATCH',
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error('Failed to update');
      const updated = await res.json();
      setItems(prev => prev.map(item => item.id === id ? updated : item));
    } catch (err) {
      console.error(err);
      setError('Failed to update routine.');
    }
  };

  const addItem = async (e) => {
    e.preventDefault();
    if (!newTitle || !newTime) return;
    try {
      const token = localStorage.getItem('token');
      const res = await fetch('http://localhost:8000/api/daily-routine/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ title: newTitle, scheduled_time: newTime }),
      });
      if (!res.ok) throw new Error('Failed to add');
      const added = await res.json();
      setItems(prev => [...prev, added]);
      setNewTitle('');
      setNewTime('');
      setError('');
    } catch (err) {
      console.error(err);
      setError('Failed to add routine item.');
    }
  };

  const completedCount = items.filter(item => item.is_completed).length;

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <button onClick={onBack} className="mb-6 bg-gray-200 hover:bg-gray-300 text-xl px-4 py-2 rounded-lg">
        ← Back
      </button>
      <h1 className="text-4xl font-bold text-blue-800 mb-4">Today's Routine</h1>
      <p className="text-xl text-gray-600 mb-6">{completedCount} of {items.length} completed</p>

      {loading && <p className="text-2xl text-gray-600">Loading...</p>}
      {error && <p className="text-red-600 text-xl mb-4">{error}</p>}

      {!loading && !error && (
        <div className="space-y-3 max-w-2xl">
          {items.map((item) => (
            <div key={item.id} className={`flex items-center justify-between p-4 rounded-xl border-2 ${item.is_completed ? 'bg-green-50 border-green-300' : 'bg-white border-gray-200'}`}>
              <div>
                <p className="text-2xl font-semibold text-gray-800">{item.title}</p>
                <p className="text-lg text-gray-500">{item.scheduled_time}</p>
              </div>
              <button
                onClick={() => toggleComplete(item.id)}
                className={`w-10 h-10 rounded-full flex items-center justify-center text-2xl ${item.is_completed ? 'bg-green-500 text-white' : 'bg-white border-2 border-gray-300 text-transparent'}`}
              >
                ✓
              </button>
            </div>
          ))}
        </div>
      )}

      <form onSubmit={addItem} className="mt-8 bg-white p-4 rounded-xl shadow-md max-w-2xl flex flex-col gap-3">
        <h2 className="text-2xl font-bold text-gray-800">Add New Routine</h2>
        <input
          type="text"
          placeholder="Title (e.g., Yoga)"
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          className="w-full p-3 text-xl border-2 rounded-lg"
          required
        />
        <input
          type="text"
          placeholder="Time (e.g., 6:00 AM)"
          value={newTime}
          onChange={(e) => setNewTime(e.target.value)}
          className="w-full p-3 text-xl border-2 rounded-lg"
          required
        />
        <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white text-xl font-bold py-3 rounded-lg">
          Add
        </button>
      </form>
    </div>
  );
}

export default DailyRoutine;
