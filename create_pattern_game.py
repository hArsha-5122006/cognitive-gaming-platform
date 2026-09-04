from pathlib import Path

content = '''import { useState, useEffect, useRef } from 'react';
import useGameSession from '../hooks/useGameSession';

// Color palette for pattern elements
const COLORS = [
  { name: 'Red', color: '#EF4444' },
  { name: 'Blue', color: '#3B82F6' },
  { name: 'Green', color: '#22C55E' },
  { name: 'Yellow', color: '#EAB308' },
  { name: 'Purple', color: '#A855F7' },
  { name: 'Orange', color: '#F97316' },
  { name: 'Pink', color: '#EC4899' },
  { name: 'Teal', color: '#14B8A6' },
];

// Difficulty settings: pattern length, options count, time limit per question
const DIFFICULTY_SETTINGS = {
  easy: { patternLength: 4, optionsCount: 3, timeLimit: 30 },
  medium: { patternLength: 6, optionsCount: 4, timeLimit: 25 },
  hard: { patternLength: 8, optionsCount: 5, timeLimit: 20 },
};

function shuffleArray(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// Generate a simple repeating pattern (e.g., A B A B ...)
function generatePattern(length) {
  const pattern = [];
  const availableColors = shuffleArray(COLORS);
  for (let i = 0; i < length; i++) {
    pattern.push(availableColors[i % 2]); // alternate between first two colors
  }
  return pattern;
}

function PatternGame({ onExit }) {
  const gameSession = useGameSession(4, 'easy');
  const [difficulty, setDifficulty] = useState('easy');
  const [phase, setPhase] = useState('setup'); // setup, question, finished
  const [pattern, setPattern] = useState([]); // full pattern array
  const [hiddenIndex, setHiddenIndex] = useState(null); // index that is hidden
  const [options, setOptions] = useState([]); // color choices
  const [correctAnswer, setCorrectAnswer] = useState(null); // correct color object
  const [score, setScore] = useState({ correct: 0, wrong: 0 });
  const [questionStartTime, setQuestionStartTime] = useState(null);
  const [reactionTimes, setReactionTimes] = useState([]);
  const [timeLeft, setTimeLeft] = useState(0);
  const [totalQuestions, setTotalQuestions] = useState(0);
  const timerRef = useRef(null);

  // Cleanup timer on unmount
  useEffect(() => {
    return () => clearInterval(timerRef.current);
  }, []);

  const startGame = () => {
    const settings = DIFFICULTY_SETTINGS[difficulty];
    const pat = generatePattern(settings.patternLength);
    // Hide a random index (not first or last to keep pattern obvious)
    const hideIdx = Math.floor(Math.random() * (settings.patternLength - 2)) + 1;
    const correct = pat[hideIdx];
    // Generate options: correct color + distractors
    const otherColors = COLORS.filter((c) => c.name !== correct.name);
    const distractors = shuffleArray(otherColors).slice(0, settings.optionsCount - 1);
    const opts = shuffleArray([correct, ...distractors]);

    setPattern(pat);
    setHiddenIndex(hideIdx);
    setCorrectAnswer(correct);
    setOptions(opts);
    setScore({ correct: 0, wrong: 0 });
    setReactionTimes([]);
    setTotalQuestions(0);
    setTimeLeft(settings.timeLimit);
    setPhase('question');
    const now = Date.now();
    setQuestionStartTime(now);
    gameSession.startGame();

    timerRef.current = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timerRef.current);
          finishGame();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  const handleAnswer = (selectedColor) => {
    if (phase !== 'question') return;
    const now = Date.now();
    const reaction = questionStartTime ? now - questionStartTime : 0;
    const isCorrect = selectedColor.name === correctAnswer.name;
    setReactionTimes((prev) => [...prev, reaction]);
    setScore((prev) => ({
      correct: prev.correct + (isCorrect ? 1 : 0),
      wrong: prev.wrong + (isCorrect ? 0 : 1),
    }));

    // Record answer
    gameSession.recordAnswer(
      `Missing element in pattern`,
      correctAnswer.name,
      selectedColor.name,
      isCorrect ? 1 : 0,
      reaction
    );

    // Generate next question (similar to start but keep same difficulty)
    const settings = DIFFICULTY_SETTINGS[difficulty];
    const pat = generatePattern(settings.patternLength);
    const hideIdx = Math.floor(Math.random() * (settings.patternLength - 2)) + 1;
    const correct = pat[hideIdx];
    const otherColors = COLORS.filter((c) => c.name !== correct.name);
    const distractors = shuffleArray(otherColors).slice(0, settings.optionsCount - 1);
    const opts = shuffleArray([correct, ...distractors]);
    setPattern(pat);
    setHiddenIndex(hideIdx);
    setCorrectAnswer(correct);
    setOptions(opts);
    setTotalQuestions((prev) => prev + 1);
    setQuestionStartTime(Date.now());
  };

  const finishGame = () => {
    clearInterval(timerRef.current);
    if (phase !== 'question') return;
    setPhase('finished');
    gameSession.endGame();
  };

  const accuracy = (score.correct + score.wrong) > 0
    ? Math.round((score.correct / (score.correct + score.wrong)) * 100)
    : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 to-rose-100 p-4 md:p-8 flex flex-col items-center">
      <div className="w-full max-w-3xl">
        <button
          onClick={onExit}
          className="mb-6 bg-white bg-opacity-70 hover:bg-opacity-100 text-gray-700 text-lg px-4 py-2 rounded-lg shadow transition"
        >
          ← Back to Games
        </button>

        {phase === 'setup' && (
          <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
            <h1 className="text-4xl font-bold text-rose-800 mb-6">Pattern Recognition</h1>
            <p className="text-xl text-gray-600 mb-8">Find the missing element in the pattern</p>
            <div className="flex justify-center gap-4 mb-8">
              {['easy', 'medium', 'hard'].map((level) => (
                <button
                  key={level}
                  onClick={() => setDifficulty(level)}
                  className={`px-6 py-3 rounded-xl text-xl font-semibold capitalize transition ${
                    difficulty === level
                      ? 'bg-rose-600 text-white shadow-lg'
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

        {phase === 'question' && (
          <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-rose-800">Complete the pattern</h2>
              <div className="text-2xl font-bold text-red-600">Time: {timeLeft}s</div>
            </div>

            {/* Pattern display with missing element */}
            <div className="flex justify-center gap-3 mb-10 flex-wrap">
              {pattern.map((color, idx) => (
                <div
                  key={idx}
                  className="w-16 h-16 md:w-20 md:h-20 rounded-full shadow-lg"
                  style={{
                    backgroundColor: idx === hiddenIndex ? '#E5E7EB' : color.color,
                    border: idx === hiddenIndex ? '3px dashed #9CA3AF' : 'none',
                  }}
                >
                  {idx === hiddenIndex && (
                    <span className="text-4xl text-gray-400 flex items-center justify-center h-full">?</span>
                  )}
                </div>
              ))}
            </div>

            {/* Options */}
            <div className="flex justify-center gap-4 flex-wrap mb-8">
              {options.map((color) => (
                <button
                  key={color.name}
                  onClick={() => handleAnswer(color)}
                  className="w-20 h-20 rounded-full shadow-lg transition transform hover:scale-110 focus:outline-none"
                  style={{ backgroundColor: color.color }}
                ></button>
              ))}
            </div>

            <p className="text-lg text-gray-600">
              Score: {score.correct} correct, {score.wrong} wrong
            </p>
          </div>
        )}

        {phase === 'finished' && (
          <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
            <h2 className="text-4xl font-bold text-rose-800 mb-6">Game Over!</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
              <div className="bg-green-50 rounded-xl p-4">
                <p className="text-2xl font-bold text-green-700">{score.correct}</p>
                <p className="text-lg text-green-600">Correct</p>
              </div>
              <div className="bg-red-50 rounded-xl p-4">
                <p className="text-2xl font-bold text-red-700">{score.wrong}</p>
                <p className="text-lg text-red-600">Wrong</p>
              </div>
              <div className="bg-blue-50 rounded-xl p-4">
                <p className="text-2xl font-bold text-blue-700">{accuracy}%</p>
                <p className="text-lg text-blue-600">Accuracy</p>
              </div>
            </div>
            <p className="text-xl text-gray-700 mb-6">Total Questions: {totalQuestions + 1}</p>
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

export default PatternGame;
'''

path = Path("frontend/src/games/PatternGame.jsx")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(content.strip(), encoding='utf-8')
print("PatternGame.jsx created successfully!")
