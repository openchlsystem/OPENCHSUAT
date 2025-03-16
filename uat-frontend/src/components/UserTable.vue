<template>
  <div class="table-responsive">
    <table class="table table-bordered table-hover align-middle">
      <thead class="table-dark">
        <tr>
          <th>#</th>
          <th>Name</th>
          <th>Email</th>
          <th>Role</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
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
            <button 
              class="btn btn-sm btn-secondary" 
              @click="$emit('toggle-status', user)"
            >
              {{ user.status === 'Active' ? 'Deactivate' : 'Activate' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  users: Array
});

defineEmits(['edit', 'toggle-status']);
</script>

<style scoped>
</style>
