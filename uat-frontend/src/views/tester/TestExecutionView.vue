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

// Fetch the assigned tests from the backend
const fetchAssignedTests = async () => {
  try {
    const response = await axios.get('/api/assigned-tests/');
    assignedTests.value = response.data;
  } catch (error) {
    console.error('Failed to fetch assigned tests:', error);
  }
};

// Open the modal to execute a test
const openExecutionModal = (test) => {
  selectedTest.value = test;
  showModal.value = true;
};

// Close the modal
const closeExecutionModal = () => {
  showModal.value = false;
};

// Update the test status and submit the results
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
  background-color: #f8f9fa;
  border-radius: 10px;
}

h2 {
  font-family: 'Arial', sans-serif;
  font-size: 1.5rem;
  color: #333;
}

.table-responsive {
  background-color: #fff;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.table {
  border-radius: 10px;
  overflow: hidden;
}

.table th, .table td {
  padding: 1rem;
  text-align: center;
  vertical-align: middle;
}

.table th {
  background-color: #f1f1f1;
}

.table td span {
  font-weight: bold;
}

.table td .btn {
  margin: 5px;
  border-radius: 5px;
}

.btn-primary {
  background-color: #007bff;
  border: 1px solid #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-danger {
  background-color: #dc3545;
  border: 1px solid #dc3545;
}

.btn-danger:hover {
  background-color: #c82333;
}

.btn-warning {
  background-color: #ffc107;
  border: 1px solid #ffc107;
}

.btn-warning:hover {
  background-color: #e0a800;
}

/* Modal Styling */
.modal {
  display: block;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-dialog {
  max-width: 600px;
  margin: 0 auto;
  border-radius: 10px;
}

.modal-content {
  border-radius: 10px;
}

.modal-header {
  background-color: #343a40;
  color: #fff;
  padding: 15px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

.modal-body {
  padding: 20px;
}

.form-label {
  font-weight: bold;
  color: #333;
}

.form-control {
  margin-bottom: 15px;
}

.form-select, .form-control {
  border-radius: 8px;
}

.modal-footer {
  display: flex;
  justify-content: space-between;
  padding: 15px;
  background-color: #f8f9fa;
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
}
</style>
