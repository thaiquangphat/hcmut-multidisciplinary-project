from voice import audio
from voice import transcribe
import torch
import torch.nn as nn
import pickle
from voice import log_audio
from text.inference import load_model, predict_with_loaded_model, TextClassifier
from adafruit import pushing_command

if __name__ == "__main__":
    # Set up device, if GPU out of memory, manually set device='cpu'
    # device = 'cuda' if torch.cuda.is_available() else 'cpu'
    device = 'cpu'

    # Get the speech
    audio_file, date_str, duration = audio.record_audio()
    text = transcribe.transcribe_audio(audio_file, device)

    print(f'You said: {text}')

    # Load the model
    model, vectorizer = load_model(
        TextClassifier,
        'text/model/TextClassifier_model.pth',
        'text/model/TextClassifier_vectorizer.pkl',
        device
    )
    
    prediction = predict_with_loaded_model(text, model, vectorizer, device)
    print(f'You want to: {prediction}')

    # Logging
    log_audio.log_command(text, prediction, audio_file, date_str, duration)

    # Pushing to adafruit
    adadevice = 'fan'
    value     = ''

    if adadevice == 'fan':
        dct = {
            'fan_on': 'ON',
            'fan_off': 'OFF'
        }
        value = dct[prediction] if prediction in dct.keys() else ''
    
    # pushing_command(adadevice, value)

