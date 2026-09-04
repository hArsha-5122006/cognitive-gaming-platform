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
    const accuracy = attempts > 0 ? (attempts - mistakes) / attempts : 0;
    const resultData = {
      game_id: gameId,
      score,
      accuracy,
      time_taken_seconds: timeTaken,
      mistakes,
      attempts,
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
    }
  }, [isActive, sessionStartTime, attempts, mistakes, score, gameId, difficulty]);

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