import axios from 'axios';

// Define the base URL for your backend API
//const baseURL = 'http://127.0.0.1:8000/uat'; // Replace with your actual backend API URL
const baseURL = 'https://backend.bitz-itc.com/uat'; // Replace with your actual backend API URL

// Create an axios instance
const axiosInstance = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Flag to prevent multiple refresh requests at the same time
let isRefreshing = false;
let refreshSubscribers = [];

// Function to add subscribers who need the new token
const subscribeTokenRefresh = (callback) => {
  refreshSubscribers.push(callback);
};

// Function to notify all subscribers about the new token
const onRefreshed = (newToken) => {
  refreshSubscribers.forEach((callback) => callback(newToken));
  refreshSubscribers = [];
};

// Request interceptor to attach the access token
axiosInstance.interceptors.request.use(
  (config) => {
    // Use access_token to match what's used in the router
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token expiration
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If 401 Unauthorized error and request is not already retried
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      if (isRefreshing) {
        // Wait for token refresh to complete before retrying
        return new Promise((resolve) => {
          subscribeTokenRefresh((newToken) => {
            originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
            resolve(axios(originalRequest));
          });
        });
      }

      isRefreshing = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token'); // Use refresh_token to be consistent
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }

        const response = await axios.post(`${baseURL}/token/refresh/`, {
          refresh: refreshToken,
        });

        const newAccessToken = response.data.access;
        localStorage.setItem('access_token', newAccessToken); // Store as access_token
        axiosInstance.defaults.headers['Authorization'] = `Bearer ${newAccessToken}`;

        // Notify all subscribers about the new token
        onRefreshed(newAccessToken);

        // Retry the original request
        return axiosInstance(originalRequest);
      } catch (err) {
        // Clear tokens
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');

        // Use window.location.href = '/login' but don't alert first
        // This will allow the router guard to handle the redirect properly
        window.location.href = '/login';
        return Promise.reject(err);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default axiosInstance;