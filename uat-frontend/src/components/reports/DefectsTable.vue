<template>
    <div class="table-container">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Title</th>
            <th>Count</th>
            <th>Category</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="defect in defectsData" :key="defect.title">
            <td>{{ defect.title }}</td>
            <td>{{ defect.count }}</td>
            <td>{{ defect.category }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  import { defineProps } from 'vue';
  
  const props = defineProps({
    defectsData: {
      type: Array,
      required: true,
    },
  });
  </script>
  
  <style scoped>
  .table-container {
    margin-top: 20px;
  }
  </style>
  