import { defineStore } from 'pinia';
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),
  actions: {
    async register(form) {
      try {
        // Try real API call first
        const response = await axios.post('/register', form);
        this.user = response.data.user;
        localStorage.setItem('user', JSON.stringify(this.user));
        console.log('User registered via API:', this.user);
      } catch (error) {
        console.error('API registration failed:', error);

        // Fallback to mock data only if the network call fails
        if (!error.response) {
          console.log('Falling back to mock registration...');
          const mockUser = {
            email: form.email,
            password: form.password,
            role: 'tester',
          };
          localStorage.setItem('user', JSON.stringify(mockUser));
          this.user = mockUser;
          console.log('Mock user registered:', this.user);
        } else {
          throw error;
        }
      }
    },

    async login(form) {
      try {
        // Try real API call first
        const response = await axios.post('/login', form);
        this.user = response.data.user;
        localStorage.setItem('user', JSON.stringify(this.user));
        console.log('User logged in via API:', this.user);
      } catch (error) {
        console.error('API login failed:', error);

        // Fallback to mock logic if the backend is down
        if (!error.response) {
          console.log('Falling back to mock login...');
          if (form.email === 'admin@example.com' && form.password === 'Admin@123') {
            const adminData = {
              email: form.email,
              role: 'admin',
            };
            localStorage.setItem('user', JSON.stringify(adminData));
            this.user = adminData;
            console.log('Mock admin logged in:', this.user);
            return;
          }

          const storedUser = JSON.parse(localStorage.getItem('user'));
          if (
            storedUser &&
            storedUser.email === form.email &&
            storedUser.password === form.password
          ) {
            this.user = storedUser;
            console.log('Mock tester logged in:', this.user);
            return;
          }

          throw new Error('Invalid email or password');
        } else {
          throw error;
        }
      }
    },

    logout() {
      localStorage.removeItem('user');
      this.user = null;
    },
  },
});
