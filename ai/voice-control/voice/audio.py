import pyaudio
import wave
import threading
import os
import shutil
from datetime import datetime
import json
import logging
import torch
from voice import transcribe
from text.inference import load_model, predict_with_loaded_model, TextClassifier
from voice import log_audio
from voice.adafruit_handler import detect_and_push

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Log current directory
logging.info(f"Current working directory: {os.getcwd()}")
logging.info(f"Script directory: {os.path.dirname(os.path.abspath(__file__))}")

# Global variables for recording state
is_recording = False
recording_thread = None
recording_flag = threading.Event()
last_recording_info = None

# Set up device for transcription
device = 'cpu'  # Using CPU as default

def get_latest_wav_file(logs_dir):
    """Get the latest .wav file from the logs directory."""
    wav_files = [f for f in os.listdir(logs_dir) if f.endswith('.wav')]
    if not wav_files:
        return None
    latest_file = max(wav_files, key=lambda x: os.path.getctime(os.path.join(logs_dir, x)))
    return os.path.join(logs_dir, latest_file)

def process_audio(audio_file, date_str, duration):
    """Process the audio file through transcription and prediction."""
    try:
        logging.info("Starting transcription...")
        text = transcribe.transcribe_audio(audio_file, device)
        logging.info(f"Transcription completed: {text}")

        logging.info("Loading model...")
        model, vectorizer = load_model(
            TextClassifier,
            'text/model/TextClassifier_model.pth',
            'text/model/TextClassifier_vectorizer.pkl',
            device
        )
        logging.info("Model loaded successfully.")

        logging.info("Predicting...")
        prediction = predict_with_loaded_model(text, model, vectorizer, device)
        logging.info(f"Prediction completed: {prediction}")

        # Logging
        logging.info("Logging command...")
        log_audio.log_command(text, prediction, audio_file, date_str, duration)
        logging.info("Command logged successfully.")

        # Pushing to adafruit
        logging.info("Pushing command to Adafruit...")
        successful = detect_and_push(prediction)
        logging.info(f"Command pushed successfully: {successful}")

        return text, prediction
    except Exception as e:
        logging.error(f"Error in processing audio: {e}")
        raise

def toggle_recording():
    """Toggle the recording state and start/stop recording accordingly."""
    global is_recording, recording_thread, last_recording_info
    
    if not is_recording:
        logging.info("Starting recording...")
        is_recording = True
        recording_flag.set()
        recording_thread = threading.Thread(target=record_audio)
        recording_thread.start()
        return {'is_recording': True, 'message': 'Recording started'}
    else:
        logging.info("Stopping recording...")
        is_recording = False
        recording_flag.clear()
        if recording_thread:
            recording_thread.join()
        
        # Get the current date for the logs directory
        current_date = datetime.now().strftime("%Y-%m-%d")
        logs_dir = os.path.join("logs", current_date)
        
        # Get the latest .wav file
        latest_wav = get_latest_wav_file(logs_dir)
        if latest_wav:
            filename = os.path.basename(latest_wav)
            date_str = current_date
            duration = get_wav_duration(latest_wav)
            
            # Log the paths being used
            logging.info(f"Using latest WAV file: {latest_wav}")
            logging.info(f"File duration: {duration} seconds")
            
            try:
                # Process the audio file
                text, prediction = process_audio(latest_wav, date_str, duration)
                
                dct = {
                    'is_recording': False,
                    'message': 'Recording stopped',
                    'audio_file': latest_wav,
                    'date_str': date_str,
                    'duration': duration,
                    'text': text,
                    'prediction': prediction
                }

                logging.info(f"Returning recording info: {json.dumps(dct, indent=2, ensure_ascii=False)}")
                return dct
            except Exception as e:
                logging.error(f"Error processing audio: {e}")
                return {
                    'is_recording': False,
                    'message': 'Recording stopped',
                    'error': str(e)
                }
        else:
            return {
                'is_recording': False,
                'message': 'Recording stopped',
                'error': 'No recording data available'
            }

def get_wav_duration(filepath):
    """Get the duration of a WAV file in seconds."""
    with wave.open(filepath, "r") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / float(rate)
    return round(duration, 2)

def record_audio(rate=44100, channels=1, chunk=1024):
    """Record audio until the recording flag is cleared."""
    p = pyaudio.PyAudio()
    
    try:
        stream = p.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

        frames = []
        logging.info("Recording started...")

        while recording_flag.is_set():
            data = stream.read(chunk)
            frames.append(data)

        logging.info("Recording stopped, processing audio...")

        stream.stop_stream()
        stream.close()

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

        logging.info(f"Audio saved as {logs_filepath} and {frontend_filepath} (Duration: {duration} sec)")
        
        # Store the recording info
        global last_recording_info
        last_recording_info = (logs_filepath, date_str, duration)
        
        return logs_filepath, date_str, duration

    except Exception as e:
        logging.error(f"Error during recording: {e}")
        raise
    finally:
        p.terminate()