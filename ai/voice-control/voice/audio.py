import pyaudio
import wave
import threading
import os
import shutil
from datetime import datetime

# Add a global variable to track the recording state
global is_recording
is_recording = False

def toggle_recording():
    """Toggle the recording state and start/stop recording accordingly."""
    global is_recording
    if not is_recording:
        start_recording()
        is_recording = True
    else:
        stop_recording()
        is_recording = False

def get_wav_duration(filepath):
    """Get the duration of a WAV file in seconds."""
    with wave.open(filepath, "r") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / float(rate)
    return round(duration, 2)

recording_flag = threading.Event()

def start_recording():
    """Set the recording flag to start recording."""
    recording_flag.set()

def stop_recording():
    """Clear the recording flag to stop recording."""
    recording_flag.clear()

def record_audio(rate=44100, channels=1, chunk=1024):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("Recording...")
    frames = []

    recording_flag.set()  # Ensure the flag is set to start recording

    while recording_flag.is_set():
        data = stream.read(chunk)
        frames.append(data)

    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M-%S")

    # Create logs directory
    logs_folder_path = os.path.join("logs", date_str)
    os.makedirs(logs_folder_path, exist_ok=True)

    # Create frontend audio directory
    frontend_audio_path = os.path.join("..", "..", "frontend", "public", "audio")
    os.makedirs(frontend_audio_path, exist_ok=True)

    filename = f"{date_str}_{time_str}.wav"

    # Save to logs directory
    logs_filepath = os.path.join(logs_folder_path, filename)
    with wave.open(logs_filepath, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    # Copy to frontend directory
    frontend_filepath = os.path.join(frontend_audio_path, filename)
    shutil.copy2(logs_filepath, frontend_filepath)

    # Get the duration
    duration = get_wav_duration(logs_filepath)

    print(f"Audio saved as {logs_filepath} and {frontend_filepath} (Duration: {duration} sec)")
    return logs_filepath, date_str, duration

def record_audio_with_control(rate=44100, channels=1, chunk=1024):
    """Record audio using the recording_flag for start/stop control."""
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("Recording...")
    frames = []

    while recording_flag.is_set():
        data = stream.read(chunk)
        frames.append(data)

    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M-%S")

    # Create logs directory
    logs_folder_path = os.path.join("logs", date_str)
    os.makedirs(logs_folder_path, exist_ok=True)

    # Create frontend audio directory
    frontend_audio_path = os.path.join("..", "..", "frontend", "public", "audio")
    os.makedirs(frontend_audio_path, exist_ok=True)

    filename = f"{date_str}_{time_str}.wav"

    # Save to logs directory
    logs_filepath = os.path.join(logs_folder_path, filename)
    with wave.open(logs_filepath, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    # Copy to frontend directory
    frontend_filepath = os.path.join(frontend_audio_path, filename)
    shutil.copy2(logs_filepath, frontend_filepath)

    # Get the duration
    duration = get_wav_duration(logs_filepath)

    print(f"Audio saved as {logs_filepath} and {frontend_filepath} (Duration: {duration} sec)")
    return logs_filepath, date_str, duration