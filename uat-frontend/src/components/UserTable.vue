<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h3>User Management</h3>
      <button @click="$emit('openModal')" class="btn btn-primary">+ Add User</button>
    </div>

    <table class="table table-striped">
      <thead class="table-dark">
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Role</th>
          <th>Organization</th>
          <th>System</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.role }}</td>
          <td>{{ user.organization?.name || 'N/A' }}</td>
          <td>{{ user.system?.name || 'N/A' }}</td>
          <td>
            <span :class="{'text-success': user.is_active, 'text-danger': !user.is_active}">
              {{ user.is_active ? 'Active' : 'Inactive' }}
            </span>
          </td>
          <td>
            <button @click="$emit('edit', user)" class="btn btn-warning btn-sm">Edit</button>
            <button @click="$emit('delete', user.id)" class="btn btn-danger btn-sm">Delete</button>
            <button @click="$emit('toggleStatus', user)" class="btn btn-secondary btn-sm">
              {{ user.is_active ? 'Deactivate' : 'Activate' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    users: Array
  }
};
</script>