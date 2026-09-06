import { useState, useRef, useCallback } from 'react';
import { api } from '../services/api';

const useGameSession = (gameId, initialDifficulty = 'easy') => {
  const [difficulty, setDifficulty] = useState(initialDifficulty);
  const [score, setScore] = useState(0);
  const [attempts, setAttempts] = useState(0);
  const [mistakes, setMistakes] = useState(0);
  const [isActive, setIsActive] = useState(false);
  const [sessionStartTime, setSessionStartTime] = useState(null);
  const resultsRef = useRef([]);

  const startGame = useCallback(() => {
    setScore(0);
    setAttempts(0);
    setMistakes(0);
    resultsRef.current = [];
    setSessionStartTime(Date.now());
    setIsActive(true);
  }, []);

  const recordAnswer = useCallback((question, correctAnswer, userAnswer, isCorrect, reactionTimeMs) => {
    setAttempts(prev => prev + 1);
    if (!isCorrect) setMistakes(prev => prev + 1);
    if (isCorrect) setScore(prev => prev + 1);
    resultsRef.current.push({
      question,
      correct_answer: correctAnswer,
      user_answer: userAnswer,
      is_correct: isCorrect ? 1 : 0,
      reaction_time_ms: reactionTimeMs,
    });
  }, []);

  const endGame = useCallback(async () => {
    if (!isActive) return;
    const endTime = Date.now();
    const timeTaken = (endTime - sessionStartTime) / 1000;
    setIsActive(false);

    const totalAttempts = resultsRef.current.length;
    const totalMistakes = resultsRef.current.filter(r => r.is_correct === 0).length;
    const totalCorrect = totalAttempts - totalMistakes;
    const accuracy = totalAttempts > 0 ? totalCorrect / totalAttempts : 0;
    const scoreValue = totalCorrect;

    const resultData = {
      game_id: gameId,
      score: scoreValue,
      accuracy,
      time_taken_seconds: timeTaken,
      mistakes: totalMistakes,
      attempts: totalAttempts,
      difficulty_level: difficulty,
      results: resultsRef.current,
    };

    try {
      const token = localStorage.getItem('token');
      if (!token) throw new Error('No token');
      await api.submitGameResult(token, resultData);
      console.log('Result submitted successfully');
    } catch (error) {
      console.error('Failed to submit result:', error);
      api.savePendingResult(resultData);
    }
  }, [isActive, sessionStartTime, gameId, difficulty]);

  return {
    difficulty,
    setDifficulty,
    score,
    attempts,
    mistakes,
    isActive,
    startGame,
    recordAnswer,
    endGame,
  };
};

export default useGameSession;
