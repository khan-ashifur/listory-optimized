import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

console.log('API_BASE_URL:', API_BASE_URL);
console.log('Environment:', process.env.REACT_APP_API_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Request interceptor to set content type
api.interceptors.request.use((config) => {
  console.log('=== AXIOS REQUEST DEBUG ===');
  console.log('Full URL:', config.baseURL + config.url);
  console.log('Method:', config.method);
  console.log('Request Data:', JSON.stringify(config.data, null, 2));
  console.log('Request Headers:', JSON.stringify(config.headers.toJSON ? config.headers.toJSON() : config.headers, null, 2));
  
  // Set content type if not FormData (for file uploads)
  if (!config.data || !(config.data instanceof FormData)) {
    config.headers['Content-Type'] = 'application/json';
  }
  
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
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
  getImages: (id) => api.get(`/listings/generated/${id}/images/`),
  generateImages: (id) => api.post(`/listings/generated/${id}/generate_images/`),
  regenerateImages: (id) => api.post(`/listings/generated/${id}/regenerate_images/`),
};


export default api;