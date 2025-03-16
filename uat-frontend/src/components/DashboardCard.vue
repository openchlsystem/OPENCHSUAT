<template>
    <div :class="`dashboard-card border-${color}`">
      <div class="card-body d-flex align-items-center">
        <div class="icon-wrapper">
          <i :class="`bi bi-${icon}`"></i>
        </div>
        <div class="card-content">
          <h6 class="card-title">{{ title }}</h6>
          <h4 class="card-value">{{ value }}</h4>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({
    title: String,
    value: Number,
    icon: String,
    color: String,
  });
  </script>
  
  <style scoped>
  /* Dashboard Card Styling */
  .dashboard-card {
    background-color: #ffffff;
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: pointer;
    height: 120px;
    display: flex;
    align-items: center;
  }
  
  .dashboard-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
  }
  
  .card-body {
    display: flex;
    align-items: center;
  }
  
  .icon-wrapper {
    width: 50px;
    height: 50px;
    background-color: var(--bs-gray-100);
    border-radius: 12px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-right: 16px;
  }
  
  .icon-wrapper i {
    font-size: 28px;
    color: var(--bs-gray-600);
  }
  
  .card-content {
    display: flex;
    flex-direction: column;
  }
  
  .card-title {
    font-size: 16px;
    font-weight: 500;
    color: #666;
    margin-bottom: 4px;
  }
  
  .card-value {
    font-size: 28px;
    font-weight: 700;
    color: #333;
    margin: 0;
  }
  
  /* Border Color Variants */
  .border-primary {
    border-left: 6px solid #4caf50;
  }
  
  .border-danger {
    border-left: 6px solid #f44336;
  }
  
  .border-success {
    border-left: 6px solid #2196f3;
  }
  
  .border-warning {
    border-left: 6px solid #ff9800;
  }
  
  /* Hover Effects for Better Interaction */
  .dashboard-card:hover .icon-wrapper i {
    color: var(--bs-gray-900);
  }
  </style>
  