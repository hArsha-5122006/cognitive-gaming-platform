import { useState, useEffect } from 'react';
import { api } from '../services/api';

function CaregiverDashboard({ onLogout }) {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    api.getCaregiverDashboard(token)
      .then((data) => {
        setPatients(data);
        if (data.length > 0) {
          setSelectedPatient(data[0]);
        }
      })
      .catch((err) => {
        console.error(err);
        setError('Failed to load dashboard.');
      })
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (!selectedPatient) return;
    const token = localStorage.getItem('token');
    api.getCaregiverAlerts(token, selectedPatient.patient_id)
      .then(setAlerts)
      .catch((err) => console.error('Failed to load alerts:', err));
  }, [selectedPatient]);

  const patient = selectedPatient;

  return (
    <div className="min-h-screen bg-gray-100 p-4 md:p-8">
      <header className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-bold text-blue-800">Caregiver Dashboard</h1>
        <button
          onClick={onLogout}
          className="bg-red-500 hover:bg-red-600 text-white text-xl px-6 py-3 rounded-xl"
        >
          Logout
        </button>
      </header>

      {loading && <p className="text-2xl text-gray-600">Loading...</p>}
      {error && <p className="text-red-600 text-xl">{error}</p>}

      {!loading && !error && patients.length === 0 && (
        <p className="text-2xl text-gray-600">No patients assigned.</p>
      )}

      {patients.length > 0 && (
        <div className="flex flex-col md:flex-row gap-6">
          <aside className="w-full md:w-64 bg-white rounded-2xl shadow-lg p-4">
            <h2 className="text-2xl font-bold text-gray-700 mb-4">Patients</h2>
            {patients.map((p) => (
              <button
                key={p.patient_id}
                onClick={() => setSelectedPatient(p)}
                className={`w-full text-left p-3 rounded-lg mb-2 transition ${
                  patient?.patient_id === p.patient_id
                    ? 'bg-blue-100 ring-2 ring-blue-300'
                    : 'hover:bg-gray-100'
                }`}
              >
                <p className="text-xl font-semibold text-gray-800">{p.name}</p>
                <p className="text-sm text-gray-500">{p.email}</p>
              </button>
            ))}
          </aside>

          {patient && (
            <div className="flex-1 space-y-6">
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h2 className="text-3xl font-bold text-gray-800 mb-4">
                  {patient.name}
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                  <div className="bg-blue-50 rounded-xl p-4">
                    <p className="text-lg text-blue-600">Overall Performance</p>
                    <p className="text-4xl font-bold text-blue-800">{patient.overall_performance}%</p>
                  </div>
                  <div className="bg-green-50 rounded-xl p-4">
                    <p className="text-lg text-green-600">Games Completed</p>
                    <p className="text-4xl font-bold text-green-800">{patient.games_completed}</p>
                  </div>
                  <div className="bg-yellow-50 rounded-xl p-4">
                    <p className="text-lg text-yellow-600">Current Streak</p>
                    <p className="text-4xl font-bold text-yellow-800">{patient.current_streak_days} days</p>
                  </div>
                </div>

                <h3 className="text-2xl font-bold text-gray-700 mb-4">Category Scores</h3>
                <div className="space-y-2 mb-6">
                  {Object.entries(patient.category_scores).map(([cat, score]) => (
                    <div key={cat} className="flex items-center gap-4">
                      <span className="text-xl capitalize text-gray-700 w-32">{cat}</span>
                      <div className="flex-1 bg-gray-200 rounded-full h-4">
                        <div
                          className="bg-blue-500 h-4 rounded-full"
                          style={{ width: `${score}%` }}
                        ></div>
                      </div>
                      <span className="text-xl font-semibold text-gray-800">{score}%</span>
                    </div>
                  ))}
                </div>

                {/* Alerts Section */}
                <div>
                  <h3 className="text-2xl font-bold text-gray-700 mb-3">Alerts</h3>
                  {alerts.length === 0 ? (
                    <p className="text-lg text-gray-500">No alerts at this time.</p>
                  ) : (
                    <div className="space-y-2">
                      {alerts.map((alert, idx) => (
                        <div
                          key={idx}
                          className={`p-3 rounded-lg flex items-center gap-3 ${
                            alert.type === 'warning'
                              ? 'bg-yellow-50 border border-yellow-300'
                              : 'bg-green-50 border border-green-300'
                          }`}
                        >
                          <span className="text-2xl">
                            {alert.type === 'warning' ? '⚠️' : '✅'}
                          </span>
                          <p className="text-lg text-gray-800">{alert.message}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default CaregiverDashboard;
