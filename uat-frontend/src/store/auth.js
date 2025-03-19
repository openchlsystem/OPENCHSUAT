import { defineStore } from 'pinia';
import axiosInstance from '@/utils/axios';  // Adjust the import path

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),
  actions: {
    async sendOTP(whatsappNumber) {
      console.log('Sending OTP to:', whatsappNumber);

      try {
        // Use axiosInstance instead of fetch
        const response = await axiosInstance.post('/api/auth/request-otp/', {
          whatsappNumber,
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
        // Use axiosInstance instead of fetch
        const response = await axiosInstance.post('/api/auth/verify-otp/', {
          whatsappNumber,
          otp: enteredOTP,
        });

        const user = response.data;
        console.log('OTP verified successfully:', user);

        // Check if the user is active
        if (!user.is_active) {
          throw new Error('Your account is inactive. Please contact support.');
        }

        // Save user data to state and localStorage
        this.user = user;
        localStorage.setItem('user', JSON.stringify(user));

        return user; // Return the user data for redirection
      } catch (error) {
        console.error('Error verifying OTP:', error);
        throw new Error(error.message || 'Invalid OTP. Please try again.');
      }
    },

    async registerUser(whatsappNumber, password) {
      console.log('Registering user...');

      try {
        // Use axiosInstance instead of fetch
        const response = await axiosInstance.post('/api/auth/register/', {
          whatsapp_number: whatsappNumber,
          password: password,
        });

        const user = response.data;
        console.log('User registered successfully:', user);
        return user;
      } catch (error) {
        console.error('Error registering user:', error);
        throw new Error(error.message || 'Registration failed. Please try again.');
      }
    },
  },
});