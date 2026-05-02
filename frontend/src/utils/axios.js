import axios from 'axios';

// Set default base URL for API calls
axios.defaults.baseURL = 'http://localhost:8000';

// Set default timeout
axios.defaults.timeout = 120000; // 2 minutes for model inference

// Request interceptor - add Bearer token to protected requests
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - redirect to login only on 401 for protected routes (not login/register)
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const url = error.config?.url || '';
      // Don't redirect if 401 came from login/register (wrong password)
      if (!url.includes('/api/auth/login') && !url.includes('/api/auth/register')) {
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default axios;
