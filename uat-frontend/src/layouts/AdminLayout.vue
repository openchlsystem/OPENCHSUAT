<template>
  <div class="layout">
    <!-- Sidebar -->
    <nav class="sidebar">
      <div class="sidebar-header">
        <h3>Admin Panel</h3>
      </div>
      <ul class="sidebar-links">
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
      </ul>
    </nav>

    <!-- Content Section -->
    <div class="content">
      <header class="header">
        <h2>Admin Dashboard</h2>
      </header>
      <main>
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminLayout',
};
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
}

/* Sidebar Styling */
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

/* Content Styling */
.content {
  margin-left: 250px;
  flex-grow: 1;
  background-color: #f8f9fa;
  padding: 20px;
}

.header {
  background-color: white;
  padding: 16px;
  border-bottom: 1px solid #ddd;
  font-size: 18px;
  font-weight: 500;
}
</style>
