<template>
  <div class="card">
    <div class="card-body">
      <table class="table table-striped">
        <thead class="table-dark">
          <tr>
            <th>First Name</th>
            <th>WhatsApp</th>
            <th>Role</th>
            <th>Organization</th>
            <th>Registered By</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.first_name }}</td>
            <td>{{ user.whatsapp_number }}</td>
            <td>{{ user.role }}</td>
            <td>{{ user.organization }}</td>
            <td>
              <span class="badge bg-info">{{ user.created_by_admin ? "Admin" : "Self" }}</span>
            </td>
            <td>
              <span :class="user.is_active ? 'badge bg-success' : 'badge bg-danger'">
                {{ user.is_active ? "Active" : "Inactive" }}
              </span>
            </td>
            <td>
              <button @click="$emit('edit', user)" class="btn btn-warning btn-sm">Edit</button>
              <button @click="$emit('toggle-status', user)" class="btn btn-danger btn-sm">
                {{ user.is_active ? "Deactivate" : "Activate" }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    users: Array,
  },
};
</script>
