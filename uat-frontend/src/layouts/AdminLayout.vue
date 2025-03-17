<template>
    <div class="admin-layout">
      <Sidebar />
      <div class="content-wrapper">
        <Navbar />
        <div class="content">
          <router-view />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Sidebar from '@/components/common/Sidebar.vue'
  import Navbar from '@/components/common/Navbar.vue'
  
  export default {
    components: {
      Sidebar,
      Navbar,
    },
  };
  </script>
  
  <style scoped>
  .admin-layout {
    display: flex;
    height: 100vh;
    overflow: hidden;
  }
  
  .content-wrapper {
    flex-grow: 1;
    margin-left: 260px; /* Matches sidebar width */
    display: flex;
    flex-direction: column;
  }
  
  .content {
    flex: 1;
    padding: 24px;
    overflow-y: auto;
    background-color: #f1f3f5;
  }
  </style>
  