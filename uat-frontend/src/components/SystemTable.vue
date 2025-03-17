<template>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>System Name</th>
          <th>Description</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="system in systems" :key="system.id">
          <td>{{ system.id }}</td>
          <td>{{ system.name }}</td>
          <td>{{ system.description }}</td>
          <td>
            <button @click="$emit('edit', system)">Edit</button>
            <button @click="$emit('delete', system.id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </template>
  
  <script setup>
  defineProps(["systems"]);
  </script>
  
  <style scoped>
  table {
    width: 100%;
    border-collapse: collapse;
  }
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
  }
  th {
    background: #f4f4f4;
  }
  button {
    margin: 5px;
    padding: 5px 10px;
    border: none;
    cursor: pointer;
  }
  </style>
  