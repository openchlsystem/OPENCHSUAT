import axios from 'axios';

// Define the base URL for your backend API
const baseURL = 'http://127.0.0.1:8000/api'; // Replace with your actual backend API URL

// Create an axios instance with base URL and other defaults
const axiosInstance = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json', 
  },
});

// Request interceptor to handle token and authentication
axiosInstance.interceptors.request.use(
  (config) => {
    // If there's a token in localStorage (assuming token is stored there after login)
    const token = localStorage.getItem('authToken');
    
    if (token) {
      // Add token to the Authorization header if available
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    // Handle error before sending request
    return Promise.reject(error);
  }
);

// Response interceptor to handle any errors from API responses
axiosInstance.interceptors.response.use(
  (response) => {
    // Handle successful response (you can do something globally here)
    return response;
  },
  (error) => {
    // Handle error responses (e.g., expired token, unauthorized, etc.)
    if (error.response && error.response.status === 401) {
      // Redirect to login or perform a logout if token is expired
      localStorage.removeItem('authToken'); // Clear expired token
      window.location.href = '/login'; // Redirect to login page
    }
    
    return Promise.reject(error);
  }
);

export default axiosInstance;
