import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import axios from 'axios';

// Import global styles
import './assets/style.css'; // Ensure this path is correct for your project structure

// Create Pinia store
const pinia = createPinia();

// Global Axios configuration
axios.defaults.baseURL = 'http://localhost:8000/api'; // Replace with your actual backend URL
axios.defaults.headers['Content-Type'] = 'application/json';

// Set Authorization token dynamically
const token = localStorage.getItem('token');
if (token) {
  axios.defaults.headers['Authorization'] = `Bearer ${token}`;
}

// Create and mount the Vue app
const app = createApp(App);

app.use(pinia);
app.use(router);

app.mount('#app');
