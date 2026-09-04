function GameSelection({ onBack }) {
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