from flask import Flask, request, jsonify
from main import recording, transcribing_audio
import torch
from voice.audio import start_recording, stop_recording
import logging
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

app = Flask(__name__)

# Enable CORS for the Flask app
CORS(app)

# device = 'cuda' if torch.cuda.is_available() else 'cpu'
device = 'cpu'

@app.route('/api/recording', methods=['POST'])
def api_recording():
    try:
        audio_file, date_str, duration = recording()
        return jsonify({
            'audio_file': audio_file,
            'date_str': date_str,
            'duration': duration
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transcribing', methods=['POST'])
def api_transcribing():
    try:
        data = request.json
        audio_file = data['audio_file']
        date_str = data['date_str']
        duration = data['duration']

        text, prediction = transcribing_audio(audio_file, date_str, duration, device)
        return jsonify({
            'text': text,
            'prediction': prediction
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/start_recording', methods=['POST'])
def api_start_recording():
    try:
        logging.info("Start recording request received.")
        start_recording()
        return jsonify({'message': 'Recording started'}), 200
    except Exception as e:
        logging.error(f"Error starting recording: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop_recording', methods=['POST'])
def api_stop_recording():
    try:
        logging.info("Stop recording request received.")
        stop_recording()
        return jsonify({'message': 'Recording stopped'}), 200
    except Exception as e:
        logging.error(f"Error stopping recording: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)