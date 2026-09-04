from pathlib import Path

content = '''import { useState, useEffect, useRef, useCallback } from 'react';
import useGameSession from '../hooks/useGameSession';

// Sample question sets (emoji-based and sentence completion)
const EMOJI_QUESTIONS = [
  { emoji: '🍎', answer: 'Apple', hint: 'A red fruit' },
  { emoji: '🐶', answer: 'Dog', hint: 'A loyal pet' },
  { emoji: '☀️', answer: 'Sun', hint: 'Shines in the sky' },
  { emoji: '🌙', answer: 'Moon', hint: 'Appears at night' },
  { emoji: '🚗', answer: 'Car', hint: 'Has four wheels' },
  { emoji: '📚', answer: 'Book', hint: 'You read it' },
  { emoji: '☕', answer: 'Tea', hint: 'A hot drink' },
  { emoji: '🏠', answer: 'House', hint: 'Where you live' },
];

const SENTENCE_QUESTIONS = [
  { sentence: 'Today I went to ____.', answer: 'market', options: ['market', 'school', 'park'] },
  { sentence: 'I drink ____ every morning.', answer: 'water', options: ['water', 'coffee', 'juice'] },
  { sentence: 'The sun rises in the ____.', answer: 'east', options: ['east', 'west', 'north'] },
  { sentence: 'We sleep at ____.', answer: 'night', options: ['night', 'noon', 'morning'] },
  { sentence: 'A dog says ____.', answer: 'bow', options: ['bow', 'meow', 'moo'] },
];

const DIFFICULTY_SETTINGS = {
  easy: { timeLimit: 30, questionsPerRound: 3 },
  medium: { timeLimit: 20, questionsPerRound: 4 },
  hard: { timeLimit: 15, questionsPerRound: 5 },
};

function LanguageGame({ onExit }) {
  const gameSession = useGameSession(6, 'easy');
  const [difficulty, setDifficulty] = useState('easy');
  const [phase, setPhase] = useState('setup'); // setup, question, finished
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [userAnswer, setUserAnswer] = useState('');
  const [score, setScore] = useState({ correct: 0, wrong: 0 });
  const [timeLeft, setTimeLeft] = useState(0);
  const [totalQuestions, setTotalQuestions] = useState(0);
  const [questionStartTime, setQuestionStartTime] = useState(null);
  const [feedback, setFeedback] = useState(null); // 'correct' or 'wrong'
  const timerRef = useRef(null);

  useEffect(() => {
    return () => clearInterval(timerRef.current);
  }, []);

  const generateQuestions = useCallback(() => {
    const settings = DIFFICULTY_SETTINGS[difficulty];
    const emojiCount = Math.ceil(settings.questionsPerRound / 2);
    const sentenceCount = settings.questionsPerRound - emojiCount;
    let emojiQs = [...EMOJI_QUESTIONS].sort(() => Math.random() - 0.5).slice(0, emojiCount);
    let sentenceQs = [...SENTENCE_QUESTIONS].sort(() => Math.random() - 0.5).slice(0, sentenceCount);
    let combined = [...emojiQs.map(q => ({ type: 'emoji', ...q })), ...sentenceQs.map(q => ({ type: 'sentence', ...q }))];
    // Shuffle combined
    combined = combined.sort(() => Math.random() - 0.5);
    setQuestions(combined);
    setCurrentIndex(0);
    setTotalQuestions(combined.length);
  }, [difficulty]);

  const startGame = () => {
    generateQuestions();
    const settings = DIFFICULTY_SETTINGS[difficulty];
    setTimeLeft(settings.timeLimit);
    setScore({ correct: 0, wrong: 0 });
    setPhase('question');
    setQuestionStartTime(Date.now());
    gameSession.startGame();
  };

  const finishGame = useCallback(() => {
    clearInterval(timerRef.current);
    setPhase('finished');
    gameSession.endGame();
  }, [gameSession]);

  // Countdown timer
  useEffect(() => {
    if (phase !== 'question') return;
    timerRef.current = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          clearInterval(timerRef.current);
          finishGame();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(timerRef.current);
  }, [phase, finishGame]);

  const handleSubmit = () => {
    if (phase !== 'question') return;
    const currentQ = questions[currentIndex];
    let isCorrect = false;
    if (currentQ.type === 'emoji') {
      isCorrect = userAnswer.trim().toLowerCase() === currentQ.answer.toLowerCase();
    } else {
      // For sentence completion, we allow multiple choice? We'll use options but also accept typed answer
      const correctAnswer = currentQ.answer.toLowerCase();
      isCorrect = userAnswer.trim().toLowerCase() === correctAnswer ||
                  (currentQ.options && currentQ.options.some(opt => opt.toLowerCase() === userAnswer.trim().toLowerCase()));
    }

    const reaction = Date.now() - questionStartTime;
    gameSession.recordAnswer(
      currentQ.type === 'emoji' ? currentQ.emoji : currentQ.sentence,
      currentQ.answer,
      userAnswer,
      isCorrect ? 1 : 0,
      reaction
    );

    setScore(prev => ({
      correct: prev.correct + (isCorrect ? 1 : 0),
      wrong: prev.wrong + (isCorrect ? 0 : 1),
    }));
    setFeedback(isCorrect ? 'correct' : 'wrong');

    // Move to next question or finish
    if (currentIndex + 1 < questions.length) {
      setCurrentIndex(prev => prev + 1);
      setUserAnswer('');
      setQuestionStartTime(Date.now());
      setFeedback(null);
    } else {
      finishGame();
    }
  };

  const accuracy = (score.correct + score.wrong) > 0
    ? Math.round((score.correct / (score.correct + score.wrong)) * 100)
    : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-teal-50 to-emerald-100 p-4 md:p-8 flex flex-col items-center">
      <div className="w-full max-w-2xl">
        <button
          onClick={onExit}
          className="mb-6 bg-white bg-opacity-70 hover:bg-opacity-100 text-gray-700 text-lg px-4 py-2 rounded-lg shadow transition"
        >
          ← Back to Games
        </button>

        {phase === 'setup' && (
          <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
            <h1 className="text-4xl font-bold text-teal-800 mb-6">Language Recall</h1>
            <p className="text-xl text-gray-600 mb-8">Answer word and sentence questions</p>
            <div className="flex justify-center gap-4 mb-8">
              {['easy', 'medium', 'hard'].map((level) => (
                <button
                  key={level}
                  onClick={() => setDifficulty(level)}
                  className={`px-6 py-3 rounded-xl text-xl font-semibold capitalize transition ${
                    difficulty === level
                      ? 'bg-teal-600 text-white shadow-lg'
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
              <h2 className="text-2xl font-bold text-teal-800">
                Question {currentIndex + 1} of {questions.length}
              </h2>
              <div className="text-2xl font-bold text-red-600">Time: {timeLeft}s</div>
            </div>

            {questions[currentIndex]?.type === 'emoji' ? (
              <div className="mb-6">
                <p className="text-xl text-gray-600 mb-4">What is the name of this?</p>
                <div className="text-8xl mb-4">{questions[currentIndex].emoji}</div>
                <p className="text-lg text-gray-500 italic">{questions[currentIndex].hint}</p>
              </div>
            ) : (
              <div className="mb-6">
                <p className="text-3xl text-gray-800 font-medium mb-4">{questions[currentIndex]?.sentence}</p>
                {questions[currentIndex]?.options && (
                  <div className="flex justify-center gap-2 flex-wrap">
                    {questions[currentIndex].options.map(opt => (
                      <button
                        key={opt}
                        onClick={() => setUserAnswer(opt)}
                        className={`px-4 py-2 rounded-lg text-xl border-2 transition ${
                          userAnswer === opt
                            ? 'bg-teal-600 text-white border-teal-600'
                            : 'bg-white text-gray-700 border-gray-300 hover:border-teal-500'
                        }`}
                      >
                        {opt}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            )}

            <input
              type="text"
              value={userAnswer}
              onChange={(e) => setUserAnswer(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSubmit()}
              className="w-full p-4 text-2xl border-2 border-gray-300 rounded-xl focus:outline-none focus:border-teal-500 mb-6"
              placeholder="Type your answer"
            />

            {feedback && (
              <p className={`text-xl mb-4 ${feedback === 'correct' ? 'text-green-600' : 'text-red-600'}`}>
                {feedback === 'correct' ? '✓ Correct!' : '✗ Wrong!'}
              </p>
            )}

            <button
              onClick={handleSubmit}
              disabled={!userAnswer.trim()}
              className="bg-blue-600 hover:bg-blue-700 text-white text-xl font-bold px-6 py-3 rounded-xl shadow-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Submit
            </button>
          </div>
        )}

        {phase === 'finished' && (
          <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
            <h2 className="text-4xl font-bold text-teal-800 mb-6">Game Over!</h2>
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

export default LanguageGame;
'''

path = Path("frontend/src/games/LanguageGame.jsx")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(content.strip(), encoding='utf-8')
print("LanguageGame.jsx created successfully!")
