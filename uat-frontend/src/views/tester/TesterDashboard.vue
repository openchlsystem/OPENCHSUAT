<template>
  <div class="dashboard-container">
    <!-- Sidebar Component -->
    <Sidebar />

    <!-- Main Dashboard Content -->
    <div class="tester-dashboard">
      <div class="container-fluid">
        <!-- Row for Heading -->
        <div class="row">
          <div class="col-12">
            <h2 class="fw-bold mb-4 text-primary">
              🧪 Tester Dashboard
            </h2>
          </div>
        </div>

        <!-- Dashboard Cards (Status Overview) -->
        <div class="row gap-4">
          <div class="col-md-4">
            <DashboardCard 
              title="Total Assigned Tests" 
              :count="stats.assignedTests" 
              icon="bi-list-check" 
              class="bg-primary text-white shadow-sm"
            />
          </div>
          <div class="col-md-4">
            <DashboardCard 
              title="Tests In Progress" 
              :count="stats.inProgressTests" 
              icon="bi-clock-history" 
              class="bg-warning text-dark shadow-sm"
            />
          </div>
          <div class="col-md-4">
            <DashboardCard 
              title="Completed Tests" 
              :count="stats.completedTests" 
              icon="bi-check-circle" 
              class="bg-success text-white shadow-sm"
            />
          </div>
        </div>

        <!-- Quick Actions (Navigation) -->
        <div class="mt-4">
          <h4 class="text-muted mb-3">Quick Actions</h4>
          <div class="d-flex justify-content-start gap-3">
            <router-link to="/tester/assigned-tests" class="btn btn-outline-primary shadow-sm">
              <i class="bi bi-list-task"></i> View Assigned Tests
            </router-link>
            <router-link to="/tester/test-history" class="btn btn-outline-info shadow-sm">
              <i class="bi bi-clock-history"></i> View Test History
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import DashboardCard from '@/components/DashboardCard.vue';
import Sidebar from '@/components/Sidebar.vue';

const stats = ref({
  assignedTests: 10,
  inProgressTests: 4,
  completedTests: 6,
});
</script>

<style scoped>
/* Ensure the sidebar and content are displayed side by side */
.dashboard-container {
  display: flex;
}

/* Sidebar Styling */
.tester-dashboard {
  margin-left: 250px; /* Adjust for sidebar width */
  padding: 20px;
  background-color: #f8f9fa;
  min-height: 100vh;
}

/* Heading Styling */
.text-primary {
  color: #007bff;
}

h2 {
  font-size: 2.5rem;
  font-weight: bold;
}

h4 {
  font-size: 1.25rem;
  font-weight: 500;
}

/* Fix Row Gap */
.row.gap-4 {
  gap: 20px;
}

/* Button Styling */
.btn {
  padding: 10px 20px;
  font-size: 1rem;
  transition: transform 0.2s ease;
}

.btn:hover {
  transform: scale(1.05);
}

/* Shadow Styling */
.shadow-sm {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
</style>
