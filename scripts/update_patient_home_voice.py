from pathlib import Path

content = '''import { useState } from 'react';
import { speak, startListening, stopListening } from '../services/voice';

function PatientHome({ onNavigate, onLogout }) {
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
    setVoiceFeedback('Listening...');
    speak('Listening. Please say a command.');

    startListening(
      (transcript) => {
        setListening(false);
        setVoiceFeedback(`You said: "${transcript}"`);
        // Process command
        if (transcript.includes('game') || transcript.includes('play')) {
          speak('Opening games.');
          onNavigate('games');
        } else if (transcript.includes('reminder') || transcript.includes('medicine')) {
          speak('Opening reminders.');
          onNavigate('reminders');
        } else if (transcript.includes('progress') || transcript.includes('report')) {
          speak('Opening progress.');
          onNavigate('progress');
        } else {
          speak('Sorry, I did not understand. Please try again.');
        }
      },
      (error) => {
        console.error('Speech recognition error:', error);
        setListening(false);
        setVoiceFeedback('Voice recognition error.');
        speak('Voice recognition error. Please try again.');
      }
    );
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <header className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-bold text-blue-800">Hello!</h1>
        <div className="flex items-center gap-4">
          <button
            onClick={handleVoiceCommand}
            className={`p-4 rounded-full shadow-lg transition ${
              listening ? 'bg-red-500 animate-pulse' : 'bg-blue-500 hover:bg-blue-600'
            }`}
            title="Voice command"
          >
            <span className="text-2xl">🎤</span>
          </button>
          <button
            onClick={onLogout}
            className="bg-red-500 hover:bg-red-600 text-white text-xl px-6 py-3 rounded-xl"
          >
            Logout
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
          <p className="text-3xl font-semibold mt-4 text-gray-800">Play Games</p>
        </button>
        <button
          onClick={() => onNavigate('reminders')}
          className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition text-center"
        >
          <span className="text-6xl">💊</span>
          <p className="text-3xl font-semibold mt-4 text-gray-800">Reminders</p>
        </button>
        <button
          onClick={() => onNavigate('progress')}
          className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition text-center"
        >
          <span className="text-6xl">📊</span>
          <p className="text-3xl font-semibold mt-4 text-gray-800">My Progress</p>
        </button>
      </main>
    </div>
  );
}

export default PatientHome;
'''

path = Path("frontend/src/pages/PatientHome.jsx")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(content.strip(), encoding='utf-8')
print("PatientHome.jsx updated with voice command!")
