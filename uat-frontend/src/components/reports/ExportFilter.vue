<template>
    <div class="export-filter">
      <div class="form-group">
        <label for="reportType">Select Report Type</label>
        <select v-model="filters.reportType" class="form-control" id="reportType">
          <option value="testCaseProgress">Test Case Progress</option>
          <option value="defects">Defects</option>
          <option value="testerPerformance">Tester Performance</option>
        </select>
      </div>
  
      <div class="form-group mt-3">
        <label for="dateRange">Date Range</label>
        <input v-model="filters.dateRange" type="date" class="form-control" id="dateRange" />
      </div>
  
      <button @click="applyFilter" class="btn btn-info mt-3">Apply Filter</button>
    </div>
  </template>
  
  <script setup>
  import { ref, defineEmits } from 'vue';
  
  const emit = defineEmits();
  const filters = ref({
    reportType: 'testCaseProgress',
    dateRange: null,
  });
  
  // Emit the filter parameters when the filter is changed
  const applyFilter = () => {
    emit('filterChanged', filters.value);
  };
  </script>
  
  <style scoped>
  .export-filter {
    max-width: 500px;
    margin-bottom: 20px;
  }
  </style>
  