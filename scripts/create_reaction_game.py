from pathlib import Path

content = '''import { useState, useEffect, useRef, useCallback } from 'react';
import useGameSession from '../hooks/useGameSession';

// Difficulty settings: delay before target appears (ms), distractors enabled
const DIFFICULTY_SETTINGS = {
  easy: { delayMin: 2000, delayMax: 4000, distractors: false, attempts: 5 },
  medium: { delayMin: 1000, delayMax: 2500, distractors: false, attempts: 5 },
  hard: { delayMin: 500, delayMax: 1500, distractors: true, attempts: 5 },
};

function ReactionGame({ onExit }) {
  const gameSession = useGameSession(5, 'easy');
  const [difficulty, setDifficulty] = useState('easy');
  const [phase, setPhase] = useState('setup'); // setup, waiting, ready, tooSoon, finished
  const [startTime, setStartTime] = useState(null);
  const [reactionTimes, setReactionTimes] = useState([]);
  const [attempt, setAttempt] = useState(0);
  const [totalAttempts, setTotalAttempts] = useState(DIFFICULTY_SETTINGS.easy.attempts);
  const [showDistractor, setShowDistractor] = useState(false);
  const [lastReaction, setLastReaction] = useState(null);
  const [timerId, setTimerId] = useState(null);
  const [tooSoon, setTooSoon] = useState(false);

  const gameActive = phase === 'waiting' || phase === 'ready';

  const clearTimer = useCallback(() => {
    if (timerId) {
      clearTimeout(timerId);
      setTimerId(null);
    }
  }, [timerId]);

  useEffect(() => {
    return () => clearTimer();
  }, [clearTimer]);

  const startGame = () => {
    const settings = DIFFICULTY_SETTINGS[difficulty];
    setTotalAttempts(settings.attempts);
    setAttempt(0);
    setReactionTimes([]);
    setLastReaction(null);
    setTooSoon(false);
    setPhase('waiting');
    gameSession.startGame();
    scheduleNext();
  };

  const scheduleNext = () => {
    clearTimer();
    const settings = DIFFICULTY_SETTINGS[difficulty];
    const delay = Math.floor(Math.random() * (settings.delayMax - settings.delayMin + 1)) + settings.delayMin;
    const id = setTimeout(() => {
      setPhase('ready');
      setStartTime(Date.now());
      if (settings.distractors && Math.random() > 0.5) {
        setShowDistractor(true);
      } else {
        setShowDistractor(false);
      }
      setTimerId(null);
    }, delay);
    setTimerId(id);
  };

  const handleTap = () => {
    if (phase === 'waiting') {
      // Tapped too early
      clearTimer();
      setTooSoon(true);
      setPhase('tooSoon');
      return;
    }
    if (phase === 'ready') {
      const reaction = Date.now() - startTime;
      setLastReaction(reaction);
      setReactionTimes((prev) => [...prev, reaction]);
      gameSession.recordAnswer(
        `Reaction ${attempt + 1}`,
        'Tap',
        'Tap',
        1,
        reaction
      );
      setAttempt((prev) => {
        const newAttempt = prev + 1;
        if (newAttempt >= totalAttempts) {
          // Finish after last attempt
          finishGame();
          return newAttempt;
        }
        // Otherwise, wait for next
        setPhase('waiting');
        scheduleNext();
        return newAttempt;
      });
    }
  };

  const finishGame = useCallback(() => {
    clearTimer();
    setPhase('finished');
    gameSession.endGame();
  }, [clearTimer, gameSession]);

  const handleTooSoonRestart = () => {
    setTooSoon(false);
    setPhase('waiting');
    scheduleNext();
  };

  const averageReaction = reactionTimes.length > 0
    ? Math.round(reactionTimes.reduce((a, b) => a + b, 0) / reactionTimes.length)
    : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-cyan-50 to-blue-100 p-4 md:p-8 flex flex-col items-center">
      <div className="w-full max-w-3xl text-center">
        <button
          onClick={onExit}
          className="mb-6 bg-white bg-opacity-70 hover:bg-opacity-100 text-gray-700 text-lg px-4 py-2 rounded-lg shadow transition"
        >
          ← Back to Games
        </button>

        {phase === 'setup' && (
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h1 className="text-4xl font-bold text-cyan-800 mb-6">Reaction Game</h1>
            <p className="text-xl text-gray-600 mb-8">Tap as fast as you can when the screen turns green</p>
            <div className="flex justify-center gap-4 mb-8">
              {['easy', 'medium', 'hard'].map((level) => (
                <button
                  key={level}
                  onClick={() => setDifficulty(level)}
                  className={`px-6 py-3 rounded-xl text-xl font-semibold capitalize transition ${
                    difficulty === level
                      ? 'bg-cyan-600 text-white shadow-lg'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  {level}
                </button>
              ))}
            </div>
            <button
              onClick={startGame}
              className="bg-green-500 hover:bg-green-600 text-white text-2xl font-bold px-8 py-4 rounded-xl shadow-lg transition transform hover:scale-105"
            >
              Start Game
            </button>
          </div>
        )}

        {phase === 'waiting' && (
          <div
            className="bg-yellow-200 rounded-2xl shadow-xl p-20 cursor-pointer select-none"
            onClick={handleTap}
          >
            <h2 className="text-5xl font-bold text-yellow-800">WAIT...</h2>
            <p className="text-xl text-yellow-700 mt-4">Tap only when green appears</p>
          </div>
        )}

        {phase === 'ready' && (
          <div
            className={`rounded-2xl shadow-xl p-20 cursor-pointer select-none transition-colors ${
              showDistractor ? 'bg-blue-500' : 'bg-green-500'
            }`}
            onClick={handleTap}
          >
            <h2 className="text-5xl font-bold text-white">
              {showDistractor ? 'BLUE!' : 'TAP!'}
            </h2>
            <p className="text-xl text-white mt-4">Tap now!</p>
          </div>
        )}

        {phase === 'tooSoon' && (
          <div className="bg-red-200 rounded-2xl shadow-xl p-8">
            <h2 className="text-4xl font-bold text-red-800 mb-4">Too Soon!</h2>
            <p className="text-xl text-red-700 mb-6">You tapped before the signal.</p>
            <button
              onClick={handleTooSoonRestart}
              className="bg-blue-600 hover:bg-blue-700 text-white text-xl font-bold px-6 py-3 rounded-xl shadow-lg transition"
            >
              Try Again
            </button>
          </div>
        )}

        {phase === 'finished' && (
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h2 className="text-4xl font-bold text-cyan-800 mb-6">Results</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
              <div className="bg-blue-50 rounded-xl p-4">
                <p className="text-2xl font-bold text-blue-700">{averageReaction} ms</p>
                <p className="text-lg text-blue-600">Average Reaction Time</p>
              </div>
              <div className="bg-green-50 rounded-xl p-4">
                <p className="text-2xl font-bold text-green-700">{reactionTimes.length}</p>
                <p className="text-lg text-green-600">Attempts Completed</p>
              </div>
            </div>
            <p className="text-xl text-gray-700 mb-6">Last Reaction: {lastReaction !== null ? `${lastReaction} ms` : 'N/A'}</p>
            <button
              onClick={() => setPhase('setup')}
              className="bg-green-500 hover:bg-green-600 text-white text-xl font-bold px-6 py-3 rounded-xl shadow-lg transition"
            >
              Play Again
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default ReactionGame;
'''

path = Path("frontend/src/games/ReactionGame.jsx")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(content.strip(), encoding='utf-8')
print("ReactionGame.jsx created successfully!")
