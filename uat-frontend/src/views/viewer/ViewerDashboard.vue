<template>
    <div class="viewer-dashboard">
      <h1>Welcome to the Viewer Dashboard</h1>
      <div class="content">
        <p>This is the section for progress tracking and reporting for viewers.</p>
        <div class="stats">
          <div class="stat-card">
            <h3>Test Case Progress</h3>
            <p>Track the progress of the test cases assigned.</p>
          </div>
          <div class="stat-card">
            <h3>Defects Dashboard</h3>
            <p>View the current defects reported during tests.</p>
          </div>
          <div class="stat-card">
            <h3>Tester Performance</h3>
            <p>View the performance metrics of the testers.</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ViewerDashboard',
    data() {
      return {
        // You can add any data here if necessary, for now it's a simple viewer dashboard
      };
    },
    mounted() {
      // This is where you could fetch any data or run any setup when the component is mounted
    }
  };
  </script>
  
  <style scoped>
  .viewer-dashboard {
    padding: 20px;
  }
  
  .content {
    margin-top: 20px;
  }
  
  .stats {
    display: flex;
    gap: 20px;
    margin-top: 20px;
  }
  
  .stat-card {
    background-color: #f1f1f1;
    padding: 20px;
    border-radius: 8px;
    flex: 1;
    text-align: center;
  }
  
  .stat-card h3 {
    color: #333;
    font-size: 18px;
  }
  
  .stat-card p {
    color: #777;
    font-size: 14px;
  }
  </style>
  