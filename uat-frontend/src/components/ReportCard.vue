<template>
    <div :class="['card', 'report-card', `border-${color}`]">
      <div class="card-body">
        <h5 class="card-title">{{ title }}</h5>
        <h2 :class="['card-value', `text-${color}`]">{{ value }}</h2>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({
    title: String,
    value: Number,
    color: {
      type: String,
      default: 'primary', // Options: primary, success, danger, warning, info, etc.
    },
  });
  </script>
  
  <style scoped>
  .report-card {
    border: 2px solid #e0e0e0;
    border-radius: 12px;
    transition: transform 0.2s ease-in-out;
    background-color: #fff;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
  }
  
  .report-card:hover {
    transform: translateY(-5px);
  }
  
  .card-title {
    font-weight: 600;
    color: #333;
    margin-bottom: 8px;
  }
  
  .card-value {
    font-size: 36px;
    font-weight: bold;
  }
  
  .border-primary {
    border-color: #007bff !important;
  }
  
  .border-success {
    border-color: #28a745 !important;
  }
  
  .border-danger {
    border-color: #dc3545 !important;
  }
  
  .border-warning {
    border-color: #ffc107 !important;
  }
  
  .text-primary {
    color: #007bff !important;
  }
  
  .text-success {
    color: #28a745 !important;
  }
  
  .text-danger {
    color: #dc3545 !important;
  }
  
  .text-warning {
    color: #ffc107 !important;
  }
  </style>
  