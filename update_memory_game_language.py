from pathlib import Path

content = '''import { useState, useEffect, useRef } from 'react';
import useGameSession from '../hooks/useGameSession';
import { speak } from '../services/voice';
import { t } from '../services/translations';

const ITEMS = [
  { emoji: '🍎', name: 'Apple' },
  { emoji: '🏠', name: 'House' },
  { emoji: '🌸', name: 'Flower' },
  { emoji: '🚗', name: 'Car' },
  { emoji: '🐶', name: 'Dog' },
  { emoji: '🐱', name: 'Cat' },
  { emoji: '🌳', name: 'Tree' },
  { emoji: '🍌', name: 'Banana' },
  { emoji: '🚲', name: 'Bicycle' },
  { emoji: '📚', name: 'Book' },
  { emoji: '🎵', name: 'Music' },
  { emoji: '☕', name: 'Tea' },
  { emoji: '🌾', name: 'Rice' },
  { emoji: '🛕', name: 'Temple' },
  { emoji: '🐘', name: 'Elephant' },
  { emoji: '🌺', name: 'Hibiscus' },
];

const DIFFICULTY_SETTINGS = {
  easy: { showCount: 4, optionsCount: 6, displayTime: 3000 },
  medium: { showCount: 6, optionsCount: 9, displayTime: 3000 },
  hard: { showCount: 8, optionsCount: 12, displayTime: 3000 },
};

function shuffleArray(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function MemoryGame({ onExit }) {
  const gameSession = useGameSession(1, 'easy');
  const [difficulty, setDifficulty] = useState('easy');
  const [phase, setPhase] = useState('setup');
  const [displayItems, setDisplayItems] = useState([]);
  const [options, setOptions] = useState([]);
  const [selected, setSelected] = useState(new Set());
  const [score, setScore] = useState({ correct: 0, wrong: 0 });

  const timerRef = useRef(null);

  useEffect(() => {
    return () => clearTimeout(timerRef.current);
  }, []);

  useEffect(() => {
    if (phase === 'show') {
      speak(t('remember_objects'));
    } else if (phase === 'select') {
      speak(t('which_objects'));
    } else if (phase === 'finished') {
      speak(`${t('game_over')} ${score.correct} ${t('correct')}, ${score.wrong} ${t('wrong')}`);
    }
  }, [phase, score.correct, score.wrong]);

  const startGame = () => {
    const settings = DIFFICULTY_SETTINGS[difficulty];
    const shuffledAll = shuffleArray(ITEMS);
    const shown = shuffledAll.slice(0, settings.showCount);
    const distractors = shuffledAll.slice(settings.showCount, settings.showCount + (settings.optionsCount - settings.showCount));
    const allOptions = shuffleArray([...shown, ...distractors]);

    setDisplayItems(shown);
    setOptions(allOptions);
    setSelected(new Set());
    setScore({ correct: 0, wrong: 0 });
    setPhase('show');
    gameSession.startGame();

    timerRef.current = setTimeout(() => {
      setPhase('select');
    }, settings.displayTime);
  };

  const toggleSelect = (itemName) => {
    if (phase !== 'select') return;
    setSelected((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(itemName)) {
        newSet.delete(itemName);
      } else {
        newSet.add(itemName);
      }
      return newSet;
    });
  };

  const handleSubmit = () => {
    let correct = 0;
    let wrong = 0;
    const answers = [];
    selected.forEach((selectedName) => {
      const wasShown = displayItems.some((item) => item.name === selectedName);
      const isCorrect = wasShown;
      if (isCorrect) correct++;
      else wrong++;
      answers.push({
        question: selectedName,
        correct_answer: wasShown ? selectedName : 'Not in original set',
        user_answer: selectedName,
        is_correct: isCorrect ? 1 : 0,
        reaction_time_ms: 0,
      });
    });

    answers.forEach((a) => {
      gameSession.recordAnswer(a.question, a.correct_answer, a.user_answer, a.is_correct === 1, 0);
    });

    setScore({ correct, wrong });
    setPhase('finished');
    gameSession.endGame();
  };

  const totalShown = DIFFICULTY_SETTINGS[difficulty].showCount;
  const accuracy = totalShown > 0 ? Math.round((score.correct / totalShown) * 100) : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4 md:p-8 flex flex-col items-center">
      <div className="w-full max-w-3xl">
        <button
          onClick={onExit}
          className="mb-6 bg-white bg-opacity-70 hover:bg-opacity-100 text-gray-700 text-lg px-4 py-2 rounded-lg shadow transition"
        >
          ← {t('back_to_games')}
        </button>

        {phase === 'setup' && (
          <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
            <h1 className="text-4xl font-bold text-blue-800 mb-6">{t('memory_game')}</h1>
            <p className="text-xl text-gray-600 mb-8">{t('choose_difficulty')}</p>
            <div className="flex justify-center gap-4 mb-8">
              {['easy', 'medium', 'hard'].map((level) => (
                <button
                  key={level}
                  onClick={() => setDifficulty(level)}
                  className={`px-6 py-3 rounded-xl text-xl font-semibold capitalize transition ${
                    difficulty === level
                      ? 'bg-blue-600 text-white shadow-lg'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  {t(level)}
                </button>
              ))}
            </div>
            <button
              onClick={startGame}
              className="bg-green-500 hover:bg-green-600 text-white text-2xl font-bold px-8 py-4 rounded-xl shadow-lg transition transform hover:scale-105"
            >
              {t('start_game')}
            </button>
          </div>
        )}

        {phase === 'show' && (
          <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
            <h2 className="text-3xl font-bold text-blue-800 mb-6">{t('memory_instruction_show')}</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {displayItems.map((item) => (
                <div
                  key={item.name}
                  className="bg-blue-50 rounded-xl p-6 flex flex-col items-center justify-center"
                >
                  <span className="text-6xl mb-2">{item.emoji}</span>
                  <span className="text-2xl font-medium text-gray-800">{item.name}</span>
                </div>
              ))}
            </div>
            <p className="mt-6 text-lg text-gray-500">Memorize them...</p>
          </div>
        )}

        {phase === 'select' && (
          <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
            <h2 className="text-3xl font-bold text-blue-800 mb-4">{t('memory_instruction_select')}</h2>
            <p className="text-lg text-gray-600 mb-6">{t('memory_instruction_hint')}</p>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
              {options.map((item) => (
                <button
                  key={item.name}
                  onClick={() => toggleSelect(item.name)}
                  className={`rounded-xl p-4 flex flex-col items-center justify-center transition transform hover:scale-105 ${
                    selected.has(item.name)
                      ? 'bg-blue-600 text-white shadow-lg ring-4 ring-blue-300'
                      : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                  }`}
                >
                  <span className="text-5xl mb-1">{item.emoji}</span>
                  <span className="text-xl font-medium">{item.name}</span>
                </button>
              ))}
            </div>
            <button
              onClick={handleSubmit}
              disabled={selected.size === 0}
              className="bg-blue-600 hover:bg-blue-700 text-white text-2xl font-bold px-8 py-4 rounded-xl shadow-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {t('submit_answers')}
            </button>
          </div>
        )}

        {phase === 'finished' && (
          <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
            <h2 className="text-4xl font-bold text-blue-800 mb-6">{t('game_over')}</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
              <div className="bg-green-50 rounded-xl p-4">
                <p className="text-2xl font-bold text-green-700">{score.correct}</p>
                <p className="text-lg text-green-600">{t('correct')}</p>
              </div>
              <div className="bg-red-50 rounded-xl p-4">
                <p className="text-2xl font-bold text-red-700">{score.wrong}</p>
                <p className="text-lg text-red-600">{t('wrong')}</p>
              </div>
              <div className="bg-blue-50 rounded-xl p-4">
                <p className="text-2xl font-bold text-blue-700">{accuracy}%</p>
                <p className="text-lg text-blue-600">{t('accuracy')}</p>
              </div>
            </div>
            <button
              onClick={() => setPhase('setup')}
              className="bg-green-500 hover:bg-green-600 text-white text-xl font-bold px-6 py-3 rounded-xl shadow-lg transition"
            >
              {t('play_again')}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default MemoryGame;
'''

path = Path("frontend/src/games/MemoryGame.jsx")
path.write_text(content.strip(), encoding='utf-8')
print("MemoryGame.jsx updated with translations!")
