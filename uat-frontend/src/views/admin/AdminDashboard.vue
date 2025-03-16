<!-- src/views/Admin/AdminDashboard.vue -->
<template>
    <div class="container-fluid admin-dashboard">
      <!-- Dashboard Metrics -->
      <div class="row g-3 mb-4">
        <div class="col-md-4 col-sm-6" v-for="(metric, index) in metricData" :key="index">
          <DashboardCard 
            :title="metric.title"
            :value="metric.value"
            :icon="metric.icon"
            :bgClass="metric.bgClass"
          />
        </div>
      </div>
  
      <!-- Performance Chart -->
      <div class="row mb-4">
        <div class="col-lg-8">
          <PerformanceChart :data="performanceData.data" :labels="performanceData.labels" />
        </div>
        
        <!-- Recent Activity -->
        <div class="col-lg-4">
          <RecentActivity :activities="recentActivity" />
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, computed } from 'vue';
  import { useAdminDashboardStore } from '@/store/adminDashboard';
  import DashboardCard from '@/components/DashboardCard.vue';
  import PerformanceChart from '@/components/PerformanceChart.vue';
  import RecentActivity from '@/components/RecentActivity.vue';
  
  const store = useAdminDashboardStore();
  
  onMounted(() => {
    store.fetchDashboardData();
  });
  
  const metricData = computed(() => [
    { title: 'Total Test Cases', value: store.metrics.totalTestCases, icon: 'fas fa-tasks', bgClass: 'bg-warning' },
    { title: 'Passed Tests', value: store.metrics.passedTests, icon: 'fas fa-check-circle', bgClass: 'bg-success' },
    { title: 'Failed Tests', value: store.metrics.failedTests, icon: 'fas fa-times-circle', bgClass: 'bg-danger' },
    { title: 'Blocked Tests', value: store.metrics.blockedTests, icon: 'fas fa-exclamation-triangle', bgClass: 'bg-warning' },
    { title: 'Total Testers', value: store.metrics.totalTesters, icon: 'fas fa-user', bgClass: 'bg-primary' },
    { title: 'Defects Reported', value: store.metrics.defectsReported, icon: 'fas fa-bug', bgClass: 'bg-secondary' },
  ]);
  
  const { performanceData, recentActivity } = store;
  </script>
  
  <style scoped>
  .admin-dashboard {
    padding: 24px;
  }
  
  .card {
    border-radius: 12px;
  }
  
  .g-3 {
    --bs-gutter-x: 1.5rem;
  }
  
  .row {
    margin-bottom: 24px;
  }
  </style>
  