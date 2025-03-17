<template>
  <div>
    <div class="header">
      <h2>User Management</h2>
    </div>

    <!-- User Table -->
    <UserTable 
      :users="users" 
      @edit-user="openUserModal" 
      @toggle-status="toggleUserStatus"
    />

    <!-- User Modal -->
    <UserModal 
      v-if="showUserModal" 
      :user="selectedUser" 
      @close="closeUserModal" 
      @save="updateUser"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import UserTable from '@/components/UserTable.vue';
import UserModal from '@/components/UserModal.vue';

const users = ref([]);
const showUserModal = ref(false);
const selectedUser = ref(null);

// ✅ Fetch all users
const fetchUsers = async () => {
  try {
    // Simulate API call
    const response = await fetch('/api/users/');
    users.value = await response.json();
  } catch (error) {
    console.error('Error fetching users:', error);
  }
};

// ✅ Open Modal for Editing User
const openUserModal = (user) => {
  selectedUser.value = { ...user };
  showUserModal.value = true;
};

// ✅ Close Modal
const closeUserModal = () => {
  showUserModal.value = false;
  selectedUser.value = null;
};

// ✅ Update User
const updateUser = async (updatedUser) => {
  try {
    await fetch(`/api/users/${updatedUser.id}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(updatedUser)
    });

    // Refresh user list
    fetchUsers();
    closeUserModal();
  } catch (error) {
    console.error('Error updating user:', error);
  }
};

// ✅ Toggle User Status
const toggleUserStatus = async (userId) => {
  try {
    await fetch(`/api/users/${userId}/toggle-status/`, { method: 'PATCH' });
    fetchUsers();
  } catch (error) {
    console.error('Error toggling user status:', error);
  }
};

onMounted(() => {
  fetchUsers();
});
</script>

<style scoped>
.header {
  margin-bottom: 24px;
}

h2 {
  font-size: 1.5rem;
  color: #000;
  font-weight: 600;
}
</style>
