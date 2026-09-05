// Voice utility: Text-to-Speech (TTS) and Speech-to-Text (STT)

// TTS
export function speak(text, lang = 'en-US') {
  if (!('speechSynthesis' in window)) {
    console.warn('Speech synthesis not supported');
    return;
  }
  // Cancel any ongoing speech
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = lang;
  utterance.rate = 0.9; // slightly slower for elderly
  utterance.pitch = 1;
  window.speechSynthesis.speak(utterance);
}

// STT
let recognition = null;

export function startListening(onResult, onError, lang = 'en-US') {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    const error = new Error('Speech recognition not supported in this browser');
    if (onError) onError(error);
    return null;
  }

  // Stop any existing recognition
  if (recognition) {
    recognition.abort();
  }

  recognition = new SpeechRecognition();
  recognition.lang = lang;
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