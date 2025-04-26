import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState({
    user_id: 'mock_user_id',
    username: 'Test User'
  });
  const [loading, setLoading] = useState(false);

  // Bypass actual login
  const login = async (email, password) => {
    return {
      user: {
        user_id: 'mock_user_id',
        username: 'Test User'
      },
      access_token: 'mock_token',
      refresh_token: 'mock_refresh_token'
    };
  };

  const logout = async () => {
    setUser(null);
  };

  const value = {
    user,
    login,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 