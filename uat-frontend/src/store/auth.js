import { defineStore } from 'pinia';
import axiosInstance from '@/utils/axios';  // Adjust the import path
import router from '@/router';  // Import the router for redirection

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('accessToken') || null,  // Access token
    refreshToken: localStorage.getItem('refreshToken') || null, // Refresh token
  }),
  actions: {
    async sendOTP(whatsapp_number) {
      console.log('Sending OTP to:', whatsapp_number);

      try {
        const response = await axiosInstance.post('/api/auth/request-otp/', {
          whatsapp_number,
        });

        console.log('OTP sent successfully:', response.data);

        // Store OTP in localStorage for verification (if needed)
        localStorage.setItem('otp', response.data.otp); // Assuming the API returns the OTP

        return response.data; // Return the API response for further use
      } catch (error) {
        console.error('Error sending OTP:', error);
        throw new Error('Failed to send OTP. Please try again.');
      }
    },

    async verifyOTP(whatsappNumber, enteredOTP) {
      console.log('Verifying OTP...');

      try {
        const response = await axiosInstance.post('/api/auth/verify-otp/', {
          whatsapp_number: whatsappNumber,
          otp: enteredOTP,
        });

        // Extract tokens from the response
        const { access, refresh } = response.data; // Assuming the API returns `access` and `refresh` tokens

        // Save tokens to state and localStorage
        this.accessToken = access;
        this.refreshToken = refresh;
        localStorage.setItem('accessToken', access);
        localStorage.setItem('refreshToken', refresh);

        console.log('OTP verified successfully. Tokens stored.');

        // Redirect to the admin dashboard
        router.push({ name: 'AdminDashboard' });  // Redirect to the admin dashboard

        return response.data; // Return the API response for further use
      } catch (error) {
        console.error('Error verifying OTP:', error);
        throw new Error(error.message || 'Invalid OTP. Please try again.');
      }
    },
  },
});