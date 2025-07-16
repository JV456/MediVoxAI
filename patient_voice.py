import logging
import os
import tempfile
import wave

import lameenc
import speech_recognition as sr

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Record audio and save as MP3 using lameenc.
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")
            
            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")
            
            # Get WAV data
            wav_data = audio_data.get_wav_data()
            
            # Create temporary WAV file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
                temp_wav.write(wav_data)
                temp_wav_path = temp_wav.name
            
            # Read WAV file and convert to MP3
            with wave.open(temp_wav_path, 'rb') as wav_file:
                frames = wav_file.readframes(wav_file.getnframes())
                sample_rate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                
                # Encode to MP3
                encoder = lameenc.Encoder()
                encoder.set_bit_rate(128)
                encoder.set_in_sample_rate(sample_rate)
                encoder.set_channels(channels)
                encoder.set_quality(2)
                
                mp3_data = encoder.encode(frames)
                mp3_data += encoder.flush()
                
                # Save MP3 file
                with open(file_path, 'wb') as mp3_file:
                    mp3_file.write(mp3_data)
            
            # Clean up temporary file
            os.unlink(temp_wav_path)
            
            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"Error during audio recording: {e}")

audio_filepath = "patient_voice_test_for_patient.mp3"
# record_audio(file_path=audio_filepath)


import os

from groq import Groq

GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
stt_model="whisper-large-v3"

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    client=Groq(api_key=GROQ_API_KEY)
    
    audio_file=open(audio_filepath, "rb")
    transcription=client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file,
            language="en"
        )
    return transcription.text