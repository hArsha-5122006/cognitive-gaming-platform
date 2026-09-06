from pathlib import Path

content = '''// Voice utility with language support and fallback
import { getLanguage } from './translations';

const localeMap = {
  en: 'en-US',
  te: 'te-IN'
};

export function speak(text, lang = null) {
  if (!('speechSynthesis' in window)) {
    console.warn('Speech synthesis not supported');
    return;
  }
  const language = lang || localeMap[getLanguage()] || 'en-US';
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = language;
  utterance.rate = 0.9;
  utterance.pitch = 1;
  window.speechSynthesis.speak(utterance);
}

let recognition = null;

export function startListening(onResult, onError, lang = null) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    const error = new Error('Speech recognition not supported in this browser');
    if (onError) onError(error);
    return null;
  }
  if (recognition) {
    recognition.abort();
  }
  recognition = new SpeechRecognition();
  recognition.lang = lang || localeMap[getLanguage()] || 'en-US';
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript.toLowerCase().trim();
    if (onResult) onResult(transcript);
  };

  recognition.onerror = (event) => {
    console.error('Speech recognition error:', event.error);
    // If language not supported, try English fallback
    if (event.error === 'language-not-supported' || event.error === 'not-allowed') {
      console.warn('Language not supported or permission denied. Falling back to English.');
      if (recognition) recognition.abort();
      recognition = null;
      // Retry with English
      const retryRec = new SpeechRecognition();
      retryRec.lang = 'en-US';
      retryRec.interimResults = false;
      retryRec.maxAlternatives = 1;
      retryRec.onresult = recognition.onresult;
      retryRec.onerror = (err) => {
        if (onError) onError(new Error(err.error));
      };
      retryRec.onend = () => { recognition = null; };
      recognition = retryRec;
      recognition.start();
    } else {
      if (onError) onError(new Error(event.error));
    }
  };

  recognition.onend = () => {
    recognition = null;
  };

  try {
    recognition.start();
  } catch (err) {
    console.error('Failed to start recognition:', err);
    if (onError) onError(err);
  }
  return recognition;
}

export function stopListening() {
  if (recognition) {
    recognition.abort();
    recognition = null;
  }
}
'''

path = Path("frontend/src/services/voice.js")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(content.strip(), encoding='utf-8')
print("voice.js updated with locale mapping and fallback!")
