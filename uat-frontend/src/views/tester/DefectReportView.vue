<template>
    <div class="defect-report-view">
      <div class="container">
        <h2 class="fw-bold mb-4">Defect Report</h2>
  
        <!-- Defect Report Form Component -->
        <DefectReportForm @submit="submitDefect" />
  
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import DefectReportForm from '@/components/DefectReportForm.vue';
  
  const submitDefect = (defectData) => {
    // Handle the submitted defect data here (call the API to submit defect)
    console.log("Submitted Defect Data: ", defectData);
  };
  </script>
  
  <style scoped>
  .defect-report-view {
    padding: 20px;
  }
  </style>
  