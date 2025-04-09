import torch
import pickle
import torch.nn as nn

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

def load_model(model_class, model_path="text/model/TextClassifier.pth", vectorizer_path="text/model/TextClassifier_vectorizer.pkl", run_device='cpu'):
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    device = torch.device("cuda" if run_device=='cuda' and torch.cuda.is_available() else "cpu")

    saved_data = torch.load(model_path, map_location=device, weights_only=True)

    input_size = saved_data['input_size']
    hidden_size = saved_data['hidden_size']
    num_classes = saved_data['num_classes']

    loaded_model = model_class(input_size, hidden_size, num_classes).to(device)
    loaded_model.load_state_dict(saved_data['state_dict'])
    loaded_model.eval()

    with open(vectorizer_path, 'rb') as f:
        loaded_vectorizer = pickle.load(f)

    # print("✅ Model and vectorizer loaded successfully.")
    return loaded_model, loaded_vectorizer

def predict_with_loaded_model(text, model, vectorizer, device):
    model.eval()
    text_vector = vectorizer.transform([text]).toarray()
    text_tensor = torch.FloatTensor(text_vector).to(device)
    
    with torch.no_grad():
        output = model(text_tensor)
        _, predicted = torch.max(output, 1)
    
    reverse_map = {0: "lights_on", 1: "lights_off", 2: "fan_on", 3: "fan_off"}
    return reverse_map[predicted.item()]

