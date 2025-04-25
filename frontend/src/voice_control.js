import React, { useState } from 'react';
import Sidebar from './sidebar'; // Import the Sidebar component

// Import the CSS file
import './voice_control.css';

const VoiceControlPage = () => {
  const [isRecording, setIsRecording] = useState(false);

  const handleToggleRecording = () => {
    setIsRecording(!isRecording);
    // TODO: Implement actual recording logic here
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
              onClick={handleToggleRecording}
            >
              <span className="material-icons">
                {isRecording ? 'mic' : 'mic_none'}
              </span>
            </button>
            <div className="recording-status">
              {isRecording ? 'Recording...' : 'Click to start recording'}
            </div>
          </div>

          {/* Conversation Section */}
          <div className="conversation-container">
            {/* User Command */}
            <div className="conversation-card">
              <div className="card-icon">
                <span className="material-icons">record_voice_over</span>
              </div>
              <p className="card-text">Turn the fan on!</p>
              <span className="card-status">record_voice...</span>
            </div>

            {/* System Response */}
            <div className="conversation-card">
              <div className="card-icon">
                <span className="material-icons">chat</span>
              </div>
              <p className="card-text">OK! Fan is on.</p>
              <span className="card-status">toys</span>
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