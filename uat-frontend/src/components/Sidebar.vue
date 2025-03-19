<template>
  <div class="sidebar">
    <div class="sidebar-header">
      <h3>Application Panel</h3>
    </div>
    <ul class="sidebar-links">
      <!-- Admin Links -->
      <li>
        <router-link to="/admin/dashboard" exact-active-class="active-link" aria-label="Dashboard">
          <i class="fas fa-tachometer-alt"></i> Dashboard
        </router-link>
      </li>
      <li>
        <router-link to="/admin/organizations" exact-active-class="active-link" aria-label="Organizations">
          <i class="fas fa-building"></i> Organizations
        </router-link>
      </li>
      <li>
        <router-link to="/admin/systems" exact-active-class="active-link" aria-label="Systems">
          <i class="fas fa-desktop"></i> Systems
        </router-link>
      </li>
      <li>
        <router-link to="/admin/functionalities" exact-active-class="active-link" aria-label="Functionalities">
          <i class="fas fa-cogs"></i> Functionalities
        </router-link>
      </li>
      <li>
        <router-link to="/admin/test-cases" exact-active-class="active-link" aria-label="Test Cases">
          <i class="fas fa-vial"></i> Test Cases
        </router-link>
      </li>
      <li>
        <router-link to="/admin/defects" exact-active-class="active-link" aria-label="Defects">
          <i class="fas fa-bug"></i> Defects
        </router-link>
      </li>
      <li>
        <router-link to="/admin/reports" exact-active-class="active-link" aria-label="Reports">
          <i class="fas fa-chart-bar"></i> Reports
        </router-link>
      </li>
      <li>
        <router-link to="/admin/settings" exact-active-class="active-link" aria-label="Settings">
          <i class="fas fa-cog"></i> Settings
        </router-link>
      </li>
      <li>
        <router-link to="/admin/users" exact-active-class="active-link" aria-label="Users">
          <i class="fas fa-users"></i> Users
        </router-link>
      </li>

      <!-- Tester Links -->
      <li>
        <router-link to="/tester/dashboard" exact-active-class="active-link" aria-label="Tester Dashboard">
          <i class="fas fa-tachometer-alt"></i> Tester Dashboard
        </router-link>
      </li>
      <li>
        <router-link to="/tester/assigned-tests" exact-active-class="active-link" aria-label="Assigned Tests">
          <i class="fas fa-list"></i> Assigned Tests
        </router-link>
      </li>
      <li>
        <router-link to="/tester/test-execution" exact-active-class="active-link" aria-label="Test Execution">
          <i class="fas fa-play-circle"></i> Test Execution
        </router-link>
      </li>
      <li>
        <router-link to="/tester/defect-reporting" exact-active-class="active-link" aria-label="Defect Reporting">
          <i class="fas fa-bug"></i> Defect Reporting
        </router-link>
      </li>
      <li>
        <router-link to="/tester/test-history" exact-active-class="active-link" aria-label="Test History">
          <i class="fas fa-history"></i> Test History
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'Sidebar',
};
</script>

<style scoped>
.sidebar {
  width: 250px;
  height: 100vh;
  background-color: #343a40;
  color: white;
  padding: 20px;
  position: fixed;
  left: 0;
  top: 0;
  overflow-y: auto;
}

.sidebar-header h3 {
  color: #ff7f00;
  margin-bottom: 20px;
}

.sidebar-links {
  list-style: none;
  padding: 0;
}

.sidebar-links li {
  margin-bottom: 12px;
}

.sidebar-links a {
  display: flex;
  align-items: center;
  color: #ccc;
  text-decoration: none;
  padding: 10px 14px;
  border-radius: 4px;
  transition: background 0.3s ease;
}

.sidebar-links a i {
  margin-right: 10px;
}

.sidebar-links a:hover {
  background-color: #495057;
}

.active-link {
  background-color: #ff7f00;
  color: #fff;
}
</style>