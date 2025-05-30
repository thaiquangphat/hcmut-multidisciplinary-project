from flask import Flask, request, jsonify
from main import transcribing_audio
import torch
from voice.audio import toggle_recording
from adafruit import get_value_from_feed
import logging
from flask_cors import CORS
import json

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
        logging.info("Humidity request received")
        receive_value = get_value_from_feed('humidity')
        logging.info(f"Humidity value received: {receive_value}")
        return jsonify({"ok": True, "value": receive_value}), 200
    except Exception as e:
        logging.error(f"Error receiving humidity data: {e}")
        return jsonify({"ok": False, 'error': str(e)}), 500
    
@app.route('/api/receive_temperature', methods=['GET'])
def api_receive_temperature():
    try:
        logging.info("Temperature request received")
        receive_value = get_value_from_feed('temperature')
        logging.info(f"Temperature value received: {receive_value}")
        return jsonify({"ok": True, "value": receive_value}), 200
    except Exception as e:
        logging.error(f"Error receiving temperature data: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/receive_light_frame', methods=['GET'])
def api_receive_light_frame():
    try:
        logging.info("Light frame request received")
        receive_value = get_value_from_feed('light')
        logging.info(f"Light frame value received: {receive_value}")
        return jsonify({"ok": True, "value": receive_value}), 200
    except Exception as e:
        logging.error(f"Error receiving light frame data: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)