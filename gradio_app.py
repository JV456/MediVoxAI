import os

import gradio as gr
from dotenv import load_dotenv

from doctor_brain import analyze_image_with_query, encode_image
from doctor_voice import (text_to_speech_with_elevenlabs,
                          text_to_speech_with_gtts)
from patient_voice import record_audio, transcribe_with_groq

load_dotenv()

system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose.
             What's in this image?. Do you find anything wrong with it medically?
             If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in
             your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
             Do not say 'In the image I see' but say 'With what I see, I think you have ....'
             Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot,
             Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

def process_inputs(audio_filepath, image_filepath):
    if not audio_filepath:
        return "Please record your voice first.", "Please provide both voice input and medical image for analysis.", None
    
    if not image_filepath:
        return "Please upload a medical image.", "Please provide both voice input and medical image for analysis.", None
    
    try:
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )
        
        doctor_response = analyze_image_with_query(
            query=system_prompt + speech_to_text_output, 
            encoded_image=encode_image(image_filepath), 
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
        
        audio_output_path = os.path.abspath("final.mp3")
        text_to_speech_with_gtts(input_text=doctor_response, output_filepath=audio_output_path)
        
        return speech_to_text_output, doctor_response, audio_output_path
        
    except Exception as e:
        error_msg = f"An error occurred during processing: {str(e)}"
        return error_msg, error_msg, None

def clear_inputs():
    return None, None, "", "", None

# Red and white theme with animations
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --primary-red: #dc2626;
    --light-red: #fee2e2;
    --dark-red: #991b1b;
    --white: #ffffff;
    --light-gray: #f8fafc;
    --gray: #64748b;
    --dark-gray: #334155;
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

/* Animated red and white gradient background */
.gradio-container {
    background: linear-gradient(-45deg, #dc2626, #fee2e2, #ffffff, #fecaca) !important;
    background-size: 400% 400% !important;
    animation: gradientShift 8s ease infinite !important;
    min-height: 100vh !important;
    font-family: 'Inter', sans-serif !important;
    position: relative !important;
    overflow: hidden !important;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Floating medical cross animation */
.gradio-container::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(circle at 20% 30%, rgba(220, 38, 38, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 40% 80%, rgba(220, 38, 38, 0.05) 0%, transparent 50%);
    animation: floatCross 15s ease-in-out infinite !important;
    pointer-events: none !important;
    z-index: 0 !important;
}

@keyframes floatCross {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(180deg); }
}

/* Main container with slide-in animation */
.gradio-container > div {
    animation: slideInUp 0.8s ease-out !important;
    position: relative !important;
    z-index: 1 !important;
}

@keyframes slideInUp {
    0% { transform: translateY(50px); opacity: 0; }
    100% { transform: translateY(0); opacity: 1; }
}

/* Title styling with red gradient */
h1 {
    color: var(--primary-red) !important;
    font-weight: 700 !important;
    font-size: 2.5rem !important;
    text-align: center !important;
    margin-bottom: 2rem !important;
    text-shadow: 0 2px 4px rgba(220, 38, 38, 0.1) !important;
    background: linear-gradient(135deg, var(--primary-red), var(--dark-red)) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    animation: titlePulse 3s ease-in-out infinite !important;
}

@keyframes titlePulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.02); }
}

/* Audio component with red accents */
.gr-audio {
    border: 2px solid var(--light-red) !important;
    border-radius: 8px !important;
    background: var(--white) !important;
    transition: all 0.3s ease !important;
    box-shadow: var(--shadow) !important;
}

.gr-audio:hover {
    border-color: var(--primary-red) !important;
    box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1) !important;
    transform: translateY(-2px) !important;
}

/* Record button animation */
.gr-audio button {
    background: var(--primary-red) !important;
    color: var(--white) !important;
    border: none !important;
    border-radius: 50% !important;
    width: 60px !important;
    height: 60px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3) !important;
    animation: recordPulse 2s ease-in-out infinite !important;
}

@keyframes recordPulse {
    0%, 100% { box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3); }
    50% { box-shadow: 0 6px 20px rgba(220, 38, 38, 0.5); }
}

.gr-audio button:hover {
    background: var(--dark-red) !important;
    transform: scale(1.1) !important;
}

/* Image upload area */
.gr-image {
    border: 2px dashed var(--light-red) !important;
    border-radius: 8px !important;
    background: var(--white) !important;
    transition: all 0.3s ease !important;
    position: relative !important;
    overflow: hidden !important;
}

.gr-image::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(220, 38, 38, 0.1), transparent);
    animation: shimmer 3s infinite !important;
}

@keyframes shimmer {
    0% { left: -100%; }
    100% { left: 100%; }
}

.gr-image:hover {
    border-color: var(--primary-red) !important;
    background: var(--light-red) !important;
    transform: scale(1.02) !important;
}

/* Textboxes with red theme */
.gr-textbox {
    border: 2px solid var(--light-red) !important;
    border-radius: 8px !important;
    background: var(--white) !important;
    transition: all 0.3s ease !important;
    box-shadow: var(--shadow) !important;
}

.gr-textbox:focus {
    border-color: var(--primary-red) !important;
    box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1) !important;
    transform: translateY(-1px) !important;
}

/* Submit button with red gradient */
.gr-button.gr-button-primary {
    background: linear-gradient(135deg, var(--primary-red), var(--dark-red)) !important;
    color: var(--white) !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3) !important;
    position: relative !important;
    overflow: hidden !important;
}

.gr-button.gr-button-primary::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.5s ease;
}

.gr-button.gr-button-primary:hover::before {
    left: 100%;
}

.gr-button.gr-button-primary:hover {
    background: linear-gradient(135deg, var(--dark-red), var(--primary-red)) !important;
    transform: translateY(-2px) scale(1.05) !important;
    box-shadow: 0 8px 20px rgba(220, 38, 38, 0.4) !important;
}

/* Clear button with white theme */
.gr-button.gr-button-secondary {
    background: var(--white) !important;
    color: var(--primary-red) !important;
    border: 2px solid var(--primary-red) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    transition: all 0.3s ease !important;
    box-shadow: var(--shadow) !important;
}

.gr-button.gr-button-secondary:hover {
    background: var(--primary-red) !important;
    color: var(--white) !important;
    transform: translateY(-2px) scale(1.05) !important;
    box-shadow: 0 8px 20px rgba(220, 38, 38, 0.3) !important;
}

/* Labels with red accents */
label {
    color: var(--primary-red) !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    margin-bottom: 0.5rem !important;
}

/* Container animations */
.gr-group {
    animation: fadeInScale 0.6s ease-out !important;
    transition: all 0.3s ease !important;
}

@keyframes fadeInScale {
    0% { transform: scale(0.95); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
}

.gr-group:hover {
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-lg) !important;
}

/* Row animations with stagger */
.gr-row:nth-child(1) { animation-delay: 0.1s !important; }
.gr-row:nth-child(2) { animation-delay: 0.2s !important; }
.gr-row:nth-child(3) { animation-delay: 0.3s !important; }
.gr-row:nth-child(4) { animation-delay: 0.4s !important; }

/* Loading state animation */
.loading {
    position: relative;
    overflow: hidden;
}

.loading::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(220, 38, 38, 0.1), transparent);
    animation: loading 1.5s infinite;
}

@keyframes loading {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

/* Responsive design */
@media (max-width: 768px) {
    h1 {
        font-size: 2rem !important;
    }
    
    .gr-button {
        width: 100% !important;
        margin-bottom: 1rem !important;
    }
}

/* Smooth scrolling */
html {
    scroll-behavior: smooth;
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: var(--light-red);
}

::-webkit-scrollbar-thumb {
    background: var(--primary-red);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--dark-red);
}

/* Focus states for accessibility */
*:focus {
    outline: 3px solid rgba(220, 38, 38, 0.3) !important;
    outline-offset: 2px !important;
}

/* Subtle entrance animation for all elements */
* {
    animation: subtleEntrance 0.8s ease-out !important;
}

@keyframes subtleEntrance {
    0% { opacity: 0; transform: translateY(10px); }
    100% { opacity: 1; transform: translateY(0); }
}
"""

# Create the interface with the same layout but red-white theme
with gr.Blocks(css=custom_css, title="AI Doctor with Vision and Voice") as iface:
    
    with gr.Row():
        with gr.Column(scale=1):
            audio_input = gr.Audio(
                sources=["microphone"], 
                type="filepath",
                label="audio_filepath"
            )
            
            image_input = gr.Image(
                type="filepath",
                label="image_filepath"
            )
            
            with gr.Row():
                clear_btn = gr.Button("Clear", variant="secondary")
                submit_btn = gr.Button("Submit", variant="primary")
        
        with gr.Column(scale=1):
            speech_output = gr.Textbox(
                label="Speech to Text",
                lines=3
            )
            
            doctor_output = gr.Textbox(
                label="Doctor's Response",
                lines=5
            )
            
            audio_output = gr.Audio(
                label="output_2",
                type="filepath"
            )
            
            flag_btn = gr.Button("Flag")
    
    # Event handlers
    submit_btn.click(
        fn=process_inputs,
        inputs=[audio_input, image_input],
        outputs=[speech_output, doctor_output, audio_output]
    )
    
    clear_btn.click(
        fn=clear_inputs,
        outputs=[audio_input, image_input, speech_output, doctor_output, audio_output]
    )

# Launch the interface
if __name__ == "__main__":
    iface.launch(
        debug=True,
        share=False,
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True
    )