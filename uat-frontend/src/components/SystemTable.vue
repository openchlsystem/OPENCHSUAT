<!-- SystemTable.vue - Updated with Functionality Navigation -->
<template>
  <table class="table table-striped">
    <thead>
      <tr>
        <th>#</th>
        <th>System Name</th>
        <th>Organization</th>
        <th>Description</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(system, index) in systems" :key="system.id">
        <td>{{ index + 1 }}</td>
        <td>
          <a href="#" @click.prevent="navigateToFunctionalities(system.id, system.name)" class="system-name">
            {{ system.name }}
          </a>
        </td>
        <td>{{ getOrganizationName(system.organization) }}</td>
        <td>{{ system.description || "N/A" }}</td>
        <td>
          <div class="d-flex gap-2">
            <button class="btn btn-primary btn-sm" @click="navigateToFunctionalities(system.id, system.name)">
              Functionalities
            </button>
            <button class="btn btn-warning btn-sm" @click="$emit('edit', system)">
              Edit
            </button>
            <button class="btn btn-danger btn-sm" @click="$emit('delete', system.id)">
              Delete
            </button>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
const props = defineProps({
  systems: Array,
  organizations: Array
});

const getOrganizationName = (orgId) => {
  if (!orgId || !props.organizations) return "N/A";
 
  const organization = props.organizations.find(org => org.id === orgId);
  return organization ? organization.name : "N/A";
};

// Function to navigate to functionalities for a specific system
const navigateToFunctionalities = (systemId, systemName) => {
  window.location.href = `/admin/functionalities?system_id=${systemId}&system_name=${encodeURIComponent(systemName)}`;
};
</script>

<style scoped>
.table {
  width: 100%;
}

.system-name {
  color: #007bff;
  font-weight: bold;
  text-decoration: none;
}

.system-name:hover {
  text-decoration: underline;
  cursor: pointer;
}
</style>