<template>
  <div class="admin-layout">
    <!-- Sidebar -->
    <Sidebar />

    <!-- Main Content -->
    <div class="main-content">
      <!-- Header (optional) -->
      <div class="header">
        <h2>Admin Dashboard</h2>
      </div>

      <!-- Router View for Child Routes -->
      <router-view />
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/Sidebar.vue';

export default {
  name: 'AdminLayout',
  components: {
    Sidebar,
  },
};
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}

.main-content {
  margin-left: 250px; /* Adjust based on your sidebar width */
  padding: 20px;
  width: calc(100% - 250px);
  background-color: #f8f9fa; /* Light background for the main content */
}

.header {
  background-color: #ffffff;
  padding: 16px;
  border-bottom: 1px solid #e0e0e0;
  margin-bottom: 20px;
}

.header h2 {
  margin: 0;
  font-size: 24px;
  color: #333;
}
</style>