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
        return
    
    adadevice, command = prediction.split('_')
    value = command.upper()

    pushing_command(adadevice, value)

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