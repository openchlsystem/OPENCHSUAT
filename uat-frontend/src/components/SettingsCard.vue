<template>
    <div class="card settings-card" @click="$emit('click')">
      <div class="card-body d-flex align-items-center">
        <i :class="['bi', icon, 'me-3', 'fs-1', 'text-primary']"></i>
        <div>
          <h5 class="card-title mb-1">{{ title }}</h5>
          <p class="card-text text-muted">{{ description }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({
    title: String,
    description: String,
    icon: String
  });
  </script>
  
  <style scoped>
  .settings-card {
    cursor: pointer;
    transition: box-shadow 0.2s ease-in-out;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
  }
  .settings-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
  </style>
  