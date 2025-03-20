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
        <td>{{ system.organization?.name || "N/A" }}</td>
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
defineProps({
  systems: Array
});
</script>

<style scoped>
.table {
  width: 100%;
}
</style>
