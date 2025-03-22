import os
import json
from datetime import datetime

def log_command(transcribed_text, filepath, date_str, duration):
    """Logs command details (transcription, timestamp, audio duration) into a JSON file."""
    json_filepath = os.path.join("logs", date_str, "commands.json")

    # Load existing log if present
    if os.path.exists(json_filepath):
        with open(json_filepath, "r") as json_file:
            log_data = json.load(json_file)
    else:
        log_data = []

    # Append new entry
    log_entry = {
        "transcribed_text": transcribed_text,
        "time_recorded": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "audio_file": filepath,
        "duration_seconds": duration
    }
    log_data.append(log_entry)

    # Save updated log
    with open(json_filepath, "w") as json_file:
        json.dump(log_data, json_file, indent=4)