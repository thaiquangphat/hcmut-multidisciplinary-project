from flask import Flask, request, jsonify
from main import transcribing_audio
import torch
from voice.audio import toggle_recording
import logging
from flask_cors import CORS
import json
from adafruit import receive_from_feed

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

app = Flask(__name__)

# Enable CORS for the Flask app
CORS(app)

# device = 'cuda' if torch.cuda.is_available() else 'cpu'
device = 'cpu'

@app.route('/api/toggle_recording', methods=['POST'])
def api_toggle_recording():
    try:
        logging.info("Toggle recording request received")
        response = toggle_recording()
        logging.info(f"Toggle recording response: {json.dumps(response, indent=2, ensure_ascii=False)}")
        return jsonify(response), 200
    except Exception as e:
        logging.error(f"Error toggling recording: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/transcribe', methods=['POST'])
def api_transcribe():
    try:
        logging.info("Transcription request received")
        data = request.json
        logging.info(f"Transcription request data: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        audio_file = data.get('audio_file')
        date_str = data.get('date_str')
        duration = data.get('duration')

        if not all([audio_file, date_str, duration]):
            error_msg = f"Missing required parameters. Received: audio_file={audio_file}, date_str={date_str}, duration={duration}"
            logging.error(error_msg)
            return jsonify({'error': error_msg}), 400

        logging.info("Starting transcription process...")
        text, prediction = transcribing_audio(audio_file, date_str, duration, device)
        logging.info(f"Transcription completed. Text: {text}, Prediction: {prediction}")
        
        return jsonify({
            'text': text,
            'prediction': prediction
        })
    except Exception as e:
        logging.error(f"Error in transcription: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/receive_humidity', methods=['GET'])
def api_receive_humidity():
    try:
        logging.info("Retrieving humidity data")
        data = receive_from_feed('humidity')
        logging.info(f"Humidity data retrieved: {data}")

        return jsonify({"ok": True, "value": float(data)}), 200 
    except Exception as e:
        logging.error(f"Error retrieving humidity data: {e}")
        return jsonify({"ok": False, 'error': str(e)}), 500
    
@app.route('/api/receive_motion', methods=['GET'])
def api_receive_motion():
    try:
        logging.info("Retrieving motion data")
        data = receive_from_feed('motion')
        logging.info(f"Motion data retrieved: {data}")

        return jsonify({"ok": True, "value": float(data)}), 200
    except Exception as e:
        logging.error(f"Error retrieving motion data: {e}")
        return jsonify({"ok": False, 'error': str(e)}), 500
    
@app.route('/api/receive_temperature', methods=['GET'])
def api_receive_temperature():
    try:
        logging.info("Retrieving temperature data")
        data = receive_from_feed('temperature')
        logging.info(f"Temperature data retrieved: {data}")

        return jsonify({"ok": True, "value": float(data)}), 200
    except Exception as e:
        logging.error(f"Error retrieving temperature data: {e}")
        return jsonify({"ok": False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)