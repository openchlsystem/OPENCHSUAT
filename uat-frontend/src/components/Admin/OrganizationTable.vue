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
          <td>{{ organization.name }}</td>
          <td>{{ organization.description }}</td>
          <td>{{ formatDate(organization.created_at) }}</td>
          <td>
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
</script>

<style scoped>
.table-responsive {
  margin-top: 20px;
}
</style>
