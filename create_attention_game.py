from pathlib import Path

content = '''import { useState, useEffect, useRef, useCallback } from 'react';
import useGameSession from '../hooks/useGameSession';

// Item pool (emoji + name)
const ITEMS = [
  { emoji: '🍎', name: 'Apple' },
  { emoji: '🍌', name: 'Banana' },
  { emoji: '🚗', name: 'Car' },
  { emoji: '🏠', name: 'House' },
  { emoji: '🌸', name: 'Flower' },
  { emoji: '🐶', name: 'Dog' },
  { emoji: '🐱', name: 'Cat' },
  { emoji: '🌳', name: 'Tree' },
  { emoji: '🚲', name: 'Bicycle' },
  { emoji: '📚', name: 'Book' },
  { emoji: '🎵', name: 'Music' },
  { emoji: '☕', name: 'Tea' },
  { emoji: '🌾', name: 'Rice' },
  { emoji: '🛕', name: 'Temple' },
  { emoji: '🐘', name: 'Elephant' },
  { emoji: '🌺', name: 'Hibiscus' },
];

// Difficulty settings: gridSize (total items), targetCount (number of targets), timeLimit (seconds)
const DIFFICULTY_SETTINGS = {
  easy: { gridSize: 9, targetCount: 3, timeLimit: 30 },
  medium: { gridSize: 16, targetCount: 4, timeLimit: 20 },
  hard: { gridSize: 25, targetCount: 5, timeLimit: 10 },
};

function shuffleArray(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function AttentionGame({ onExit }) {
  const gameSession = useGameSession(3, 'easy');
  const [difficulty, setDifficulty] = useState('easy');
  const [phase, setPhase] = useState('setup'); // setup, playing, finished
  const [grid, setGrid] = useState([]); // array of items (some are target)
  const [targetItem, setTargetItem] = useState(null); // item object
  const [taps, setTaps] = useState([]); // { item, isCorrect, reactionTime }
  const [timeLeft, setTimeLeft] = useState(0);
  const [startTime, setStartTime] = useState(null);
  const [lastTapTime, setLastTapTime] = useState(null);
  const [correctTaps, setCorrectTaps] = useState(0);
  const [wrongTaps, setWrongTaps] = useState(0);
  const [missedTargets, setMissedTargets] = useState(0);
  const [completionTime, setCompletionTime] = useState(0);

  const timerRef = useRef(null);

  // Cleanup timer on unmount
  useEffect(() => {
    return () => clearInterval(timerRef.current);
  }, []);

  const startGame = () => {
    const settings = DIFFICULTY_SETTINGS[difficulty];
    // Choose target item
    const target = ITEMS[Math.floor(Math.random() * ITEMS.length)];
    setTargetItem(target);

    // Generate grid: shuffle all items, pick gridSize items
    const shuffled = shuffleArray(ITEMS);
    const baseItems = shuffled.slice(0, settings.gridSize);
    // Place targetCount targets randomly among grid
    // First remove any existing target from base (to avoid duplication)
    const nonTargetItems = baseItems.filter((item) => item.name !== target.name);
    // If we removed too many, we may need to fill from remaining ITEMS
    let fillItems = [...nonTargetItems];
    while (fillItems.length < settings.gridSize - settings.targetCount) {
      const extra = shuffleArray(ITEMS).find((item) => item.name !== target.name);
      fillItems.push(extra);
    }
    // Take first needed non-target items
    const finalNonTargets = fillItems.slice(0, settings.gridSize - settings.targetCount);
    // Create target objects
    const targets = Array.from({ length: settings.targetCount }, () => ({ ...target }));
    const allGridItems = shuffleArray([...targets, ...finalNonTargets]);
    setGrid(allGridItems);
    setTaps([]);
    setCorrectTaps(0);
    setWrongTaps(0);
    setMissedTargets(0);
    setCompletionTime(0);
    setTimeLeft(settings.timeLimit);
    setPhase('playing');
    gameSession.startGame();
    const now = Date.now();
    setStartTime(now);
    setLastTapTime(now);

    // Start countdown
    timerRef.current = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timerRef.current);
          endGame();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  const endGame = useCallback(() => {
    clearInterval(timerRef.current);
    if (phase !== 'playing') return;
    const endTime = Date.now();
    const totalTime = (endTime - startTime) / 1000;
    setCompletionTime(totalTime);

    // Determine missed targets
    const targetTaps = taps.filter((t) => t.isCorrect).length;
    const totalTargets = DIFFICULTY_SETTINGS[difficulty].targetCount;
    const missed = Math.max(0, totalTargets - targetTaps);
    setMissedTargets(missed);
    setCorrectTaps(targetTaps);
    setWrongTaps(taps.filter((t) => !t.isCorrect).length);

    // Record each tap as answer in session
    taps.forEach((t) => {
      gameSession.recordAnswer(
        t.item.name,
        t.isCorrect ? t.item.name : 'Not target',
        t.item.name,
        t.isCorrect ? 1 : 0,
        t.reactionTime
      );
    });

    // End session
    gameSession.endGame();
    setPhase('finished');
  }, [phase, startTime, taps, difficulty, gameSession]);

  const handleItemTap = (item) => {
    if (phase !== 'playing') return;
    const now = Date.now();
    const reaction = lastTapTime ? now - lastTapTime : now - startTime;
    const isCorrect = item.name === targetItem.name;
    const newTap = { item, isCorrect, reactionTime: reaction };
    setTaps((prev) => [...prev, newTap]);
    setLastTapTime(now);

    // Provide visual feedback (optional: could add temporary state)
    // We'll just rely on the state change for animation classes in the grid
  };

  const handleFinishEarly = () => {
    endGame();
  };

  const accuracy = (correctTaps + wrongTaps + missedTargets) > 0
    ? Math.round((correctTaps / (correctTaps + wrongTaps + missedTargets)) * 100)
    : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-50 to-orange-100 p-4 md:p-8 flex flex-col items-center">
      <div className="w-full max-w-4xl">
        <button
          onClick={onExit}
          className="mb-6 bg-white bg-opacity-70 hover:bg-opacity-100 text-gray-700 text-lg px-4 py-2 rounded-lg shadow transition"
        >
          ← Back to Games
        </button>

        {phase === 'setup' && (
          <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
            <h1 className="text-4xl font-bold text-orange-800 mb-6">Attention Game</h1>
            <p className="text-xl text-gray-600 mb-8">Find and tap all the target objects</p>
            <div className="flex justify-center gap-4 mb-8">
              {['easy', 'medium', 'hard'].map((level) => (
                <button
                  key={level}
                  onClick={() => setDifficulty(level)}
                  className={`px-6 py-3 rounded-xl text-xl font-semibold capitalize transition ${
                    difficulty === level
                      ? 'bg-orange-600 text-white shadow-lg'
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

        {phase === 'playing' && (
          <div className="bg-white rounded-2xl shadow-xl p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-orange-800">
                Tap all: <span className="text-4xl">{targetItem?.emoji}</span> {targetItem?.name}
              </h2>
              <div className="text-2xl font-bold text-red-600">Time: {timeLeft}s</div>
            </div>

            {/* Grid of items */}
            <div
              className="grid gap-3"
              style={{
                gridTemplateColumns: `repeat(${Math.ceil(Math.sqrt(grid.length))}, 1fr)`,
              }}
            >
              {grid.map((item, idx) => (
                <button
                  key={idx}
                  onClick={() => handleItemTap(item)}
                  className="aspect-square rounded-xl bg-gray-50 hover:bg-gray-100 flex flex-col items-center justify-center transition transform hover:scale-105 active:scale-95 shadow-md"
                >
                  <span className="text-4xl md:text-5xl">{item.emoji}</span>
                  <span className="text-sm md:text-base text-gray-600 mt-1">{item.name}</span>
                </button>
              ))}
            </div>

            <div className="flex justify-center mt-6">
              <button
                onClick={handleFinishEarly}
                className="bg-blue-600 hover:bg-blue-700 text-white text-xl font-bold px-6 py-3 rounded-xl shadow-lg transition"
              >
                Finish Now
              </button>
            </div>
          </div>
        )}

        {phase === 'finished' && (
          <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
            <h2 className="text-4xl font-bold text-orange-800 mb-6">Game Over!</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
              <div className="bg-green-50 rounded-xl p-4">
                <p className="text-2xl font-bold text-green-700">{correctTaps}</p>
                <p className="text-lg text-green-600">Correct Taps</p>
              </div>
              <div className="bg-red-50 rounded-xl p-4">
                <p className="text-2xl font-bold text-red-700">{wrongTaps}</p>
                <p className="text-lg text-red-600">Wrong Taps</p>
              </div>
              <div className="bg-yellow-50 rounded-xl p-4">
                <p className="text-2xl font-bold text-yellow-700">{missedTargets}</p>
                <p className="text-lg text-yellow-600">Missed Targets</p>
              </div>
              <div className="bg-blue-50 rounded-xl p-4">
                <p className="text-2xl font-bold text-blue-700">{accuracy}%</p>
                <p className="text-lg text-blue-600">Accuracy</p>
              </div>
            </div>
            <p className="text-xl text-gray-700 mb-6">Completion Time: {completionTime.toFixed(1)} sec</p>
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

export default AttentionGame;
'''

path = Path("frontend/src/games/AttentionGame.jsx")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(content.strip(), encoding='utf-8')
print("AttentionGame.jsx created successfully!")
