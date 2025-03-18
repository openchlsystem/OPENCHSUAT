<template>
  <div class="admin-layout">
    <Sidebar :user-role="'admin'" />
    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/Sidebar.vue';

export default {
  name: 'AdminLayout',
  components: {
    Sidebar
  }
};
</script>


<style scoped>
.admin-layout {
  display: flex;
}

.main-content {
  margin-left: 250px;
  padding: 20px;
  width: calc(100% - 250px);
}

.header {
  background-color: #f8f9fa;
  padding: 12px;
  border-bottom: 1px solid #e0e0e0;
}
</style>
