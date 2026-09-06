import { useState, useEffect } from 'react';
import MemoryGame from '../games/MemoryGame';
import SequenceGame from '../games/SequenceGame';
import AttentionGame from '../games/AttentionGame';
import PatternGame from '../games/PatternGame';
import ReactionGame from '../games/ReactionGame';
import LanguageGame from '../games/LanguageGame';
import { t } from '../services/translations';
import { api } from '../services/api';

function GameSelection({ onBack }) {
  const [selectedGameId, setSelectedGameId] = useState(null);
  const [aiSuggestion, setAiSuggestion] = useState(null);
  const [difficultyMap, setDifficultyMap] = useState({});

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) return;

    // Get patient id
    api.getPatientId(token)
      .then(patientId => {
        // Fetch AI next game suggestion
        fetch(`http://localhost:8000/api/recommendations/next_game/${patientId}`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then(res => res.json())
        .then(data => setAiSuggestion(data))
        .catch(console.error);

        // Fetch difficulty recommendation for each game
        const gameIds = [1, 2, 3, 4, 5, 6];
        gameIds.forEach(gameId => {
          fetch(`http://localhost:8000/api/recommendations/difficulty/${patientId}/${gameId}`, {
            headers: { Authorization: `Bearer ${token}` },
          })
          .then(res => res.json())
          .then(data => {
            setDifficultyMap(prev => ({
              ...prev,
              [gameId]: data.recommended_difficulty,
            }));
          })
          .catch(console.error);
        });
      })
      .catch(console.error);
  }, []);

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

      {aiSuggestion && aiSuggestion.recommended_category && (
        <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-xl mb-6">
          <p className="text-xl">
            <strong>AI Suggestion:</strong> Try <strong>{aiSuggestion.recommended_category}</strong> game
            because {aiSuggestion.reason}
          </p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {games.map((game) => (
          <button
            key={game.id}
            className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition text-center relative"
            onClick={() => setSelectedGameId(game.id)}
          >
            <span className="text-6xl">{game.emoji}</span>
            <p className="text-3xl font-semibold mt-4 text-gray-800">{game.name}</p>
            <p className="text-xl text-gray-500 mt-2">{game.description}</p>
            {difficultyMap[game.id] && (
              <span className="absolute top-2 right-2 bg-blue-100 text-blue-800 text-sm font-bold px-2 py-1 rounded-full">
                AI: {difficultyMap[game.id]}
              </span>
            )}
          </button>
        ))}
      </div>
    </div>
  );
}

export default GameSelection;
