import { defineStore } from 'pinia';
import axiosInstance from '@/utils/axios';  // Adjust the import path if needed
import router from '@/router';  // Import the router for redirection

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('accessToken') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
    user: null,  // Store user info if needed
  }),
  actions: {
    /**
     * Register a new user.
     */
    async registerUser(whatsapp_number, name, password) {
      try {
        const response = await axiosInstance.post('/auth/register/', {
          whatsapp_number,
          name,
          password,
        });

        console.log('User registered successfully:', response.data);
        return response.data;  // Return success response
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
        const response = await axiosInstance.post('/auth/request-otp/', { whatsapp_number });

        console.log('OTP sent successfully:', response.data);

        // Store OTP in localStorage for verification (if needed)
        // localStorage.setItem('otp', response.data.otp); // Assuming the API returns the OTP

        return response.data; // Return API response for further use
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
        const response = await axiosInstance.post('/auth/verify-otp/', {
          whatsapp_number: whatsappNumber,
          otp: enteredOTP,
        });

        // Extract tokens from the response
        const { access, refresh, user } = response.data; // Assuming API returns `access`, `refresh`, and `user`

        // Save tokens to state and localStorage
        this.accessToken = access;
        this.refreshToken = refresh;
        this.user = user;
        localStorage.setItem('accessToken', access);
        localStorage.setItem('refreshToken', refresh);
        localStorage.setItem('user', JSON.stringify(user));

        console.log('OTP verified successfully. Tokens stored.');

        // Redirect user to dashboard
        // ✅ Redirect based on user role
    if (user.role === 'admin') {
      router.push({ name: 'AdminDashboard' });
    } else if (user.role === 'tester') {
      router.push({ name: 'TesterDashboard' });
    } else {
      router.push({ name: 'Login' }); // Fallback if role is undefined
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
    logoutUser() {
      console.log('Logging out user...');
      
      // Clear user data and tokens
      this.accessToken = null;
      this.refreshToken = null;
      this.user = null;
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('user');

      // Redirect to login page
      router.push({ name: 'Login' });
    },
  },
});
