<!-- src/components/RecentActivity.vue -->
<template>
    <div class="card shadow-sm">
      <div class="card-header bg-success text-white">
        Recent Activity
      </div>
      <ul class="list-group list-group-flush">
        <li 
          class="list-group-item d-flex justify-content-between align-items-center" 
          v-for="activity in activities" 
          :key="activity.id"
        >
          <span>{{ activity.message }}</span>
          <span class="text-muted small">{{ activity.time }}</span>
        </li>
      </ul>
    </div>
  </template>
  
  <script setup>
  defineProps({
    activities: Array,
  });
  </script>
  
  <style scoped>
  .card {
    border-radius: 8px;
  }
  
  .list-group-item {
    font-size: 14px;
  }
  
  .list-group-item:last-child {
    border-bottom: none;
  }
  
  .text-muted {
    font-size: 12px;
  }
  </style>
  