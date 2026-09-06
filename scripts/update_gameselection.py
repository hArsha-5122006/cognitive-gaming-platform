from pathlib import Path

content = '''import { useState } from 'react';
import useGameSession from '../hooks/useGameSession';

function GameSelection({ onBack }) {
  const [selectedGame, setSelectedGame] = useState(null);
  const gameSession = useGameSession(1, 'easy');

  const games = [
    { id: 1, name: 'Memory Game', emoji: '🧠', description: 'Remember the objects' },
    { id: 2, name: 'Sequence Game', emoji: '🔢', description: 'Remember the order' },
    { id: 3, name: 'Attention Game', emoji: '🎯', description: 'Find the target' },
    { id: 4, name: 'Pattern Game', emoji: '🔷', description: 'Complete the pattern' },
  ];

  const handleStart = () => {
    setSelectedGame('memory');
    gameSession.startGame();
  };

  const handleCorrect = () => {
    gameSession.recordAnswer('Apple', 'Apple', 'Apple', true, 1200);
  };

  const handleWrong = () => {
    gameSession.recordAnswer('House', 'House', 'Car', false, 1800);
  };

  const handleEnd = () => {
    gameSession.endGame();
  };

  if (selectedGame === 'memory') {
    return (
      <div className="min-h-screen bg-gray-100 p-8">
        <button
          onClick={() => { setSelectedGame(null); }}
          className="mb-6 bg-gray-200 hover:bg-gray-300 text-xl px-4 py-2 rounded-lg"
        >
          ← Back
        </button>
        <h1 className="text-4xl font-bold text-blue-800 mb-8">Memory Game Demo</h1>
        <div className="bg-white p-6 rounded-2xl shadow-lg max-w-md space-y-4">
          <p className="text-2xl">Status: {gameSession.isActive ? 'Playing...' : 'Finished'}</p>
          <p className="text-2xl">Score: {gameSession.score}</p>
          <p className="text-2xl">Attempts: {gameSession.attempts}</p>
          <p className="text-2xl">Mistakes: {gameSession.mistakes}</p>
          <div className="flex flex-col gap-3">
            <button
              onClick={handleCorrect}
              disabled={!gameSession.isActive}
              className="bg-green-500 hover:bg-green-600 text-white text-xl font-bold py-3 rounded-xl disabled:opacity-50"
            >
              Correct Answer
            </button>
            <button
              onClick={handleWrong}
              disabled={!gameSession.isActive}
              className="bg-red-500 hover:bg-red-600 text-white text-xl font-bold py-3 rounded-xl disabled:opacity-50"
            >
              Wrong Answer
            </button>
            <button
              onClick={handleEnd}
              disabled={!gameSession.isActive}
              className="bg-blue-600 hover:bg-blue-700 text-white text-xl font-bold py-3 rounded-xl disabled:opacity-50"
            >
              End Game
            </button>
          </div>
        </div>
      </div>
    );
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
            onClick={() => {
              if (game.id === 1) handleStart();
              else alert(`${game.name} coming soon!`);
            }}
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
print("Updated GameSelection.jsx successfully!")
