# MediVoxAI 🩺🤖

**MediVoxAI** is a next-generation Medical Chatbot powered by a Multimodal Large Language Model (LLM) with both Vision and Voice capabilities. MediVoxAI can converse with patients, understand spoken questions, analyze medical images, and respond with empathetic and informative answers — making healthcare assistance more accessible and interactive.
**LINK:** https://huggingface.co/spaces/jv456/MediVoxAI

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

<img width="1495" height="1333" alt="diagram-export-7-17-2025-1_27_28-AM" src="https://github.com/user-attachments/assets/16bb78fa-0d28-4eae-aa29-b4590de7ba71" />

---

## How It Works

1. **User speaks or uploads an image** via the Gradio UI.
2. **Voice input is transcribed** to text using Whisper.
3. **Image and text** are processed by the multimodal LLM (Llama 3 Vision).
4. **AI generates response** as text.
5. **Doctor's response is converted to voice** using TTS and played back.
6. **All interaction happens in a web UI** (Gradio).

---

## Tools and Technologies

- **Groq** for AI Inference
- **OpenAI Whisper** for transcription
- **Llama 3 Vision** for multimodal understanding
- **gTTS & ElevenLabs** for speech synthesis
- **Gradio** for UI
- **Python, VS Code**

---

## Output

<img width="1643" height="865" alt="Screenshot 2025-07-17 105312" src="https://github.com/user-attachments/assets/cdfdb340-e235-4ba3-a6fa-f00bc1024171" />

---

## ⭐ Support

If you like this project, please give it a star!


