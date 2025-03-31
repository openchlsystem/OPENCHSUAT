<template>
  <div class="tester-layout">
    <nav class="sidebar">
      <div class="sidebar-header">
        <h3>Tester Panel</h3>
      </div>
      <ul>
        <li>
          <router-link to="/tester/dashboard">
            <i class="fas fa-tachometer-alt"></i> Dashboard
          </router-link>
        </li>
        <li>
          <router-link to="/tester/assigned-tests">
            <i class="fas fa-tasks"></i> Assigned Tests
          </router-link>
        </li>
        <li>
          <router-link to="/tester/test-execution">
            <i class="fas fa-play-circle"></i> Test Execution
          </router-link>
        </li>
        <li>
          <router-link to="/tester/defect-reporting">
            <i class="fas fa-bug"></i> Report Defect
          </router-link>
        </li>
        <li>
          <router-link to="/tester/test-history">
            <i class="fas fa-history"></i> Test History
          </router-link>
        </li>
      </ul>
      <!-- Logout button at bottom of sidebar -->
      <div class="logout-container">
        <LogoutButton theme="tester"/>
      </div>
    </nav>

    <div class="content">
      <header class="header">
        <h2>Tester Panel</h2>
        <div class="user-info">
          <span class="welcome-message">Welcome, {{ userName }}</span>
          <LogoutButton 
            buttonText="Sign Out" 
            size="small" 
            theme="tester"
            class="header-logout"
          />
        </div>
      </header>
      <main>
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';
import { useAuthStore } from '@/store/auth';
import LogoutButton from '@/components/LogoutButton.vue';

export default {
  name: 'TesterLayout',
  components: {
    LogoutButton
  },
  setup() {
    const authStore = useAuthStore();
    const userName = computed(() => authStore.user?.name || 'Tester');

    return {
      userName
    };
  }
};
</script>

<style scoped>
.tester-layout {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 250px;
  background-color: #343a40;
  color: white;
  padding: 20px;
  display: flex;
  flex-direction: column;
  height: 100vh;
  position: fixed;
  left: 0;
  overflow-y: auto;
}

.sidebar-header h3 {
  color: #f8c146;
  margin-bottom: 20px;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  flex-grow: 1;
}

.sidebar ul li {
  margin: 15px 0;
}

.sidebar ul li a {
  text-decoration: none;
  color: white;
  font-size: 16px;
  display: flex;
  align-items: center;
  padding: 8px 10px;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.sidebar ul li a:hover {
  background-color: #495057;
}

.sidebar ul li a i {
  margin-right: 10px;
}

.sidebar ul li a.router-link-exact-active {
  font-weight: bold;
  color: #f8c146;
  background-color: rgba(248, 193, 70, 0.1);
}

/* Logout Container */
.logout-container {
  margin-top: auto;
  padding-top: 20px;
  border-top: 1px solid #495057;
  margin-bottom: 15px;
}

.content {
  flex-grow: 1;
  background: #f4f4f4;
  padding: 20px;
  margin-left: 250px;
}

.header {
  background: white;
  padding: 10px 15px;
  border-bottom: 1px solid #ddd;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.welcome-message {
  font-size: 14px;
  color: #666;
}

.header-logout :deep(.logout-btn) {
  background-color: #f8c146; /* Match tester theme color */
}

.header-logout :deep(.logout-btn:hover) {
  background-color: #e0ac35; /* Darker shade for hover */
}
</style>