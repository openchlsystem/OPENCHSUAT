<template>
    <div class="tester-dashboard">
      <div class="container">
        <h2 class="fw-bold mb-4">🧪 Tester Dashboard</h2>
  
        <!-- Dashboard Cards -->
        <div class="row">
          <DashboardCard 
            title="Total Assigned Tests" 
            :count="stats.assignedTests" 
            icon="bi-list-check" 
            class="bg-primary"
          />
          <DashboardCard 
            title="Tests In Progress" 
            :count="stats.inProgressTests" 
            icon="bi-clock-history" 
            class="bg-warning"
          />
          <DashboardCard 
            title="Completed Tests" 
            :count="stats.completedTests" 
            icon="bi-check-circle" 
            class="bg-success"
          />
        </div>
  
        <!-- Quick Access -->
        <div class="mt-4">
          <h4>Quick Actions</h4>
          <router-link to="/tester/assigned-tests" class="btn btn-outline-primary">
            <i class="bi bi-list-task"></i> View Assigned Tests
          </router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import DashboardCard from '@/components/DashboardCard.vue';
  
  const stats = ref({
    assignedTests: 10,
    inProgressTests: 4,
    completedTests: 6,
  });
  </script>
  
  <style scoped>
  .tester-dashboard {
    padding: 20px;
  }
  </style>
  