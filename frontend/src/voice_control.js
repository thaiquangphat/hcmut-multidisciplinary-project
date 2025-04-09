import React from 'react';
import Sidebar from './sidebar'; // Import the Sidebar component

// Import the CSS file
import './voice_control.css';

const VoiceControlPage = () => {
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
          <div className="header-status">
            <span className="status-text">rss_feed</span>
            <div className="status-icon">📶</div>
          </div>
        </header>

        <div className="content-container">
          {/* Microphone and Pause Buttons */}
          <div className="button-group">
            <div className="mic-button">
              <span className="mic-icon">🎤</span>
            </div>
            <div className="pause-button">
              <span className="pause-icon">⏸️</span>
            </div>
          </div>

          {/* Microphone Status */}
          <div className="status-group">
            <span className="status-text">mic_none</span>
            <span className="status-text">pause_circle...</span>
          </div>

          {/* Conversation Section */}
          <div className="conversation-container">
            {/* User Command */}
            <div className="conversation-card">
              <div className="card-icon">🗣️</div>
              <p className="card-text">Turn the fan on!</p>
              <span className="card-status">record_voice...</span>
            </div>

            {/* System Response */}
            <div className="conversation-card">
              <div className="card-icon">💬</div>
              <p className="card-text">OK! Fan is on.</p>
              <span className="card-status">toys</span>
              <div className="card-icon fan-icon">🌀</div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default VoiceControlPage;