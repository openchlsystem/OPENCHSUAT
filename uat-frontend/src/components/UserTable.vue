<template>
    <div class="table-responsive">
      <table class="table table-bordered table-hover">
        <thead class="table-light">
          <tr>
            <th>#</th>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody v-if="!loading">
          <tr v-for="(user, index) in users" :key="user.id">
            <td>{{ index + 1 }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.role }}</td>
            <td>
              <span :class="user.status === 'Active' ? 'text-success' : 'text-danger'">
                {{ user.status }}
              </span>
            </td>
            <td>
              <button class="btn btn-sm btn-warning me-2" @click="$emit('edit', user)">
                <i class="bi bi-pencil"></i> Edit
              </button>
              <button class="btn btn-sm btn-secondary me-2" @click="$emit('toggleStatus', user.id)">
                <i class="bi bi-toggle-on"></i> 
                {{ user.status === 'Active' ? 'Deactivate' : 'Activate' }}
              </button>
            </td>
          </tr>
          <tr v-if="!users.length">
            <td colspan="6" class="text-center text-muted">No users available.</td>
          </tr>
        </tbody>
        <tbody v-else>
          <tr>
            <td colspan="6" class="text-center text-muted">Loading users...</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  defineProps({
    users: Array,
    loading: Boolean,
  });
  </script>
  
  <style scoped>
  .table {
    border-radius: 10px;
    overflow: hidden;
  }
  </style>
  