function Reminders({ onBack }) {
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