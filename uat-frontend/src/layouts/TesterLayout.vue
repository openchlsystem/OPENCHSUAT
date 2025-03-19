<template>
  <div class="tester-layout">
    <nav class="sidebar">
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
    </nav>

    <div class="content">
      <header class="header">
        <h2>Tester Panel</h2>
      </header>
      <main>
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TesterLayout',
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
}

.sidebar ul {
  list-style: none;
  padding: 0;
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
}

.sidebar ul li a i {
  margin-right: 10px;
}

.sidebar ul li a.router-link-exact-active {
  font-weight: bold;
  color: #f8c146;
}

.content {
  flex-grow: 1;
  background: #f4f4f4;
  padding: 20px;
}

.header {
  background: white;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}
</style>
