import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const productAPI = {
  create: (productData) => api.post('/core/products/', productData),
  list: () => api.get('/core/products/'),
  get: (id) => api.get(`/core/products/${id}/`),
  update: (id, data) => api.put(`/core/products/${id}/`, data),
  delete: (id) => api.delete(`/core/products/${id}/`),
  platforms: () => api.get('/core/products/platforms/'),
  brandTones: () => api.get('/core/products/brand_tones/'),
};

export const listingAPI = {
  generate: (productId, platform) => api.post(`/listings/generate/${productId}/${platform}/`),
  list: () => api.get('/listings/generated/'),
  get: (id) => api.get(`/listings/generated/${id}/`),
  delete: (id) => api.delete(`/listings/generated/${id}/`),
};

export const userAPI = {
  profile: () => api.get('/auth/profile/'),
};

export default api;