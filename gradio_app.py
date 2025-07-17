import os
import time

import gradio as gr
from dotenv import load_dotenv

from doctor_brain import analyze_image_with_query, encode_image
from doctor_voice import text_to_speech_with_gtts
from patient_voice import transcribe_with_groq

load_dotenv()

system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

def process_inputs(audio_filepath, image_filepath):
    speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
                                                 audio_filepath=audio_filepath,
                                                 stt_model="whisper-large-v3")

    # Handle the image input
    if image_filepath:
        doctor_response = analyze_image_with_query(query=system_prompt+speech_to_text_output, encoded_image=encode_image(image_filepath), model="meta-llama/llama-4-scout-17b-16e-instruct")
    else:
        doctor_response = "No image provided for me to analyze"

    # Use absolute path for audio output
    audio_output_path = os.path.abspath("final.mp3")
    text_to_speech_with_gtts(input_text=doctor_response, output_filepath=audio_output_path)

    return speech_to_text_output, doctor_response, audio_output_path

# Use Gradio Blocks for better control
with gr.Blocks(title="MediVoxAI - AI Doctor with Vision and Voice") as demo:
    gr.Markdown("# MediVoxAI - AI Doctor with Vision and Voice")
    gr.Markdown("Upload an image and record your voice to get medical advice")
    
    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Record your voice")
            image_input = gr.Image(type="filepath", label="Upload medical image")
            submit_btn = gr.Button("Get Medical Advice", variant="primary")
        
        with gr.Column():
            speech_output = gr.Textbox(label="Speech to Text", lines=3)
            doctor_output = gr.Textbox(label="Doctor's Response", lines=5)
            audio_output = gr.Audio(label="Doctor's Voice Response", type="filepath")
    
    submit_btn.click(
        fn=process_inputs,
        inputs=[audio_input, image_input],
        outputs=[speech_output, doctor_output, audio_output]
    )

if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        debug=False
    )