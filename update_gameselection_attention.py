from pathlib import Path

content = '''import { useState } from 'react';
import MemoryGame from '../games/MemoryGame';
import SequenceGame from '../games/SequenceGame';
import AttentionGame from '../games/AttentionGame';

function GameSelection({ onBack }) {
  const [selectedGameId, setSelectedGameId] = useState(null);

  const games = [
    { id: 1, name: 'Memory Game', emoji: '🧠', description: 'Remember the objects' },
    { id: 2, name: 'Sequence Game', emoji: '🔢', description: 'Remember the order' },
    { id: 3, name: 'Attention Game', emoji: '🎯', description: 'Find the target' },
    { id: 4, name: 'Pattern Game', emoji: '🔷', description: 'Complete the pattern' },
  ];

  if (selectedGameId === 1) {
    return <MemoryGame onExit={() => setSelectedGameId(null)} />;
  }
  if (selectedGameId === 2) {
    return <SequenceGame onExit={() => setSelectedGameId(null)} />;
  }
  if (selectedGameId === 3) {
    return <AttentionGame onExit={() => setSelectedGameId(null)} />;
  }

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
            key={game.id}
            className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition text-center"
            onClick={() => setSelectedGameId(game.id)}
          >
            <span className="text-6xl">{game.emoji}</span>
            <p className="text-3xl font-semibold mt-4 text-gray-800">{game.name}</p>
            <p className="text-xl text-gray-500 mt-2">{game.description}</p>
          </button>
        ))}
      </div>
    </div>
  );
}

export default GameSelection;
'''

path = Path("frontend/src/pages/GameSelection.jsx")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(content.strip(), encoding='utf-8')
print("GameSelection.jsx updated for Attention Game!")
