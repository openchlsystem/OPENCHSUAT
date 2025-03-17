<template>
  <div class="admin-layout">
    <!-- Sidebar -->
    <Sidebar />

    <div class="dashboard-content">
      <div class="container-fluid admin-dashboard">
        <!-- Dashboard Metrics -->
        <div class="row g-3 mb-4">
          <div class="col-xl-4 col-md-6" v-for="(metric, index) in metricData" :key="index">
            <DashboardCard 
              :title="metric.title"
              :value="metric.value"
              :icon="metric.icon"
              :bgClass="metric.bgClass"
            />
          </div>
        </div>

        <!-- Performance Chart and Recent Activity -->
        <div class="row">
          <!-- Performance Chart -->
          <div class="col-lg-8 mb-4">
            <div class="card shadow-sm p-3">
              <h5 class="card-title mb-3">Performance Overview</h5>
              <PerformanceChart :data="performanceData.data" :labels="performanceData.labels" />
            </div>
          </div>
          
          <!-- Recent Activity -->
          <div class="col-lg-4">
            <div class="card shadow-sm p-3">
              <h5 class="card-title mb-3">Recent Activity</h5>
              <RecentActivity :activities="recentActivity" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useAdminDashboardStore } from '@/store/AdminDashboard.js';
import DashboardCard from '@/components/DashboardCard.vue';
import PerformanceChart from '@/components/PerformanceChart.vue';
import RecentActivity from '@/components/RecentActivity.vue';
import Sidebar from '@/components/Sidebar.vue';

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
/* Admin layout container */
.admin-layout {
  display: flex;
}

/* Sidebar width handling */
.sidebar {
  width: 250px; /* Fixed width for sidebar */
  flex-shrink: 0;
}

/* Dashboard content should not overlap sidebar */
.dashboard-content {
  flex-grow: 1;
  padding: 24px;
  margin-left: 250px; /* Ensure sidebar width is accounted for */
  background-color: #f8f9fa;
  min-height: 100vh;
  overflow-y: auto;
}

/* Dashboard container */
.admin-dashboard {
  padding: 20px;
}

/* Card styling */
.card {
  border-radius: 12px;
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

/* Color consistency */
.bg-warning {
  background-color: #ffcc00 !important;
}

.bg-success {
  background-color: #28a745 !important;
}

.bg-danger {
  background-color: #dc3545 !important;
}

.bg-primary {
  background-color: #007bff !important;
}

.bg-secondary {
  background-color: #6c757d !important;
}

h5 {
  font-size: 18px;
  font-weight: bold;
  color: #343a40;
}

/* Shadow for modern look */
.shadow-sm {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
}

/* Responsive handling */
@media (max-width: 768px) {
  .dashboard-content {
    margin-left: 0; /* Remove left margin on smaller screens */
    padding: 10px;
  }

  .sidebar {
    width: 100%; /* Sidebar takes full width on small screens */
    position: fixed;
    z-index: 1050;
  }
}
</style>
