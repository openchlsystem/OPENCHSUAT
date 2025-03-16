<template>
    <div class="test-execution-view">
      <div class="container">
        <h2 class="fw-bold mb-4">Test Execution</h2>
  
        <!-- Test Execution Table -->
        <TestExecutionTable
          :tests="assignedTests"
          @openExecutionModal="openExecutionModal"
        />
  
        <!-- Test Execution Modal -->
        <TestExecutionModal
          v-if="showModal"
          :test="selectedTest"
          @closeModal="closeExecutionModal"
          @updateStatus="updateTestStatus"
        />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import TestExecutionTable from '@/components/TestExecutionTable.vue';
  import TestExecutionModal from '@/components/TestExecutionModal.vue';
  
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
  
  const openExecutionModal = (test) => {
    selectedTest.value = test;
    showModal.value = true;
  };
  
  const closeExecutionModal = () => {
    showModal.value = false;
  };
  
  const updateTestStatus = async (testId, status) => {
    try {
      const response = await axios.patch(`/api/assigned-tests/${testId}/`, { status });
      // Update the status of the test in the local array
      const testIndex = assignedTests.value.findIndex(test => test.id === testId);
      if (testIndex !== -1) {
        assignedTests.value[testIndex].status = status;
      }
      closeExecutionModal();
    } catch (error) {
      console.error('Failed to update test status:', error);
    }
  };
  
  onMounted(() => {
    fetchAssignedTests();
  });
  </script>
  
  <style scoped>
  .test-execution-view {
    padding: 20px;
  }
  </style>
  