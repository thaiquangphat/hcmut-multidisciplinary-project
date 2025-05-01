import os
import json
from datetime import datetime
import random

def generate_chatbot_response(command: str) -> str:
    responses = {
        "lights_on": [
            "Sure, I've turned on the lights for you.",
            "Lights are on now. Let there be light!",
            "Got it! The room should be brighter now.",
            "The lights are switched on. Anything else?",
            "Lights are up and running!"
        ],
        "lights_off": [
            "Okay, turning off the lights.",
            "Lights are now off. Saving energy!",
            "Done. It's dark now.",
            "I've switched the lights off.",
            "Lights out! Let me know if you need them back on."
        ],
        "fan_on": [
            "Fan is now on. Enjoy the breeze!",
            "Cool! The fan is spinning now.",
            "Fan started. Hope that helps.",
            "Turning the fan on as requested.",
            "The fan is on. Stay chill!"
        ],
        "fan_off": [
            "Fan is turned off.",
            "No more breeze – the fan is off.",
            "Okay, stopping the fan.",
            "The fan has been powered down.",
            "Fan's off now. Let me know if you change your mind."
        ],
        "none": [
            "Sorry, I didn't catch any valid command.",
            "Hmm, I couldn't recognize that. Could you try again?",
            "No actionable command detected.",
            "I'm not sure what to do with that input.",
            "Can you please repeat that command more clearly?"
        ]
    }

    return random.choice(responses.get(command, responses["none"]))

def log_command(transcribed_text, label, filepath, date_str, duration):
    """Logs command details (transcription, timestamp, audio duration) into a JSON file."""
    # Paths for both logs and frontend directories
    logs_json_path = os.path.join("logs", date_str, "commands.json")
    frontend_json_path = os.path.join("..", "..", "frontend", "public", "audio", "commands.json")

    # Create frontend directory if it doesn't exist
    os.makedirs(os.path.dirname(frontend_json_path), exist_ok=True)

    # Load existing log if present in logs directory
    if os.path.exists(logs_json_path):
        with open(logs_json_path, "r") as json_file:
            log_data = json.load(json_file)
    else:
        log_data = []

    # Load existing log frontend if present in logs directory
    if os.path.exists(frontend_json_path):
        with open(frontend_json_path, "r") as json_file:
            log_frontend_data = json.load(json_file)
    else:
        log_frontend_data = []

    # Create new entry
    log_entry = {
        "transcribed_text": transcribed_text,
        "time_recorded": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "audio_file": os.path.basename(filepath),  # Only store the filename
        "duration_seconds": duration,
        "label": label,
        "date": date_str,
        "chatbot_response": generate_chatbot_response(label)
    }
    log_data.append(log_entry)
    log_frontend_data.append(log_entry)

    # Save updated log to logs directory
    with open(logs_json_path, "w") as json_file:
        json.dump(log_data, json_file, indent=4)

    # Save updated log to frontend directory
    with open(frontend_json_path, "w") as json_file:
        json.dump(log_frontend_data, json_file, indent=4)