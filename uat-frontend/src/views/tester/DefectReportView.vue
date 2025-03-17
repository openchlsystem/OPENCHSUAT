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
import axios from 'axios';

const submitDefect = async (defectData) => {
  try {
    // API call to submit defect data
    const formData = new FormData();
    formData.append('title', defectData.title);
    formData.append('description', defectData.description);
    formData.append('severity', defectData.severity);
    formData.append('priority', defectData.priority);
    if (defectData.evidence) {
      formData.append('evidence', defectData.evidence);
    }

    const response = await axios.post('/api/defects/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    console.log("Defect Report Submitted:", response.data);
    // Optionally, show success message or redirect user
  } catch (error) {
    console.error("Failed to submit defect:", error);
    // Optionally, show error message
  }
};
</script>

<style scoped>
.defect-report-view {
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 10px;
}
</style>
