from voice import audio
from voice import transcribe
import torch
import torch.nn as nn
import pickle
from voice import log_audio
from text.inference import load_model, predict_with_loaded_model, TextClassifier
from adafruit import pushing_command

def detect_and_push(prediction):
    if prediction == 'none':
        return 'none'
    
    adadevice, command = prediction.split('_')
    value = command.upper()

    return pushing_command(adadevice, value)

def recording():
    print("\033[95mInside recording function. Starting audio recording...\033[0m")
    audio_file, date_str, duration = audio.record_audio()
    print("\033[95mInside recording function. Audio recording finished...\033[0m")
    return audio_file, date_str, duration

def transcribing_audio(audio_file, date_str, duration, device):
    try:
        print("Starting transcription...")
        text = transcribe.transcribe_audio(audio_file, device)
        print(f"Transcription completed: {text}")

        print("Loading model...")
        model, vectorizer = load_model(
            TextClassifier,
            'text/model/TextClassifier_model.pth',
            'text/model/TextClassifier_vectorizer.pkl',
            device
        )
        print("Model loaded successfully.")

        print("Predicting...")
        prediction = predict_with_loaded_model(text, model, vectorizer, device)
        print(f"Prediction completed: {prediction}")

        # Logging
        print("Logging command...")
        log_audio.log_command(text, prediction, audio_file, date_str, duration)
        print("Command logged successfully.")

        # Pushing to adafruit
        print("Pushing command to Adafruit...")
        successful = detect_and_push(prediction)
        print(f"Command pushed successfully: {successful}")

        return text, prediction
    except Exception as e:
        print(f"Error in transcribing_audio: {e}")
        raise

def main(device):
    # Get the speech
    audio_file, date_str, duration = audio.record_audio()
    text = transcribe.transcribe_audio(audio_file, device)

    # Load the model
    model, vectorizer = load_model(
        TextClassifier,
        'text/model/TextClassifier_model.pth',
        'text/model/TextClassifier_vectorizer.pkl',
        device
    )
    
    # Inference
    prediction = predict_with_loaded_model(text, model, vectorizer, device)

    # Logging
    log_audio.log_command(text, prediction, audio_file, date_str, duration)

    # Pushing to adafruit
    successful = detect_and_push(prediction)

    return successful

if __name__ == "__main__":
    # Set up device, if GPU out of memory, manually set device='cpu'
    # device = 'cuda' if torch.cuda.is_available() else 'cpu'
    device = 'cpu'

    result = main(device)
    if isinstance(result, Exception):
        print(f'Some errors detected: {result}.')