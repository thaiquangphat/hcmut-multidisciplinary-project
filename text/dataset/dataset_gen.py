import itertools
import json

adjectives = {
    "fast": 4, "bright": 5, "cold": 2, "warm": 3, "powerful": 6, 
    "heavy": 4, "strong": 5, "intense": 6, "vibrant": 5, "sturdy": 4, 
    "steady": 4, "flashing": 6, "refreshing": 5, "blinding": 6, "brightened": 5, 
    "eco-friendly": 3, "electric": 5, "brilliant": 5, "dynamic": 5, "luminous": 6, 
    "sparkling": 6
}
verbs = {
    "turn": 3, "make": 4, "activate": 5, "stop": 2, "increase": 6, 
    "decrease": 3, "start": 4, "control": 7, "adjust": 5, "boost": 6, 
    "power": 7, "optimize": 6, "trigger": 6, "enhance": 6, 
    "improve": 5, "intensify": 6, "brighten": 5, "elevate": 6, "supercharge": 7, 
    "recharge": 5, "start-up": 6, "reboot": 5, "adjust intensity": 6, 
    "speed up": 6, "increase speed": 7, "boost power": 7, "light up": 5, 
    "flicker": 3, "disable": 2, "activate power": 6,
}



nouns = ["fan", "light", "fans", "lights"]

action_labels = {
    0: "lights_on", 
    1: "lights_off",
    2: "fan_on",
    3: "fan_off" 
}

adjective_noun_verb = list(itertools.product(adjectives.keys(), nouns, verbs.keys()))

def calculate_weight(adjective, verb):
    adj_weight = adjectives[adjective]
    verb_weight = verbs[verb]
    total_weight = adj_weight + verb_weight
    return total_weight

json_output = []
threshold = int(input("Enter the threshold for classification (1-10): "))
for perm in adjective_noun_verb:
    adjective, noun, verb = perm
    total_weight = calculate_weight(adjective, verb)
    
    if noun == "light" or noun == "lights":
        if total_weight > threshold:
            label = action_labels[0]
        else:
            label = action_labels[1]
    elif noun == "fan" or noun == "fans":
        if total_weight > threshold:
            label = action_labels[2]
        else:
            label = action_labels[3]
    
    json_output.append({
        "text": f"{adjective} {noun} {verb}",
        "label": label
    })

with open("synthetic_dataset.json", "w") as f:
    json.dump(json_output, f, indent=2)
    print("Synthetic dataset saved to synthetic_dataset.json")