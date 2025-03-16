<template>
  <div class="d-flex">
    <!-- Sidebar Component -->
    <Sidebar />

    <!-- Main Dashboard Content -->
    <div class="tester-dashboard flex-fill">
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
        <div class="row g-4">
          <DashboardCard 
            title="Total Assigned Tests" 
            :count="stats.assignedTests" 
            icon="bi-list-check" 
            class="bg-primary text-white shadow-sm"
          />
          <DashboardCard 
            title="Tests In Progress" 
            :count="stats.inProgressTests" 
            icon="bi-clock-history" 
            class="bg-warning text-dark shadow-sm"
          />
          <DashboardCard 
            title="Completed Tests" 
            :count="stats.completedTests" 
            icon="bi-check-circle" 
            class="bg-success text-white shadow-sm"
          />
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
import Sidebar from '@/components/Sidebar.vue'; // Import Sidebar

const stats = ref({
  assignedTests: 10,
  inProgressTests: 4,
  completedTests: 6,
});
</script>

<style scoped>
.tester-dashboard {
  padding: 20px;
  background-color: #f8f9fa;
  min-height: 100vh;
}

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

.row g-4 {
  gap: 20px;
}

.btn {
  padding: 10px 20px;
  font-size: 1rem;
  transition: transform 0.2s ease;
}

.btn:hover {
  transform: scale(1.05);
}

.shadow-sm {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Styling for Sidebar */
.d-flex {
  display: flex;
}

.flex-fill {
  flex: 1;
}
</style>
