<template>
    <div class="test-history-table">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Test Name</th>
            <th>Status</th>
            <th>Execution Date</th>
            <th>Comments</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(test, index) in historyData" :key="index">
            <td>{{ test.testName }}</td>
            <td>
              <span :class="`badge bg-${test.status.toLowerCase()}`">{{ test.status }}</span>
            </td>
            <td>{{ test.executionDate }}</td>
            <td>{{ test.comments || 'N/A' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  import { defineProps } from 'vue';
  
  const props = defineProps({
    historyData: {
      type: Array,
      required: true
    }
  });
  </script>
  
  <style scoped>
  .test-history-table {
    margin-top: 20px;
  }
  
  .table th {
    text-align: center;
  }
  
  .badge {
    padding: 5px 10px;
    font-size: 0.875rem;
  }
  </style>
  