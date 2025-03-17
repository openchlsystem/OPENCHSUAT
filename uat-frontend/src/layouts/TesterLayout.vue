<template>
    <div class="tester-layout">
      <Sidebar />
      <div class="content">
        <Navbar />
        <router-view />
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
  }
  </script>
  
  <style scoped>
  .tester-layout {
    display: flex;
    height: 100vh;
  }
  
  .content {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
  }
  </style>
  