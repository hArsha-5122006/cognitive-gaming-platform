function CaregiverDashboard({ onLogout }) {
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