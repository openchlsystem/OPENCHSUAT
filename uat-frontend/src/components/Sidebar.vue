<template>
  <div class="sidebar">
    <ul class="nav flex-column">
      <!-- Admin Pages -->
      <li v-if="userRole === 'admin'" class="nav-item">
        <router-link class="nav-link" to="/admin/dashboard" :class="{ active: isActive('/admin/dashboard') }">
          <i class="bi bi-speedometer2 me-2"></i> Dashboard
        </router-link>
      </li>
      <li v-if="userRole === 'admin'" class="nav-item">
        <router-link class="nav-link" to="/admin/defects" :class="{ active: isActive('/admin/defects') }">
          <i class="bi bi-bug me-2"></i> Defects
        </router-link>
      </li>
      <li v-if="userRole === 'admin'" class="nav-item">
        <router-link class="nav-link" to="/admin/reports" :class="{ active: isActive('/admin/reports') }">
          <i class="bi bi-graph-up me-2"></i> Reports
        </router-link>
      </li>
      <li v-if="userRole === 'admin'" class="nav-item">
        <router-link class="nav-link" to="/admin/settings" :class="{ active: isActive('/admin/settings') }">
          <i class="bi bi-gear me-2"></i> Settings
        </router-link>
      </li>
      <li v-if="userRole === 'admin'" class="nav-item">
        <router-link class="nav-link" to="/admin/system-management" :class="{ active: isActive('/admin/system-management') }">
          <i class="bi bi-server me-2"></i> System Management
        </router-link>
      </li>
      <li v-if="userRole === 'admin'" class="nav-item">
        <router-link class="nav-link" to="/admin/test-cases" :class="{ active: isActive('/admin/test-cases') }">
          <i class="bi bi-card-list me-2"></i> Test Cases
        </router-link>
      </li>
      <li v-if="userRole === 'admin'" class="nav-item">
        <router-link class="nav-link" to="/admin/users" :class="{ active: isActive('/admin/users') }">
          <i class="bi bi-people-fill me-2"></i> User Management
        </router-link>
      </li>
      <li v-if="userRole === 'admin'" class="nav-item">
        <router-link class="nav-link" to="/admin/functionalities" :class="{ active: isActive('/admin/functionalities') }">
          <i class="bi bi-tools me-2"></i> Functionality Management
        </router-link>
      </li>

      <!-- Tester Pages -->
      <li v-if="userRole === 'tester'" class="nav-item">
        <router-link class="nav-link" to="/tester/dashboard" :class="{ active: isActive('/tester/dashboard') }">
          <i class="bi bi-speedometer2 me-2"></i> Tester Dashboard
        </router-link>
      </li>
      <li v-if="userRole === 'tester'" class="nav-item">
        <router-link class="nav-link" to="/tester/assigned-tests" :class="{ active: isActive('/tester/assigned-tests') }">
          <i class="bi bi-list-check me-2"></i> Assigned Tests
        </router-link>
      </li>
      <li v-if="userRole === 'tester'" class="nav-item">
        <router-link class="nav-link" to="/tester/test-execution/1" :class="{ active: isActive('/tester/test-execution') }">
          <i class="bi bi-play-btn me-2"></i> Test Execution
        </router-link>
      </li>
      <li v-if="userRole === 'tester'" class="nav-item">
        <router-link class="nav-link" to="/tester/defect-report" :class="{ active: isActive('/tester/defect-report') }">
          <i class="bi bi-flag me-2"></i> Defect Report
        </router-link>
      </li>
      <li v-if="userRole === 'tester'" class="nav-item">
        <router-link class="nav-link" to="/tester/test-history" :class="{ active: isActive('/tester/test-history') }">
          <i class="bi bi-clock-history me-2"></i> Test History
        </router-link>
      </li>

      <!-- Reports (Available to Admin & Viewer) -->
      <li v-if="userRole === 'admin' || userRole === 'viewer'" class="nav-item">
        <router-link class="nav-link" to="/reports/defects" :class="{ active: isActive('/reports/defects') }">
          <i class="bi bi-bug me-2"></i> Defects Dashboard
        </router-link>
      </li>
      <li v-if="userRole === 'admin' || userRole === 'viewer'" class="nav-item">
        <router-link class="nav-link" to="/reports/progress" :class="{ active: isActive('/reports/progress') }">
          <i class="bi bi-graph-up me-2"></i> Test Case Progress
        </router-link>
      </li>
      <li v-if="userRole === 'admin' || userRole === 'viewer'" class="nav-item">
        <router-link class="nav-link" to="/reports/performance" :class="{ active: isActive('/reports/performance') }">
          <i class="bi bi-person-check me-2"></i> Tester Performance
        </router-link>
      </li>
      <li v-if="userRole === 'admin'" class="nav-item">
        <router-link class="nav-link" to="/reports/export" :class="{ active: isActive('/reports/export') }">
          <i class="bi bi-download me-2"></i> Export Reports
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();
const userRole = JSON.parse(localStorage.getItem('user'))?.role || 'viewer';

const isActive = (route) => {
  return router.currentRoute.value.path.startsWith(route);
};
</script>


<style scoped>
/* Sidebar container */
.sidebar {
  width: 240px;
  height: 100vh;
  background-color: #1f2937;
  padding: 20px;
  position: fixed;
  top: 0;
  left: 0;
  overflow-y: auto;
  border-right: 1px solid #374151;
  transition: width 0.3s ease;
  z-index: 1000;
}

/* Sidebar scrollbar styling */
.sidebar::-webkit-scrollbar {
  width: 6px;
}

.sidebar::-webkit-scrollbar-thumb {
  background-color: #4b5563;
  border-radius: 4px;
}

.sidebar::-webkit-scrollbar-track {
  background-color: #1f2937;
}

/* Nav Links */
.nav-link {
  color: #d1d5db;
  font-size: 16px;
  padding: 10px 16px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  transition: background-color 0.2s ease;
}

.nav-link i {
  font-size: 18px;
}

/* Hover and Active States */
.nav-link:hover {
  background-color: #374151;
  color: #ffffff;
}

.nav-link.active {
  background-color: #2563eb;
  color: #ffffff;
}

/* Nav Item */
.nav-item {
  margin-bottom: 6px;
}
</style>
