// src/store/auth.js
import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),
  actions: {
    async sendOTP(whatsappNumber) {
      console.log('Sending OTP to:', whatsappNumber);

      try {
        // Call the API endpoint to send OTP
        const response = await fetch('/api/auth/request-otp/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ whatsappNumber }),
        });

        if (!response.ok) {
          throw new Error('Failed to send OTP');
        }

        const data = await response.json();
        console.log('OTP sent successfully:', data);

        // Store OTP in localStorage for verification (if needed)
        localStorage.setItem('otp', data.otp); // Assuming the API returns the OTP

        return data; // Return the API response for further use
      } catch (error) {
        console.error('Error sending OTP:', error);
        throw new Error('Failed to send OTP. Please try again.');
      }
    },

    async verifyOTP(whatsappNumber, enteredOTP) {
      console.log('Verifying OTP...');

      try {
        // Call the API endpoint to verify OTP
        const response = await fetch('/api/auth/verify-otp/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ whatsappNumber, otp: enteredOTP }),
        });

        if (!response.ok) {
          throw new Error('Failed to verify OTP');
        }

        const user = await response.json();
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
          const response = await fetch('/api/auth/register/', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({ whatsapp_number: whatsappNumber, password: password }),
          });
  
          if (!response.ok) {
              const errorData = await response.json();
              let errorMessage = 'Registration failed. Please try again.';
              if (errorData && errorData.detail) {
                  errorMessage = errorData.detail;
              } else if (errorData && errorData.whatsapp_number) {
                  errorMessage = errorData.whatsapp_number[0];
              } else if (errorData && errorData.password) {
                  errorMessage = errorData.password[0];
              }
  
              throw new Error(errorMessage);
          }
  
          const responseText = await response.text();
  
          if (!responseText) {
              throw new Error('Empty response from server.');
          }
  
          try {
              const user = JSON.parse(responseText);
              console.log('User registered successfully:', user);
              return user;
          } catch (jsonError) {
              console.error('Error parsing JSON:', jsonError);
              throw new Error('Invalid JSON response from server.');
          }
  
      } catch (error) {
          console.error('Error registering user:', error);
          throw new Error(error.message || 'Registration failed. Please try again.');
      }
  },

    // logout() {
    //   localStorage.removeItem('user');
    //   localStorage.removeItem('otp');
    //   this.user = null;
    // },
  },
});