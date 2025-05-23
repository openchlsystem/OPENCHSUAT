import { defineStore } from 'pinia';
import axiosInstance from '@/utils/axios';
import router from '@/router';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    // Changed from accessToken to access_token to match router expectations
    access_token: localStorage.getItem('access_token') || null,
    refresh_token: localStorage.getItem('refresh_token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),
  
  getters: {
    // Add a getter for userRole that router uses
    userRole: (state) => state.user?.role || null,
    
    // Add a getter for isAuthenticated
    isAuthenticated: (state) => !!state.access_token
  },
  
  actions: {
    /**
     * Register a new user.
     */
    async registerUser(whatsapp_number, name, password) {
      try {
        const response = await axiosInstance.post('uat/auth/register/', {
          whatsapp_number,
          name,
          password,
        });

        console.log('User registered successfully:', response.data);
        return response.data;
      } catch (error) {
        console.error('Registration failed:', error.response?.data || error.message);
        throw new Error(error.response?.data?.detail || 'Registration failed. Please try again.');
      }
    },

    /**
     * Send OTP to the given WhatsApp number.
     */
    async sendOTP(whatsapp_number) {
      console.log('Sending OTP to:', whatsapp_number);

      try {
        const response = await axiosInstance.post('uat/auth/request-otp/', { whatsapp_number });
        console.log('OTP sent successfully:', response.data);
        return response.data;
      } catch (error) {
        console.error('Error sending OTP:', error);
        throw new Error('Failed to send OTP. Please try again.');
      }
    },

    /**
     * Verify OTP and log in the user.
     */
    async verifyOTP(whatsappNumber, enteredOTP) {
      console.log('Verifying OTP...');

      try {
        const response = await axiosInstance.post('uat/auth/verify-otp/', {
          whatsapp_number: whatsappNumber,
          otp: enteredOTP,
        });

        // Extract tokens from the response
        const { access, refresh, user } = response.data;

        // Save tokens to state and localStorage - using the same key names as router expects
        this.access_token = access;
        this.refresh_token = refresh;
        this.user = user;
        
        // Store with consistent naming
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
        localStorage.setItem('user', JSON.stringify(user));

        console.log('OTP verified successfully. Tokens stored.');

        // Redirect based on user role
        if (user.role === 'admin') {
          router.push({ name: 'AdminDashboard' });
        } else if (user.role === 'tester') {
          router.push({ name: 'TesterDashboard' });
        } else {
          router.push({ name: 'Home' }); // Fallback to home if role is undefined
        }

        return response.data;
      } catch (error) {
        console.error('Error verifying OTP:', error);
        throw new Error(error.response?.data?.detail || 'Invalid OTP. Please try again.');
      }
    },

    /**
     * Log out the user.
     */
    logout() {
      console.log('Logging out user...');
      
      // Clear user data and tokens
      this.access_token = null;
      this.refresh_token = null;
      this.user = null;
      
      // Clear localStorage with consistent naming
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');

      // Redirect to login page
      router.push({ name: 'Login' });
    },
    
    /**
     * Method to update user data if needed
     */
    updateUserData(userData) {
      this.user = userData;
      localStorage.setItem('user', JSON.stringify(userData));
    }
  },
});