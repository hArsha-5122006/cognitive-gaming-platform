from pathlib import Path

content = '''import { useState } from 'react';
import MemoryGame from '../games/MemoryGame';
import SequenceGame from '../games/SequenceGame';
import AttentionGame from '../games/AttentionGame';
import PatternGame from '../games/PatternGame';
import ReactionGame from '../games/ReactionGame';
import LanguageGame from '../games/LanguageGame';
import { t } from '../services/translations';

function GameSelection({ onBack }) {
  const [selectedGameId, setSelectedGameId] = useState(null);

  const games = [
    { id: 1, name: t('memory_game'), emoji: '🧠', description: t('memory_game') },
    { id: 2, name: t('sequence_game'), emoji: '🔢', description: t('sequence_game') },
    { id: 3, name: t('attention_game'), emoji: '🎯', description: t('attention_game') },
    { id: 4, name: t('pattern_game'), emoji: '🔷', description: t('pattern_game') },
    { id: 5, name: t('reaction_game'), emoji: '⚡', description: t('reaction_game') },
    { id: 6, name: t('language_game'), emoji: '📝', description: t('language_game') },
  ];

  if (selectedGameId === 1) return <MemoryGame onExit={() => setSelectedGameId(null)} />;
  if (selectedGameId === 2) return <SequenceGame onExit={() => setSelectedGameId(null)} />;
  if (selectedGameId === 3) return <AttentionGame onExit={() => setSelectedGameId(null)} />;
  if (selectedGameId === 4) return <PatternGame onExit={() => setSelectedGameId(null)} />;
  if (selectedGameId === 5) return <ReactionGame onExit={() => setSelectedGameId(null)} />;
  if (selectedGameId === 6) return <LanguageGame onExit={() => setSelectedGameId(null)} />;

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <button
        onClick={onBack}
        className="mb-6 bg-gray-200 hover:bg-gray-300 text-xl px-4 py-2 rounded-lg"
      >
        ← {t('back_to_games')}
      </button>
      <h1 className="text-4xl font-bold text-blue-800 mb-8">{t('choose_game')}</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
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
path.write_text(content.strip(), encoding='utf-8')
print("GameSelection.jsx updated with translations!")
