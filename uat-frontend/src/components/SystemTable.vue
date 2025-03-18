<template>
  <div>
    <table class="table table-striped">
      <thead class="table-dark">
        <tr>
          <th>Name</th>
          <th>Organization</th>
          <th>Description</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="system in systems" :key="system.id">
          <td>{{ system.name }}</td>
          <td>{{ system.organization.name }}</td>
          <td>{{ system.description }}</td>
          <td>
            <button @click="$emit('edit', system)" class="btn btn-warning btn-sm">Edit</button>
            <button @click="$emit('delete', system.id)" class="btn btn-danger btn-sm">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps(["systems"]);
</script>
