import torch
import pickle
import torch.nn as nn

# Neural Network Model
class TextClassifier(nn.Module):
    def __init__(self, input_size, hidden_size1, hidden_size2, num_classes, dropout_prob=0.3):
        super(TextClassifier, self).__init__()

        self.model = nn.Sequential(
            nn.Linear(input_size, hidden_size1),
            nn.BatchNorm1d(hidden_size1),
            nn.LeakyReLU(),
            nn.Dropout(dropout_prob),
            
            nn.Linear(hidden_size1, hidden_size2),
            nn.BatchNorm1d(hidden_size2),
            nn.LeakyReLU(),
            nn.Dropout(dropout_prob),
            
            nn.Linear(hidden_size2, num_classes)
        )

    def forward(self, x):
        return self.model(x)

def load_model(model_class, model_path="model/TextClassifier_model.pth", vectorizer_path="model/TextClassifier_vectorizer.pkl", device='cpu'):
    saved_data = torch.load(model_path, map_location=device)

    input_size = saved_data['input_size']
    hidden_size1 = saved_data['hidden_size1']
    hidden_size2 = saved_data['hidden_size2']
    num_classes = saved_data['num_classes']
    dropout_prob = saved_data.get('dropout_prob', 0.3)  # Fallback if not saved

    loaded_model = model_class(input_size, hidden_size1, hidden_size2, num_classes, dropout_prob).to(device)
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
    
    reverse_map = {0: "lights_on", 1: "lights_off", 2: "fan_on", 3: "fan_off", 4: "none"}
    return reverse_map[predicted.item()]

