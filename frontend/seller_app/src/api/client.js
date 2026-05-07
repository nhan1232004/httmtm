// API client configuration with axios
// Handles Bearer token authentication, error handling, and base URL configuration
// Token stored in localStorage as 'seller_auth_token'

import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

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
    const token = localStorage.getItem('seller_auth_token');
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
    // Handle 401 Unauthorized
    if (error.response?.status === 401) {
      localStorage.removeItem('seller_auth_token');
      localStorage.removeItem('seller_user_id');
      localStorage.removeItem('seller_email');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth APIs
export const authAPI = {
  // Send OTP to email
  sendOTP: async (email) => {
    const response = await axiosInstance.post('/api/auth/register/send-otp', { email });
    return response.data;
  },

  // Verify OTP and get token
  verifyOTP: async (email, otp) => {
    const response = await axiosInstance.post('/api/auth/register/verify-otp', {
      email,
      code: otp,
      name: email.split('@')[0],
      password: 'TempPass123!',
      role: 'seller'
    });
    return response.data;
  },

  // Logout
  logout: async () => {
    try {
      await axiosInstance.post('/api/auth/logout');
    } catch (error) {
      console.log('Logout error:', error);
    }
    localStorage.removeItem('seller_auth_token');
    localStorage.removeItem('seller_user_id');
    localStorage.removeItem('seller_email');
  },
};

// Dashboard APIs
export const dashboardAPI = {
  // Get dashboard overview stats
  getStats: async () => {
    const response = await axiosInstance.get('/api/seller/dashboard/stats');
    return response.data;
  },

  // Get revenue trend data
  getRevenueTrend: async (days = 30) => {
    const response = await axiosInstance.get(`/api/seller/dashboard/revenue-trend?days=${days}`);
    return response.data;
  },
};

// Orders APIs
export const ordersAPI = {
  // Get seller's orders
  getOrders: async (page = 1, limit = 20, status = null) => {
    let url = `/api/seller/orders?page=${page}&limit=${limit}`;
    if (status) {
      url += `&status=${status}`;
    }
    const response = await axiosInstance.get(url);
    return response.data;
  },

  // Get order details
  getOrderDetails: async (orderId) => {
    const response = await axiosInstance.get(`/api/seller/orders/${orderId}`);
    return response.data;
  },

  // Update order status
  updateOrderStatus: async (orderId, status) => {
    const response = await axiosInstance.patch(`/api/seller/orders/${orderId}`, { status });
    return response.data;
  },
};

// Products APIs
export const productsAPI = {
  // Get all seller's products
  getProducts: async (page = 1, limit = 20, search = null) => {
    let url = `/api/seller/products?page=${page}&limit=${limit}`;
    if (search) {
      url += `&search=${encodeURIComponent(search)}`;
    }
    const response = await axiosInstance.get(url);
    return response.data;
  },

  // Get product details
  getProductDetails: async (productId) => {
    const response = await axiosInstance.get(`/api/seller/products/${productId}`);
    return response.data;
  },

  // Create new product
  createProduct: async (productData) => {
    const response = await axiosInstance.post('/api/seller/products', productData);
    return response.data;
  },

  // Update product
  updateProduct: async (productId, productData) => {
    const response = await axiosInstance.patch(`/api/seller/products/${productId}`, productData);
    return response.data;
  },

  // Delete product
  deleteProduct: async (productId) => {
    const response = await axiosInstance.delete(`/api/seller/products/${productId}`);
    return response.data;
  },

  // Get product categories
  getCategories: async () => {
    const response = await axiosInstance.get('/api/seller/products/categories');
    return response.data;
  },
};

// Analytics APIs
export const analyticsAPI = {
  // Get sales by category
  getSalesByCategory: async (days = 30) => {
    const response = await axiosInstance.get(`/api/seller/analytics/sales-by-category?days=${days}`);
    return response.data;
  },

  // Get top products
  getTopProducts: async (limit = 10) => {
    const response = await axiosInstance.get(`/api/seller/analytics/top-products?limit=${limit}`);
    return response.data;
  },

  // Get customer insights
  getCustomerInsights: async () => {
    const response = await axiosInstance.get('/api/seller/analytics/customer-insights');
    return response.data;
  },

  // Get recommendations
  getRecommendations: async () => {
    const response = await axiosInstance.get('/api/seller/analytics/recommendations');
    return response.data;
  },
};

// Account APIs
export const accountAPI = {
  // Get seller profile
  getProfile: async () => {
    const response = await axiosInstance.get('/api/seller/account/profile');
    return response.data;
  },

  // Update seller profile
  updateProfile: async (profileData) => {
    const response = await axiosInstance.patch('/api/seller/account/profile', profileData);
    return response.data;
  },

  // Update password
  updatePassword: async (currentPassword, newPassword) => {
    const response = await axiosInstance.patch('/api/seller/account/password', {
      currentPassword,
      newPassword,
    });
    return response.data;
  },

  // Get seller settings
  getSettings: async () => {
    const response = await axiosInstance.get('/api/seller/account/settings');
    return response.data;
  },

  // Update seller settings
  updateSettings: async (settingsData) => {
    const response = await axiosInstance.patch('/api/seller/account/settings', settingsData);
    return response.data;
  },
};

export default axiosInstance;
