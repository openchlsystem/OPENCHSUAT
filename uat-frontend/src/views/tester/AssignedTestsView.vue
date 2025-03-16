<template>
    <div class="assigned-tests-view">
      <div class="container">
        <!-- Header -->
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2 class="fw-bold">Assigned Tests</h2>
          <button class="btn btn-primary" @click="fetchAssignedTests">
            <i class="bi bi-arrow-clockwise"></i> Refresh
          </button>
        </div>
  
        <!-- Assigned Test Table -->
        <AssignedTestTable
          :tests="assignedTests"
          @view="viewTest"
        />
  
        <!-- Assigned Test Modal -->
        <AssignedTestModal 
          v-model:show="showModal"
          :testData="selectedTest"
          @close="closeModal"
        />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import AssignedTestTable from '@/components/AssignedTestTable.vue';
  import AssignedTestModal from '@/components/AssignedTestModal.vue';
  import axios from 'axios';
  
  const assignedTests = ref([]);
  const showModal = ref(false);
  const selectedTest = ref(null);
  
  const fetchAssignedTests = async () => {
    try {
      const response = await axios.get('/api/assigned-tests/');
      assignedTests.value = response.data;
    } catch (error) {
      console.error('Failed to fetch assigned tests:', error);
    }
  };
  
  const viewTest = (test) => {
    selectedTest.value = test;
    showModal.value = true;
  };
  
  const closeModal = () => {
    showModal.value = false;
  };
  
  onMounted(() => {
    fetchAssignedTests();
  });
  </script>
  
  <style scoped>
  .assigned-tests-view {
    padding: 20px;
  }
  </style>
  