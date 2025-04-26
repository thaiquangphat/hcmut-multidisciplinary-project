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
  const [globalState, setGlobalState] = useState(0);

  const toggleGlobalState = () => {
    setGlobalState((prevState) => (prevState === 0 ? 1 : 0));
    console.log(`Global state changed to: ${globalState}`);
  };

  const handleRecording = async () => {
    try {
      console.log('Toggling recording state...');
      await axios.post('http://127.0.0.1:5000/api/toggle_recording');
      setIsRecording(isRecording); // Toggle the recording state

      if (!isRecording) {
        // If stopping recording, handle transcription
        setText('Transcribing...');
        setPrediction('');

        const response = await axios.post('http://127.0.0.1:5000/api/recording');
        const { audio_file, date_str, duration } = response.data;

        const transcribeResponse = await axios.post('http://127.0.0.1:5000/api/transcribing', {
          audio_file,
          date_str,
          duration
        });

        setText(transcribeResponse.data.text);
        setPrediction(transcribeResponse.data.prediction);
      }
    } catch (error) {
      console.error('Error toggling recording or processing:', error);
      setText('');
      setPrediction('');
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
              className={`record-button ${globalState === 1 ? 'recording' : ''}`}
              onClick={() => {
                toggleGlobalState();
                handleRecording();
              }}
            >
              <span className="material-icons">
                {globalState === 1 ? 'mic' : 'mic_none'}
              </span>
            </button>
            <div className="recording-status">
              {globalState === 1 ? 'Recording...' : 'Click to start recording'}
            </div>
          </div>
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