import React from 'react';
import Sidebar from './sidebar'; // Import the Sidebar component

// Import the CSS file
import './statistics.css';

const StatisticsPage = () => {
  // Sample data for the command history
  const commandHistory = [
    { time: '5:00 AM', command: 'Fan on', date: '28-02-2025' },
    { time: '6:00 AM', command: 'Fan off', date: '28-02-2025' },
    { time: '7:00 AM', command: 'Lights on', date: '28-02-2025' },
  ];

  // Sample data for the dates (not used in the UI yet, but keeping it for future use)
  const dates = [
    '28-02-2025',
    '29-02-2025',
    '30-02-2025',
    '31-02-2025',
    '01-04-2025',
    '02-04-2025',
    '03-04-2025',
  ];

  return (
    <div className="statistics-page">
      {/* Sidebar */}
      <Sidebar activePage="STATISTICS" />

      {/* Main Content */}
      <main className="statistics-main-content">
        <header className="statistics-header">
          <div>
            <h1 className="statistics-header-title">History of commands</h1>
            <p className="statistics-header-subtitle">Find what you have asked to do</p>
          </div>
          <div className="statistics-header-icon">📁</div>
        </header>

        <div className="statistics-content-container">
          {/* Command List */}
          <div className="statistics-command-list">
            {commandHistory.map((item, index) => (
              <div
                key={index}
                className={`statistics-command-item ${
                  index < commandHistory.length - 1 ? 'statistics-border-bottom' : ''
                }`}
              >
                <span className="statistics-command-time">{item.time}</span>
                <span className="statistics-command-text">{item.command}</span>
                <span className="statistics-command-info">ℹ️</span>
              </div>
            ))}
          </div>

          {/* Audio Player */}
          <div className="statistics-audio-player">
            <div className="statistics-audio-icon">equalizer</div>
            <div className="statistics-player-controls">
              <div className="statistics-play-button">
                <span className="statistics-play-icon">▶️</span>
              </div>
              <div className="statistics-progress-bar-container">
                <span className="statistics-progress-time">00:01</span>
                <div className="statistics-progress-bar">
                  <div className="statistics-progress-filled" />
                  <div className="statistics-progress-handle" />
                </div>
                <span className="statistics-progress-time">00:03</span>
              </div>
            </div>
            <p className="statistics-audio-text">Please turn the fan.</p>
            <span className="statistics-audio-status">pl...</span>
          </div>
        </div>
      </main>
    </div>
  );
};

export default StatisticsPage;