<template>
  <div class="test-history-view">
    <div class="container">
      <h2 class="fw-bold mb-4">Test History</h2>
  
      <!-- Filter or Search Bar for Test History -->
      <div class="mb-4">
        <input 
          v-model="searchQuery" 
          type="text" 
          class="form-control" 
          placeholder="Search by test name..." 
        />
      </div>
  
      <!-- Test History Table Component -->
      <TestHistoryTable :historyData="filteredTestHistory" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import TestHistoryTable from '@/components/TestHistoryTable.vue';
import axios from 'axios';

const testHistory = ref([]);
const searchQuery = ref('');

// Fetch the test history data when the component is mounted
onMounted(async () => {
  try {
    const response = await axios.get('/api/test-history');  // Axios call to the backend
    testHistory.value = response.data;  // Store the data fetched from the backend
  } catch (error) {
    console.error('Error fetching test history:', error);
  }
});

// Filter the test history data based on search query
const filteredTestHistory = computed(() => {
  return testHistory.value.filter(test =>
    test.testName.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});
</script>

<style scoped>
.test-history-view {
  padding: 20px;
}

input.form-control {
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

h2 {
  color: #333;
}
</style>
