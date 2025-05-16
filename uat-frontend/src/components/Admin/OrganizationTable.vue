//=============================================================================
// FILE 1: OrganizationTable.vue - REPLACE YOUR EXISTING FILE WITH THIS
//=============================================================================

<template>
  <div class="table-responsive">
    <table class="table table-striped">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Description</th>
          <th>Created At</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="organization in organizations" :key="organization.id">
          <td>{{ organization.id }}</td>
          <td>
            <a href="#" @click.prevent="navigateToSystems(organization.id)" class="org-name">
              {{ organization.name }}
            </a>
          </td>
          <td>{{ organization.description }}</td>
          <td>{{ formatDate(organization.created_at) }}</td>
          <td>
            <button class="btn btn-sm btn-info me-2" @click="navigateToSystems(organization.id)">
              View Systems
            </button>
            <button class="btn btn-sm btn-primary me-2" @click="$emit('edit', organization)">
              Edit
            </button>
            <button class="btn btn-sm btn-danger" @click="$emit('delete', organization.id)">
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script setup>
defineProps({
  organizations: {
    type: Array,
    required: true,
  },
});
defineEmits(['edit', 'delete']);
const formatDate = (date) => {
  return new Date(date).toLocaleDateString();
};

// Function to navigate to systems page filtered by organization
const navigateToSystems = (orgId) => {
  window.location.href = `/admin/systems?org_id=${orgId}`;
};
</script>
<style scoped>
.table-responsive {
  margin-top: 20px;
}

.org-name {
  color: #007bff;
  font-weight: bold;
  text-decoration: none;
}

.org-name:hover {
  text-decoration: underline;
  cursor: pointer;
}

.btn-info {
  background-color: #17a2b8;
  border-color: #17a2b8;
  color: white;
}

.btn-info:hover {
  background-color: #138496;
  border-color: #138496;
  color: white;
}
</style>