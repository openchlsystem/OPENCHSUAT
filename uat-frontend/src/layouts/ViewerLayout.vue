<template>
    <div class="viewer-layout">
      <Sidebar />
      <div class="content">
        <Navbar />
        <router-view />
      </div>
    </div>
  </template>
  
  <script>
  import Sidebar from '@/components/Sidebar.vue'
  import Navbar from '@/components/Navbar.vue'
  
  export default {
    components: {
      Sidebar,
      Navbar,
    },
  }
  </script>
  
  <style scoped>
  .viewer-layout {
    display: flex;
    height: 100vh;
  }
  
  .content {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
  }
  </style>
  