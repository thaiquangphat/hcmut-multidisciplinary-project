import pyaudio
import wave
import threading
import os
from datetime import datetime

def get_wav_duration(filepath):
    """Get the duration of a WAV file in seconds."""
    with wave.open(filepath, "r") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / float(rate)
    return round(duration, 2)

def record_audio(rate=44100, channels=1, chunk=1024):
    p = pyaudio.PyAudio()
    
    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)
    
    print("Recording... Press Enter to stop.")
    frames = []
    
    def stop_recording():
        input()
        nonlocal recording
        recording = False
    
    recording = True
    stop_thread = threading.Thread(target=stop_recording)
    stop_thread.start()
    
    while recording:
        data = stream.read(chunk)
        frames.append(data)
    
    print("Recording finished.")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M-%S")
    
    folder_path = os.path.join("logs", date_str)
    os.makedirs(folder_path, exist_ok=True)
    
    filename = f"{date_str}_{time_str}.wav"
    filepath = os.path.join(folder_path, filename)
    
    with wave.open(filepath, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
    
    # Get the duration
    duration = get_wav_duration(filepath)
    
    print(f"Audio saved as {filepath} (Duration: {duration} sec)")
    return filepath, date_str, duration