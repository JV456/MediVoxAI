import os

import elevenlabs
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from gtts import gTTS

load_dotenv()

### Text-to-speech with gTTS

# def text_to_speech_with_gtts_old(input_text, output_filepath):
#     language = 'en-in'
    
#     audioobj = gTTS(
#         text=input_text,
#         lang=language,
#         slow=False
#     )
#     audioobj.save(output_filepath)
    
# input_text = "Hello, this is a test of the text-to-speech functionality."
# text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")

### Text-to-Speech with ElevenLabs

import platform
import subprocess

import elevenlabs
from elevenlabs.client import ElevenLabs

# ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    
# print(f"Using API key: {ELEVENLABS_API_KEY[:10]}...")

# def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
#     client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
#     audio=client.generate(
#         text=input_text,
#         voice="Bjt2TTr1iJsjxGH0bpLU",
#         output_format="mp3_22050_32",
#         model="eleven_turbo_v2"
#     )
#     elevenlabs.save(audio, output_filepath)
    
# text_to_speech_with_elevenlabs_old(input_text=input_text, output_filepath="elevenlabs_testing.mp3")


### Model to text output to voice





# def text_to_speech_with_gtts(input_text, output_filepath):
#     language = 'en'
    
#     audioobj = gTTS(
#         text=input_text,
#         lang=language,
#         slow=False
#     )
#     audioobj.save(output_filepath)
#     os_name = platform.system()
#     try:
#         if os_name == "Darwin":
#             subprocess.run(['afplay', output_filepath])
#         elif os_name == "Windows":
#             if output_filepath.endswith('.mp3'):
#                 # Use Windows Media Player for MP3 files
#                 subprocess.run(['powershell', '-c', f'Add-Type -AssemblyName presentationCore; $mediaPlayer = New-Object system.windows.media.mediaplayer; $mediaPlayer.open([uri]::new((Resolve-Path "{output_filepath}"))); $mediaPlayer.Play(); Start-Sleep 10'])
#             else:
#                 # Use SoundPlayer for WAV files
#                 subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
#         elif os_name == "Linux":
#             subprocess.run(['aplay', output_filepath])
#         else:
#             raise OSError("Unsupported operating system")
#     except Exception as e:
#         print(f"An error occurred while trying to play the audio: {e}")


def text_to_speech_with_gtts(input_text, output_filepath):
    language = 'en'
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    return output_filepath
    
    
# input_text = "Hello, this is jai testing the text-to-speech functionality with gTTS."

# text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")



## Text-to-Speech with ElevenLabs


ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio=client.generate(
        text=input_text,
        voice="Bjt2TTr1iJsjxGH0bpLU",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)
    os_name = platform.system()
    try:
        if os_name == "Darwin":
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":
            if output_filepath.endswith('.mp3'):
                # Use Windows Media Player for MP3 files
                subprocess.run(['powershell', '-c', f'Add-Type -AssemblyName presentationCore; $mediaPlayer = New-Object system.windows.media.mediaplayer; $mediaPlayer.open([uri]::new((Resolve-Path "{output_filepath}"))); $mediaPlayer.Play(); Start-Sleep 10'])
            else:
                # Use SoundPlayer for WAV files
                subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":
            subprocess.run(['aplay', output_filepath])
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")
    
# text_to_speech_with_elevenlabs(input_text=input_text, output_filepath="elevenlabs_testing_autoplay.mp3")

