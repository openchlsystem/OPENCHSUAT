<template>
    <div class="test-history-view">
      <div class="container">
        <h2 class="fw-bold mb-4">Test History</h2>
  
        <!-- Test History Table Component -->
        <TestHistoryTable :historyData="testHistory" />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import TestHistoryTable from '@/components/TestHistoryTable.vue';
  import axios from 'axios';
  
  const testHistory = ref([]);
  
  // Fetch the test history data when the component is mounted
  onMounted(async () => {
    try {
      const response = await axios.get('/api/test-history');  // Axios call to the backend
      testHistory.value = response.data;  // Store the data fetched from the backend
    } catch (error) {
      console.error('Error fetching test history:', error);
    }
  });
  </script>
  
  <style scoped>
  .test-history-view {
    padding: 20px;
  }
  </style>
  