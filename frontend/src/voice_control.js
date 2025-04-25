import React, { useState } from 'react';
import axios from 'axios';
import Sidebar from './sidebar'; // Import the Sidebar component

// Import the CSS file
import './voice_control.css';

const VoiceControlPage = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [text, setText] = useState('');
  const [prediction, setPrediction] = useState('');
  const [recordingData, setRecordingData] = useState(null);

  const handleRecording = async () => {
    if (!isRecording) {
        // Start recording
        setIsRecording(true); // Immediately set the recording state
        try {
            console.log('Sending start recording request...');
            await axios.post('http://127.0.0.1:5000/api/start_recording');
            console.log('Start recording request sent successfully.');
        } catch (error) {
            console.error('Error starting recording:', error);
            setIsRecording(false); // Revert state if an error occurs
        }
    } else {
        // Stop recording
        setIsRecording(false); // Immediately toggle the recording state
        try {
            console.log('Sending stop recording request...');
            await axios.post('http://127.0.0.1:5000/api/stop_recording');
            console.log('Stop recording request sent successfully.');

            // Show transcribing status
            setText('Transcribing...');
            setPrediction('');

            // Wait for the backend to process the stop signal
            const response = await axios.post('http://127.0.0.1:5000/api/recording');
            const { audio_file, date_str, duration } = response.data;

            // Transcribe the audio
            const transcribeResponse = await axios.post('http://127.0.0.1:5000/api/transcribing', {
                audio_file,
                date_str,
                duration
            });

            setText(transcribeResponse.data.text);
            setPrediction(transcribeResponse.data.prediction);
        } catch (error) {
            console.error('Error stopping recording or transcribing:', error);
            setText(''); // Clear transcribing status on error
            setPrediction('');
        }
    }
  };

  return (
    <div className="voice-control-page">
      {/* Sidebar */}
      <Sidebar activePage="VOICE CONTROL" />

      {/* Main Content */}
      <main className="main-content">
        <header className="header">
          <div>
            <h1 className="header-title">Voice Control</h1>
            <p className="header-subtitle">Hi Thao, what do you want?</p>
          </div>
        </header>

        <div className="content-container">
          <div className="recording-container">
            <button
              className={`record-button ${isRecording ? 'recording' : ''}`}
              onClick={handleRecording}
            >
              <span className="material-icons">
                {isRecording ? 'mic' : 'mic_none'}
              </span>
            </button>
            <div className="recording-status">
              {isRecording ? 'Recording...' : 'Click to start recording'}
            </div>
          </div>

          {/* Transcription and Prediction Section */}
          {text && (
            <div className="transcription-container">
              <p>
                <strong>Transcribed Text:</strong> {text}
              </p>
              <p>
                <strong>Prediction:</strong> {prediction}
              </p>
            </div>
          )}

          {/* Conversation Section */}
          <div className="conversation-container">
            {/* User Command */}
            <div className="conversation-card">
              <div className="card-icon">
                <span className="material-icons">record_voice_over</span>
              </div>
              <p className="card-text">{text || ''}</p>
              <span className="card-status">{text ? 'record_voice...' : ''}</span>
            </div>

            {/* System Response */}
            <div className="conversation-card">
              <div className="card-icon">
                <span className="material-icons">chat</span>
              </div>
              <p className="card-text">{prediction || ''}</p>
              <span className="card-status">{prediction ? 'toys' : ''}</span>
              <div className="card-icon">
                <span className="material-icons">air</span>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default VoiceControlPage;