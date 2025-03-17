<template>
  <div class="assigned-tests-view">
    <div class="container">
      <!-- Header -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="fw-bold text-primary">Assigned Tests</h2>
        <button class="btn btn-refresh" @click="fetchAssignedTests">
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
  background-color: #f9f9f9;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

h2 {
  font-size: 28px;
  color: #0066cc; /* Blue color */
}

.btn-refresh {
  background-color: #ff8c00; /* Orange */
  color: #fff;
  border-radius: 8px;
  padding: 10px 15px;
  border: none;
  font-weight: bold;
}

.btn-refresh:hover {
  background-color: #e07b00; /* Darker Orange */
}

table th {
  background-color: #0066cc; /* Blue */
  color: white;
}

table td {
  color: #333;
}

.text-primary {
  color: #0066cc;
}
</style>
