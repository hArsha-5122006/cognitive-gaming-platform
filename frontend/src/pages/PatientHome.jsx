function PatientHome({ onNavigate, onLogout }) {
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