<template>
    <div class="dashboard-card">
      <div class="card-icon">
        <i :class="icon"></i>
      </div>
      <div class="card-content">
        <h3>{{ value }}</h3>
        <p>{{ title }}</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      title: String,
      value: [String, Number],
      icon: String
    }
  }
  </script>
  
  <style scoped>
  .dashboard-card {
    display: flex;
    align-items: center;
    background-color: #f9f9f9;
    border-left: 5px solid #ff7f00;
    padding: 16px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 16px;
    transition: all 0.3s ease;
  }
  
  .dashboard-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }
  
  .card-icon {
    font-size: 32px;
    color: #ff7f00;
    margin-right: 12px;
  }
  
  .card-content h3 {
    font-size: 20px;
    margin: 0;
    color: #333;
  }
  
  .card-content p {
    font-size: 14px;
    color: #777;
    margin: 4px 0 0;
  }
  </style>
  