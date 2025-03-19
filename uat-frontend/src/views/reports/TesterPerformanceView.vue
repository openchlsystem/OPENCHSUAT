<!-- src/views/reports/TesterPerformance.vue -->
<template>
  <div class="report-view">
    <div class="container">
      <h2 class="fw-bold mb-4">Tester Performance Report</h2>

      <div v-if="loading" class="text-center">
        <div class="spinner-border text-primary" role="status"></div>
        <p>Loading performance data...</p>
      </div>

      <div v-else class="row">
        <div class="col-md-4">
          <div class="card p-3 shadow">
            <h5 class="fw-bold">Performance Summary</h5>
            <ul class="list-group">
              <li class="list-group-item">🧪 Total Tests Executed: {{ performanceData.total_tests }}</li>
              <li class="list-group-item">✅ Success Rate: {{ performanceData.success_rate }}%</li>
              <li class="list-group-item">🐞 Defect Handling Rate: {{ performanceData.defect_handling_rate }}%</li>
            </ul>
          </div>
        </div>
        <div class="col-md-8">
          <TesterPerformanceTable :testers="testerList" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import TesterPerformanceTable from '@/components/reports/TesterPerformanceTable.vue';

const performanceData = ref({});
const testerList = ref([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const response = await axios.get('/api/reports/tester-performance');
    performanceData.value = response.data.summary;
    testerList.value = response.data.testers;
  } catch (error) {
    console.error('Error fetching performance data:', error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.report-view {
  padding: 24px;
}

.card {
  border-radius: 12px;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style>
