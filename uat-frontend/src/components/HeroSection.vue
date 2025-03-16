<template>
    <div class="hero-container">
      <div class="hero-content">
        <h1>Welcome to the UAT System</h1>
        <p>Efficient and organized testing management system</p>
        <router-link to="/login">
          <button class="login-btn">Login</button>
        </router-link>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'HeroSection',
  };
  </script>
  
  <style scoped>
  .hero-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: #f8f9fa;
  }
  
  .hero-content {
    text-align: center;
    max-width: 600px;
    padding: 20px;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  }
  
  .hero-content h1 {
    font-size: 2.5rem;
    color: #367588;
    margin-bottom: 20px;
  }
  
  .hero-content p {
    font-size: 1.2rem;
    color: #444;
    margin-bottom: 30px;
  }
  
  .login-btn {
    background-color: #367588;
    color: white;
    padding: 12px 20px;
    border: none;
    border-radius: 4px;
    font-size: 1.2rem;
    cursor: pointer;
    text-decoration: none;
  }
  
  .login-btn:hover {
    background-color: #2d5f70;
  }
  </style>
  