import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom'; // Import useNavigate for navigation
import logoImg from './yolohome.png';
import illustrationImg from './yolohome.png';
import chair from './chair.png'

const LoginPage = () => {
  const [username, setUsername] = useState(''); // State for username
  const [password, setPassword] = useState(''); // State for password (optional)
  const navigate = useNavigate(); // Hook for navigation

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username.trim()) { // Check if username is not empty
      navigate('/dashboard', { state: { username } }); // Navigate to dashboard with username
    } else {
      alert('Please enter a username'); // Basic validation
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        minHeight: '100vh',
        background: 'linear-gradient(to bottom, #fff, #f5f0e1)',
        fontFamily: 'Arial, sans-serif',
      }}
    >
      {/* Header */}
      <header
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          padding: '20px 40px',
        }}
      >
        {/* Logo */}
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <img
            src={logoImg}
            alt="Smart Home Logo"
            style={{ width: '50px', height: '50px', marginRight: '10px' }}
          />
          <span style={{ fontSize: '20px', fontWeight: 'bold', color: '#333' }}>
            SMART HOME
          </span>
        </div>

        {/* Navigation Links */}
        <nav>
          <Link
            to="/about"
            style={{
              marginRight: '20px',
              textDecoration: 'none',
              color: '#333',
              fontSize: '16px',
            }}
          >
            ABOUT US
          </Link>
          <Link
            to="/"
            style={{
              padding: '10px 20px',
              backgroundColor: '#8b5a2b',
              color: '#fff',
              border: 'none',
              borderRadius: '20px',
              cursor: 'pointer',
              fontSize: '16px',
              textDecoration: 'none',
              display: 'inline-block',
            }}
          >
            CANCEL
          </Link>
        </nav>
      </header>

      {/* Main Content */}
      <main
        style={{
          display: 'flex',
          flex: 1,
          padding: '40px',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        {/* Illustration Section */}
        <div style={{ flex: 1, paddingRight: '20px' }}>
          <img
            src={chair}
            alt="Illustration of chairs and table"
            style={{ maxWidth: '100%', height: 'auto' }}
          />
        </div>

        {/* Login Form Section */}
        <div style={{ flex: 1, maxWidth: '400px' }}>
          <h2
            style={{
              fontSize: '36px',
              color: '#333',
              marginBottom: '20px',
              textAlign: 'center',
            }}
          >
            LOGIN ACCOUNT
          </h2>
          <form
            onSubmit={handleSubmit} // Add form submission handler
            style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '15px',
            }}
          >
            <label
              style={{
                fontSize: '18px',
                color: '#333',
                marginBottom: '5px',
              }}
            >
              Username
            </label>
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)} // Update username state
              style={{
                padding: '15px',
                fontSize: '16px',
                border: 'none',
                borderRadius: '10px',
                backgroundColor: '#f5e5b3',
                color: '#999',
              }}
            />
            <label
              style={{
                fontSize: '18px',
                color: '#333',
                marginBottom: '5px',
              }}
            >
              Password
            </label>
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)} // Update password state
              style={{
                padding: '15px',
                fontSize: '16px',
                border: 'none',
                borderRadius: '10px',
                backgroundColor: '#f5e5b3',
                color: '#999',
              }}
            />
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginTop: '10px',
              }}
            >
              <label style={{ display: 'flex', alignItems: 'center', fontSize: '14px', color: '#333' }}>
                <input type="checkbox" style={{ marginRight: '5px' }} />
                Remember your account
              </label>
              <Link
                to="/forget-password"
                style={{
                  textDecoration: 'none',
                  color: '#333',
                  fontSize: '14px',
                }}
              >
                Forget your password?
              </Link>
            </div>
            <button
              type="submit"
              style={{
                padding: '15px',
                backgroundColor: '#8b5a2b',
                color: '#fff',
                border: 'none',
                borderRadius: '10px',
                cursor: 'pointer',
                fontSize: '16px',
                marginTop: '20px',
              }}
            >
              LOG IN
            </button>
          </form>
        </div>
      </main>
    </div>
  );
};

export default LoginPage;