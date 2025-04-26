import os
import json
from datetime import datetime

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
        "date": date_str
    }
    log_data.append(log_entry)
    log_frontend_data.append(log_entry)

    # Save updated log to logs directory
    with open(logs_json_path, "w") as json_file:
        json.dump(log_data, json_file, indent=4)

    # Save updated log to frontend directory
    with open(frontend_json_path, "w") as json_file:
        json.dump(log_frontend_data, json_file, indent=4)