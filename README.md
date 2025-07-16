# MediVoxAI 🩺🤖

**MediVoxAI** is a next-generation Medical Chatbot powered by a Multimodal Large Language Model (LLM) with both Vision and Voice capabilities. MediVoxAI can converse with patients, understand spoken questions, analyze medical images, and respond with empathetic and informative answers — making healthcare assistance more accessible and interactive.

---

## Features

- **Multimodal LLM**: Handles both medical images and text inputs.
- **Speech-to-Text (STT)**: Records and transcribes patient voice input.
- **Text-to-Speech (TTS)**: Responds with realistic doctor voice output.
- **Intuitive UI**: User-friendly interface using Gradio.

---

## Project Layout

### Phase 1: Setup the Brain of the Doctor (Multimodal LLM)

- Configure GROQ API key for fast AI inference.
- Prepare images in required format.
- Integrate the Llama 3 Vision model for image and text understanding.

### Phase 2: Setup Voice of the Patient

- Set up audio recording using `ffmpeg` and `portaudio`.
- Implement speech-to-text transcription with OpenAI Whisper.

### Phase 3: Setup Voice of the Doctor

- Integrate TTS using `gTTS` and ElevenLabs.
- Convert model-generated text responses into human-like voice.

### Phase 4: User Interface

- Build an interactive UI with Gradio for seamless conversation.

---

## Technical Architecture



