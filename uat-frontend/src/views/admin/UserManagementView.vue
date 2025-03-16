<template>
  <div class="user-management-view container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="fw-bold text-orange">User Management</h2>
      <button class="btn btn-dark" @click="openModal">
        <i class="bi bi-person-plus me-2"></i> Add User
      </button>
    </div>

    <UserTable 
      :users="users" 
      @edit="editUser"
      @toggle-status="toggleUserStatus"
    />

    <UserModal 
      :showModal="showModal"
      :modalTitle="modalTitle"
      :userData="currentUser"
      @close="closeModal"
      @submit="saveUser"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import UserTable from '@/components/UserTable.vue';
import UserModal from '@/components/UserModal.vue';

const users = ref([]);
const showModal = ref(false);
const modalTitle = ref('');
const currentUser = ref(null);

const fetchUsers = async () => {
  const response = await axios.get('/api/users/');
  users.value = response.data;
};

onMounted(fetchUsers);

const openModal = () => {
  modalTitle.value = 'Add User';
  currentUser.value = null;
  showModal.value = true;
};

const editUser = (user) => {
  modalTitle.value = 'Edit User';
  currentUser.value = { ...user };
  showModal.value = true;
};

const toggleUserStatus = async (user) => {
  await axios.patch(`/api/users/${user.id}/toggle-status/`);
  fetchUsers();
};

const saveUser = async (data) => {
  if (data.id) {
    await axios.put(`/api/users/${data.id}/`, data);
  } else {
    const response = await axios.post('/api/users/', data);
    users.value.push(response.data); // ✅ Add user directly to list
  }
  
  showModal.value = false;
  alert(data.id ? 'User updated successfully!' : 'User created successfully!');
};

const closeModal = () => {
  showModal.value = false;
};
</script>

<style scoped>
.text-orange {
  color: #fd7e14;
}
</style>
