<template>
    <div class="user-management-view">
      <div class="container">
        <!-- Header -->
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2 class="fw-bold">User Management</h2>
          <button class="btn btn-primary" @click="openModal">
            <i class="bi bi-person-plus"></i> Add User
          </button>
        </div>
  
        <!-- User Table -->
        <UserTable :users="users" @edit="editUser" @toggleStatus="toggleUserStatus" />
  
        <!-- User Modal -->
        <UserModal 
          v-model:show="showModal" 
          :userData="selectedUser" 
          @save="saveUser" 
        />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import UserTable from '@/components/UserTable.vue';
  import UserModal from '@/components/UserModal.vue';
  
  const users = ref([]);
  const showModal = ref(false);
  const selectedUser = ref(null);
  
  // Fetch users from backend
  const fetchUsers = async () => {
    try {
      const response = await axios.get('/api/users/');
      users.value = response.data;
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };
  
  onMounted(fetchUsers);
  
  const openModal = () => {
    selectedUser.value = null;
    showModal.value = true;
  };
  
  const editUser = (user) => {
    selectedUser.value = { ...user };
    showModal.value = true;
  };
  
  const toggleUserStatus = async (id) => {
    try {
      await axios.patch(`/api/users/${id}/toggle-status/`);
      fetchUsers();
    } catch (error) {
      console.error('Error updating status:', error);
    }
  };
  
  const saveUser = async (userData) => {
    try {
      if (userData.id) {
        await axios.put(`/api/users/${userData.id}/`, userData);
      } else {
        await axios.post('/api/users/', userData);
      }
      fetchUsers();
      showModal.value = false;
    } catch (error) {
      console.error('Error saving user:', error);
    }
  };
  </script>
  
  <style scoped>
  .user-management-view {
    padding: 20px;
  }
  </style>
  