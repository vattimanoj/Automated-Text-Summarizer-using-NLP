import React, { createContext, useState, useEffect, useContext, useCallback } from 'react';
import axios from '../utils/axios';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('token'));

  const fetchUser = useCallback(async () => {
    try {
      const response = await axios.get('/api/auth/me');
      setUser(response.data);
    } catch (error) {
      console.error('Error fetching user:', error);
      logout();
    } finally {
      setLoading(false);
    }
  }, []); // logout is stable, axios is stable

  useEffect(() => {
    if (token) {
      // If we already have user (e.g. from login), skip fetch - avoids extra request & race
      if (user) {
        setLoading(false);
      } else {
        fetchUser();
      }
    } else {
      setLoading(false);
    }
  }, [token, user, fetchUser]);

  const login = async (email, password) => {
    // OAuth2 expects application/x-www-form-urlencoded (username/password)
    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);

    const response = await axios.post('/api/auth/login', params);
    const access_token = response.data.access_token || response.data.accessToken;
    const user = response.data.user;

    if (!access_token || !user) {
      throw new Error('Invalid login response');
    }

    localStorage.setItem('token', access_token);
    setToken(access_token);
    setUser(user);
    return { success: true };
  };

  const register = async (name, email, password) => {
    await axios.post('/api/auth/register', {
      name,
      email,
      password,
    });
    return { success: true };
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
  };

  const updateUser = (updatedUser) => {
    setUser(updatedUser);
  };

  const value = {
    user,
    token,
    login,
    register,
    logout,
    updateUser,
    loading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
