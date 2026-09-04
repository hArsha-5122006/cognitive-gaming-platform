import { useState, useEffect, useRef } from 'react';
import useGameSession from '../hooks/useGameSession';

// Color palette for sequence (using Tailwind-friendly hex)
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

const DIFFICULTY_SETTINGS = {
  easy: { sequenceLength: 3, displayTime: 2500 },
  medium: { sequenceLength: 4, displayTime: 2500 },
  hard: { sequenceLength: 5, displayTime: 2500 },
};

function shuffleArray(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function SequenceGame({ onExit }) {
  const gameSession = useGameSession(2, 'easy');
  const [difficulty, setDifficulty] = useState('easy');
  const [phase, setPhase] = useState('setup'); // setup, show, input, finished
  const [sequence, setSequence] = useState([]); // array of color objects
  const [userInput, setUserInput] = useState([]); // array of color names
  const [reactionTimes, setReactionTimes] = useState([]); // per click times
  const [inputStartTime, setInputStartTime] = useState(null);
  const [lastClickTime, setLastClickTime] = useState(null);
  const [correctCount, setCorrectCount] = useState(0);
  const [incorrectCount, setIncorrectCount] = useState(0);
  const [totalTime, setTotalTime] = useState(0);

  const timerRef = useRef(null);

  // Cleanup timer on unmount
  useEffect(() => {
    return () => clearTimeout(timerRef.current);
  }, []);

  const startGame = () => {
    const settings = DIFFICULTY_SETTINGS[difficulty];
    // Generate random sequence
    const shuffled = shuffleArray(COLORS);
    const seq = shuffled.slice(0, settings.sequenceLength);
    setSequence(seq);
    setUserInput([]);
    setReactionTimes([]);
    setCorrectCount(0);
    setIncorrectCount(0);
    setTotalTime(0);
    setPhase('show');
    gameSession.startGame();

    // Automatically hide after displayTime
    timerRef.current = setTimeout(() => {
      setPhase('input');
      const now = Date.now();
      setInputStartTime(now);
      setLastClickTime(now);
    }, settings.displayTime);
  };

  const handleColorClick = (colorName) => {
    if (phase !== 'input') return;
    if (userInput.length >= sequence.length) return;

    const now = Date.now();
    const reactionTime = lastClickTime ? now - lastClickTime : now - inputStartTime;
    const newUserInput = [...userInput, colorName];
    const newReactionTimes = [...reactionTimes, reactionTime];

    setUserInput(newUserInput);
    setReactionTimes(newReactionTimes);
    setLastClickTime(now);

    // Check if completed
    if (newUserInput.length === sequence.length) {
      // Evaluate
      let correct = 0;
      let incorrect = 0;
      const answers = [];
      for (let i = 0; i < sequence.length; i++) {
        const isCorrect = newUserInput[i] === sequence[i].name;
        if (isCorrect) correct++;
        else incorrect++;
        answers.push({
          question: `Position ${i + 1}`,
          correct_answer: sequence[i].name,
          user_answer: newUserInput[i],
          is_correct: isCorrect ? 1 : 0,
          reaction_time_ms: newReactionTimes[i],
        });
      }
      // Record each answer
      answers.forEach((a) => {
        gameSession.recordAnswer(a.question, a.correct_answer, a.user_answer, a.is_correct === 1, a.reaction_time_ms);
      });
      setCorrectCount(correct);
      setIncorrectCount(incorrect);
      setTotalTime((Date.now() - inputStartTime) / 1000);
      setPhase('finished');
      gameSession.endGame();
    }
  };

  const accuracy = sequence.length > 0 ? Math.round((correctCount / sequence.length) * 100) : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-100 p-4 md:p-8 flex flex-col items-center">
      <div className="w-full max-w-3xl">
        <button
          onClick={onExit}
          className="mb-6 bg-white bg-opacity-70 hover:bg-opacity-100 text-gray-700 text-lg px-4 py-2 rounded-lg shadow transition"
        >
          ← Back to Games
        </button>

        {phase === 'setup' && (
          <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
            <h1 className="text-4xl font-bold text-purple-800 mb-6">Sequence Recall</h1>
            <p className="text-xl text-gray-600 mb-8">Remember the order of colors</p>
            <div className="flex justify-center gap-4 mb-8">
              {['easy', 'medium', 'hard'].map((level) => (
                <button
                  key={level}
                  onClick={() => setDifficulty(level)}
                  className={`px-6 py-3 rounded-xl text-xl font-semibold capitalize transition ${
                    difficulty === level
                      ? 'bg-purple-600 text-white shadow-lg'
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

        {phase === 'show' && (
          <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
            <h2 className="text-3xl font-bold text-purple-800 mb-6">Watch the sequence!</h2>
            <div className="flex justify-center gap-4 flex-wrap">
              {sequence.map((color, idx) => (
                <div
                  key={idx}
                  className="w-24 h-24 rounded-full shadow-lg animate-pulse"
                  style={{ backgroundColor: color.color }}
                ></div>
              ))}
            </div>
            <p className="mt-6 text-lg text-gray-500">Memorize the order...</p>
          </div>
        )}

        {phase === 'input' && (
          <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
            <h2 className="text-3xl font-bold text-purple-800 mb-4">Repeat the sequence</h2>
            <p className="text-lg text-gray-600 mb-6">Click the colors in the same order</p>

            {/* Progress dots showing how many inputs done */}
            <div className="flex justify-center gap-2 mb-6">
              {Array.from({ length: sequence.length }, (_, i) => (
                <div
                  key={i}
                  className={`w-6 h-6 rounded-full ${
                    i < userInput.length ? 'bg-purple-600' : 'bg-gray-300'
                  }`}
                ></div>
              ))}
            </div>

            {/* Color buttons */}
            <div className="flex justify-center gap-4 flex-wrap mb-8">
              {COLORS.map((color) => (
                <button
                  key={color.name}
                  onClick={() => handleColorClick(color.name)}
                  className="w-20 h-20 rounded-full shadow-lg transition transform hover:scale-110 focus:outline-none"
                  style={{ backgroundColor: color.color }}
                  disabled={userInput.length >= sequence.length}
                ></button>
              ))}
            </div>

            <button
              onClick={() => {
                // Reset input for the same sequence (allow retry)
                setUserInput([]);
                setReactionTimes([]);
                const now = Date.now();
                setInputStartTime(now);
                setLastClickTime(now);
              }}
              className="text-lg text-blue-600 underline"
            >
              Reset Input
            </button>
          </div>
        )}

        {phase === 'finished' && (
          <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
            <h2 className="text-4xl font-bold text-purple-800 mb-6">Result</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
              <div className="bg-green-50 rounded-xl p-4">
                <p className="text-2xl font-bold text-green-700">{correctCount}</p>
                <p className="text-lg text-green-600">Correct</p>
              </div>
              <div className="bg-red-50 rounded-xl p-4">
                <p className="text-2xl font-bold text-red-700">{incorrectCount}</p>
                <p className="text-lg text-red-600">Incorrect</p>
              </div>
              <div className="bg-blue-50 rounded-xl p-4">
                <p className="text-2xl font-bold text-blue-700">{accuracy}%</p>
                <p className="text-lg text-blue-600">Accuracy</p>
              </div>
            </div>
            <p className="text-xl text-gray-700 mb-6">Total Time: {totalTime.toFixed(1)} sec</p>
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

export default SequenceGame;