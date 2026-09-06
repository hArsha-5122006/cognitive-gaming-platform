from pathlib import Path

content = '''// translations.js
export const translations = {
  en: {
    login: 'Login',
    welcome: 'Welcome',
    patient_home: 'Hello!',
    play_games: 'Play Games',
    reminders: 'Reminders',
    my_progress: 'My Progress',
    choose_game: 'Choose a Game',
    memory_game: 'Memory Game',
    sequence_game: 'Sequence Game',
    attention_game: 'Attention Game',
    pattern_game: 'Pattern Game',
    reaction_game: 'Reaction Game',
    language_game: 'Language Game',
    logout: 'Logout',
    voice_command: 'Voice command',
    listening: 'Listening...',
    opening_games: 'Opening games.',
    opening_reminders: 'Opening reminders.',
    opening_progress: 'Opening progress.',
    sorry_not_understand: 'Sorry, I did not understand. Please try again.',
    voice_error: 'Voice recognition error. Please try again.',
    remember_objects: 'Remember these objects.',
    which_objects: 'Which objects did you see? Select all that you remember.',
    game_over: 'Game over.',
    correct: 'Correct',
    wrong: 'Wrong',
    accuracy: 'Accuracy',
    play_again: 'Play Again',
    start_game: 'Start Game',
    difficulty: 'Difficulty',
    easy: 'Easy',
    medium: 'Medium',
    hard: 'Hard',
    submit_answers: 'Submit Answers',
    memory_instruction_show: 'Remember these objects!',
    memory_instruction_select: 'Which objects did you see?',
    memory_instruction_hint: 'Select all that you remember',
    back_to_games: 'Back to Games',
  },
  te: {
    login: 'లాగిన్',
    welcome: 'స్వాగతం',
    patient_home: 'నమస్కారం!',
    play_games: 'ఆటలు ఆడండి',
    reminders: 'రిమైండర్లు',
    my_progress: 'నా పురోగతి',
    choose_game: 'ఆటను ఎంచుకోండి',
    memory_game: 'మెమరీ గేమ్',
    sequence_game: 'సీక్వెన్స్ గేమ్',
    attention_game: 'అటెన్షన్ గేమ్',
    pattern_game: 'ప్యాటర్న్ గేమ్',
    reaction_game: 'రియాక్షన్ గేమ్',
    language_game: 'భాషా గేమ్',
    logout: 'లాగ్అవుట్',
    voice_command: 'వాయిస్ కమాండ్',
    listening: 'వింటున్నాను...',
    opening_games: 'ఆటలను తెరుస్తున్నాను.',
    opening_reminders: 'రిమైండర్లను తెరుస్తున్నాను.',
    opening_progress: 'పురోగతిని తెరుస్తున్నాను.',
    sorry_not_understand: 'క్షమించండి, నాకు అర్థం కాలేదు. దయచేసి మళ్లీ ప్రయత్నించండి.',
    voice_error: 'వాయిస్ గుర్తింపు లోపం. దయచేసి మళ్లీ ప్రయత్నించండి.',
    remember_objects: 'ఈ వస్తువులను గుర్తుంచుకోండి.',
    which_objects: 'మీరు ఏ వస్తువులను చూశారు? మీకు గుర్తున్నవన్నీ ఎంచుకోండి.',
    game_over: 'ఆట ముగిసింది.',
    correct: 'సరైనవి',
    wrong: 'తప్పులు',
    accuracy: 'ఖచ్చితత్వం',
    play_again: 'మళ్లీ ఆడండి',
    start_game: 'ఆట ప్రారంభించండి',
    difficulty: 'కష్టం',
    easy: 'సులభం',
    medium: 'మధ్యస్థం',
    hard: 'కష్టం',
    submit_answers: 'సమాధానాలు సమర్పించండి',
    memory_instruction_show: 'ఈ వస్తువులను గుర్తుంచుకోండి!',
    memory_instruction_select: 'మీరు ఏ వస్తువులను చూశారు?',
    memory_instruction_hint: 'మీకు గుర్తున్నవన్నీ ఎంచుకోండి',
    back_to_games: 'ఆటలకు తిరిగి వెళ్ళు',
  }
};

export const getLanguage = () => {
  return localStorage.getItem('language') || 'en';
};

export const setLanguage = (lang) => {
  localStorage.setItem('language', lang);
};

export const t = (key) => {
  const lang = getLanguage();
  return translations[lang]?.[key] || translations.en[key] || key;
};
'''

path = Path("frontend/src/services/translations.js")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(content.strip(), encoding='utf-8')
print("translations.js created!")
