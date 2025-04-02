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
        <td>{{ system.name }}</td>
        <td>{{ getOrganizationName(system.organization) }}</td>
        <td>{{ system.description || "N/A" }}</td>
        <td>
          <button class="btn btn-sm btn-warning me-2" @click="$emit('edit', system)">Edit</button>
          <button class="btn btn-sm btn-danger" @click="$emit('delete', system.id)">Delete</button>
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
</script>

<style scoped>
.table {
  width: 100%;
}
</style>