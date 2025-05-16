<!-- src/views/reports/TestCaseProgress.vue -->
<template>
  <div class="report-view">
    <div class="container">
      <h2 class="fw-bold mb-4">Test Case Progress</h2>

      <div v-if="loading" class="text-center">
        <div class="spinner-border text-primary" role="status"></div>
        <p>Loading progress data...</p>
      </div>

      <div v-else>
        <TestCaseProgressChart :progressData="progressData" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import TestCaseProgressChart from '@/components/reports/TestCaseProgressChart.vue';
import axios from 'axios';

const progressData = ref([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const response = await axios.get('/api/test-case-progress');
    progressData.value = response.data;
  } catch (error) {
    console.error('Error fetching progress data:', error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.report-view {
  padding: 24px;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style>
