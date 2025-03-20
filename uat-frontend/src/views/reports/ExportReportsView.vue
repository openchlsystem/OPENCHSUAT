<!-- src/views/reports/ExportReports.vue -->
<template>
  <div class="report-view">
    <div class="container">
      <h2 class="fw-bold mb-4">Export Reports</h2>

      <ExportFilter @filterChanged="onFilterChanged" />

      <div class="mt-4">
        <button @click="exportReport('csv')" class="btn btn-primary me-2">
          Export as CSV
        </button>
        <button @click="exportReport('pdf')" class="btn btn-success">
          Export as PDF
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import ExportFilter from '@/components/reports/ExportFilter.vue';
import axios from 'axios';

const filterParams = ref({
  reportType: 'testCaseProgress',
  dateRange: null,
});

const onFilterChanged = (newFilterParams) => {
  filterParams.value = newFilterParams;
};

const exportReport = async (format) => {
  try {
    const response = await axios.post('/api/export-report', {
      format,
      filterParams: filterParams.value,
    });
    if (response.status === 200) {
      window.location.href = response.data.downloadUrl;
    }
  } catch (error) {
    console.error('Error exporting report:', error);
  }
};
</script>

<style scoped>
.report-view {
  padding: 24px;
}

.btn {
  padding: 10px 20px;
}
</style>
