from pathlib import Path

content = '''import { useState } from 'react';
import { speak, startListening, stopListening } from '../services/voice';
import { t } from '../services/translations';

function PatientHome({ onNavigate, onLogout, language, onToggleLanguage }) {
  const [listening, setListening] = useState(false);
  const [voiceFeedback, setVoiceFeedback] = useState('');

  const handleVoiceCommand = () => {
    if (listening) {
      stopListening();
      setListening(false);
      setVoiceFeedback('');
      return;
    }
    setListening(true);
    setVoiceFeedback(t('listening'));
    speak(t('listening'));

    startListening(
      (transcript) => {
        setListening(false);
        setVoiceFeedback(`You said: "${transcript}"`);
        if (transcript.includes('game') || transcript.includes('play') || transcript.includes('ఆట')) {
          speak(t('opening_games'));
          onNavigate('games');
        } else if (transcript.includes('reminder') || transcript.includes('medicine') || transcript.includes('రిమైండర్')) {
          speak(t('opening_reminders'));
          onNavigate('reminders');
        } else if (transcript.includes('progress') || transcript.includes('report') || transcript.includes('పురోగతి')) {
          speak(t('opening_progress'));
          onNavigate('progress');
        } else if (transcript.includes('routine') || transcript.includes('daily') || transcript.includes('దినచర్య')) {
          speak(t('opening_routine'));
          onNavigate('routine');
        } else {
          speak(t('sorry_not_understand'));
        }
      },
      (error) => {
        console.error('Speech recognition error:', error);
        setListening(false);
        setVoiceFeedback(t('voice_error'));
        speak(t('voice_error'));
      }
    );
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <header className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-bold text-blue-800">{t('patient_home')}</h1>
        <div className="flex items-center gap-4">
          <button
            onClick={handleVoiceCommand}
            className={`p-4 rounded-full shadow-lg transition ${
              listening ? 'bg-red-500 animate-pulse' : 'bg-blue-500 hover:bg-blue-600'
            }`}
            title={t('voice_command')}
          >
            <span className="text-2xl">🎤</span>
          </button>
          <button
            onClick={onToggleLanguage}
            className="bg-gray-200 hover:bg-gray-300 text-xl px-4 py-2 rounded-xl"
          >
            {language === 'en' ? 'తెలుగు' : 'English'}
          </button>
          <button
            onClick={onLogout}
            className="bg-red-500 hover:bg-red-600 text-white text-xl px-6 py-3 rounded-xl"
          >
            {t('logout')}
          </button>
        </div>
      </header>

      {voiceFeedback && (
        <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-xl text-lg text-blue-800">
          {voiceFeedback}
        </div>
      )}

      <main className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <button
          onClick={() => onNavigate('games')}
          className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition text-center"
        >
          <span className="text-6xl">🧠</span>
          <p className="text-3xl font-semibold mt-4 text-gray-800">{t('play_games')}</p>
        </button>
        <button
          onClick={() => onNavigate('routine')}
          className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition text-center"
        >
          <span className="text-6xl">📅</span>
          <p className="text-3xl font-semibold mt-4 text-gray-800">{language === 'en' ? 'Daily Routine' : 'దినచర్య'}</p>
        </button>
        <button
          onClick={() => onNavigate('reminders')}
          className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition text-center"
        >
          <span className="text-6xl">💊</span>
          <p className="text-3xl font-semibold mt-4 text-gray-800">{t('reminders')}</p>
        </button>
        <button
          onClick={() => onNavigate('progress')}
          className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition text-center"
        >
          <span className="text-6xl">📊</span>
          <p className="text-3xl font-semibold mt-4 text-gray-800">{t('my_progress')}</p>
        </button>
      </main>
    </div>
  );
}

export default PatientHome;
'''

path = Path("frontend/src/pages/PatientHome.jsx")
path.write_text(content.strip(), encoding='utf-8')
print("PatientHome.jsx updated with routine button!")
