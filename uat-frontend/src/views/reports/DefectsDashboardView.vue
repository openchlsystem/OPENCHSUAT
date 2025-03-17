<!-- src/views/reports/DefectsDashboard.vue -->
<template>
  <div class="report-view">
    <div class="container">
      <h2 class="fw-bold mb-4">Defects Dashboard</h2>

      <div v-if="loading" class="text-center">
        <div class="spinner-border text-primary" role="status"></div>
        <p>Loading defects data...</p>
      </div>

      <div v-else>
        <DefectsTable :defectsData="defectsData" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import DefectsTable from '@/components/reports/DefectsTable.vue';
import axios from 'axios';

const defectsData = ref([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const response = await axios.get('/api/defects-dashboard');
    defectsData.value = response.data;
  } catch (error) {
    console.error('Error fetching defects data:', error);
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
