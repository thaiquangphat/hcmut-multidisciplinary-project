from voice import audio
from voice import transcribe
import torch
import torch.nn as nn
import pickle
from voice import log_audio

# Neural Network Model
class TextClassifier(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(TextClassifier, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        x = self.layer1(x)
        x = self.relu(x)
        x = self.layer2(x)
        return x
    
# Function to load model
def load_model(model_class, model_path="model/text_classifier_model.pth", vectorizer_path="model/text_classifier_model_vectorizer.pkl"):
    # Load the saved dictionary
    saved_data = torch.load(model_path, weights_only=True)
    
    # Extract architecture parameters
    input_size = saved_data['input_size']
    hidden_size = saved_data['hidden_size']
    num_classes = saved_data['num_classes']
    
    # Initialize the model with the saved parameters
    loaded_model = model_class(input_size, hidden_size, num_classes)
    
    # Load the state dictionary
    loaded_model.load_state_dict(saved_data['state_dict'])
    loaded_model.eval()  # Set to evaluation mode
    
    # Load the vectorizer
    with open(vectorizer_path, 'rb') as f:
        loaded_vectorizer = pickle.load(f)
    
    return loaded_model, loaded_vectorizer

# Inference with the loaded model
def predict_with_loaded_model(text, model, vectorizer):
    model.eval()
    text_vector = vectorizer.transform([text]).toarray()
    text_tensor = torch.FloatTensor(text_vector)
    
    with torch.no_grad():
        output = model(text_tensor)
        _, predicted = torch.max(output, 1)
    
    reverse_map = {0: "lights_on", 1: "lights_off", 2: "fan_on", 3: "fan_off"}
    return reverse_map[predicted.item()]

if __name__ == "__main__":
    # Get the speech
    audio_file, date_str, duration = audio.record_audio()
    text = transcribe.transcribe_audio(audio_file)

    print(f'You said: {text}')

    # Load the model
    model, vectorizer = load_model(
        TextClassifier,
        'text/model/TextClassifier.pth',
        'text/model/TextClassifier_vectorizer.pkl'
    )
    
    prediction = predict_with_loaded_model(text, model, vectorizer)
    print(f'You want to: {prediction}')

    # Logging
    log_audio.log_command(text, prediction, audio_file, date_str, duration)

