from pathlib import Path

content = '''// Voice utility with language support
import { getLanguage } from './translations';

export function speak(text, lang = null) {
  if (!('speechSynthesis' in window)) {
    console.warn('Speech synthesis not supported');
    return;
  }
  const language = lang || getLanguage();
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
  recognition.lang = lang || getLanguage();
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript.toLowerCase().trim();
    if (onResult) onResult(transcript);
  };

  recognition.onerror = (event) => {
    if (onError) onError(new Error(event.error));
  };

  recognition.onend = () => {
    recognition = null;
  };

  recognition.start();
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
print("voice.js updated with language support!")
