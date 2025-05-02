import React, { useState, useEffect } from 'react';
import apiClient from './api';

const FaceIDSettings = () => {
  const [isFaceIDEnabled, setIsFaceIDEnabled] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch FaceID status
  useEffect(() => {

    const fetchFaceIDStatus = async () => {
      try {
        const response = await apiClient.get('/faceid/status');
        setIsFaceIDEnabled(response.data.enabled);
      } catch (error) {
        if (error.response?.status === 403) {
          setError("Session expired. Please log in again.");
        } else {
          setError("Failed to fetch FaceID status.");
        }
      }
    };

    fetchFaceIDStatus();
  }, []);

  // Enable FaceID (start camera for login)
  const handleEnableFaceID = async () => {
    setIsLoading(true);
    setError(null);
    try {
      await apiClient.post('/auth/faceid/login');
      setIsFaceIDEnabled(true);
    } catch (err) {
      setError('Failed to enable FaceID');
    } finally {
      setIsLoading(false);
    }
  };

  // Disable FaceID
  const handleDisableFaceID = async () => {
    setIsLoading(true);
    setError(null);
    try {
      await apiClient.post('/auth/faceid/disable');
      setIsFaceIDEnabled(false);
    } catch (err) {
      setError('Failed to disable FaceID');
    } finally {
      setIsLoading(false);
    }
  };

  // Enroll FaceID (start camera for signup)
  const handleEnrollFaceID = async () => {
    setIsLoading(true);
    setError(null);
    try {
      await apiClient.post('/auth/faceid/signup');
      setIsFaceIDEnabled(true);
    } catch (err) {
      setError('Failed to enroll FaceID');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="setting-section">
      <h2>FaceID Settings</h2>
      {error && <p className="error-message">{error}</p>}

      <div className="faceid-toggle">
        <label>
          <input
            type="checkbox"
            checked={isFaceIDEnabled}
            onChange={() => {
              if (isFaceIDEnabled) {
                handleDisableFaceID();
              } else {
                handleEnableFaceID();
              }
            }}
            disabled={isLoading}
          />
          {isFaceIDEnabled ? 'Enabled' : 'Disabled'}
        </label>
      </div>

      {!isFaceIDEnabled && (
        <button 
          className="enroll-button" 
          onClick={handleEnrollFaceID} 
          disabled={isLoading}
        >
          Enroll FaceID
        </button>
      )}

      {isFaceIDEnabled && (
        <p className="status-message">FaceID is currently enabled for authentication.</p>
      )}
    </section>
  );
};

export default FaceIDSettings;