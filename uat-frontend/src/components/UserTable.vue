<template>
  <div class="table-wrapper">
    <table class="table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Role</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.role }}</td>
          <td>
            <span :class="{ active: user.is_active, inactive: !user.is_active }">
              {{ user.is_active ? 'Active' : 'Inactive' }}
            </span>
          </td>
          <td>
            <button class="btn-primary" @click="$emit('edit-user', user)">Edit</button>
            <button 
              class="btn-secondary" 
              @click="$emit('toggle-status', user.id)"
            >
              {{ user.is_active ? 'Deactivate' : 'Activate' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({ users: Array });
defineEmits(['edit-user', 'toggle-status']);
</script>

<style scoped>
</style>
