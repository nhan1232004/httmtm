// API client configuration for CEO Dashboard
// Uses Analytics & ML endpoints for strategic insights

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add Bearer token
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('ceo_auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('ceo_auth_token');
      localStorage.removeItem('ceo_user_id');
      localStorage.removeItem('ceo_email');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication APIs
export const authAPI = {
  login: async (email, password) => {
    const response = await axiosInstance.post('/api/auth/login', { email, password });
    return response.data;
  },

  logout: async () => {
    try {
      await axiosInstance.post('/api/auth/logout');
    } catch (error) {
      console.log('Logout error:', error);
    }
    localStorage.removeItem('ceo_auth_token');
    localStorage.removeItem('ceo_user_id');
    localStorage.removeItem('ceo_email');
  },

  getProfile: async () => {
    const response = await axiosInstance.get('/api/auth/me');
    return response.data;
  },
};

// CEO Dashboard API
export const ceoAPI = {
  getDashboard: async () => {
    const response = await axiosInstance.get('/api/ceo/dashboard');
    return response.data;
  },
};

// Analytics APIs
export const analyticsAPI = {
  getOverview: async () => {
    const response = await axiosInstance.get('/api/analytics/overview');
    return response.data;
  },

  getGeography: async () => {
    const response = await axiosInstance.get('/api/analytics/geography');
    return response.data;
  },

  getHeatmap: async () => {
    const response = await axiosInstance.get('/api/analytics/heatmap');
    return response.data;
  },

  getForecast: async () => {
    const response = await axiosInstance.get('/api/analytics/forecast');
    return response.data;
  },

  getSegments: async () => {
    const response = await axiosInstance.get('/api/analytics/segments');
    return response.data;
  },

  getRules: async () => {
    const response = await axiosInstance.get('/api/analytics/rules');
    return response.data;
  },

  getAnomalies: async () => {
    const response = await axiosInstance.get('/api/analytics/anomalies');
    return response.data;
  },

  getChurnRisk: async () => {
    const response = await axiosInstance.get('/api/analytics/churn-risk');
    return response.data;
  },
};

// ML Inference APIs
export const mlAPI = {
  getRecommendations: async (customerId) => {
    const response = await axiosInstance.get(`/api/recommend/${customerId}`);
    return response.data;
  },

  getSegment: async (customerId) => {
    const response = await axiosInstance.get(`/api/segment/${customerId}`);
    return response.data;
  },

  getBasketSuggestions: async () => {
    const response = await axiosInstance.get('/api/basket/suggest');
    return response.data;
  },

  getSampleCustomers: async () => {
    const response = await axiosInstance.get('/api/customers/sample');
    return response.data;
  },
};

export default axiosInstance;
