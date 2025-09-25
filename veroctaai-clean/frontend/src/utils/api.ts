import axios from 'axios'

// Create axios instance with default configuration
// Frontend and backend are served by the same Flask app on the same port
const getApiBaseURL = () => {
  if ((import.meta as any).env?.VITE_API_URL) {
    return (import.meta as any).env.VITE_API_URL;
  }
  
  // Use relative URL since frontend and backend are served from the same Flask app
  return '/api';
};

const api = axios.create({
  baseURL: getApiBaseURL(),
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// No need to modify fetch URLs since we're using relative URLs
// The Flask app serves both frontend and API from the same port


// Request interceptor for adding auth tokens
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for handling errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API endpoints
export const endpoints = {
  // Auth
  login: '/auth/login',
  register: '/auth/register',
  me: '/auth/me',

  // Reports
  reports: '/reports',
  report: (id: number) => `/reports/${id}`,
  deleteReport: (id: number) => `/reports/${id}`,

  // Analysis
  upload: '/upload',
  spendScore: '/spend-score',
  downloadReport: '/report',

  // System
  health: '/health',
  verifyClone: '/verify-clone',
  docs: '/docs'
}

// Generic API functions
export const apiClient = {
  get: (url: string, config = {}) => api.get(url, config),
  post: (url: string, data = {}, config = {}) => api.post(url, data, config),
  put: (url: string, data = {}, config = {}) => api.put(url, data, config),
  delete: (url: string, config = {}) => api.delete(url, config),
  patch: (url: string, data = {}, config = {}) => api.patch(url, data, config),
}

export default api