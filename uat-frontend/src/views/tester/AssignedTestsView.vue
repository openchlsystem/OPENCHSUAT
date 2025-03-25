<template>
  <div class="assigned-tests-container">
    <h2>📋 Assigned Test Cases</h2>

    <!-- Show No Assigned Tests Message -->
    <div v-if="assignedTests.length === 0" class="no-tests-container">
      <img src="@/assets/data.png" alt="No Tests" class="no-tests-image" />
      <p class="no-tests-message">No test cases assigned to you yet.</p>
    </div>

    <!-- Assigned Test Cases Table -->
    <AssignedTestTable v-if="assignedTests.length > 0" 
      :testCases="assignedTests" 
      @openTestModal="fetchTestDetails"
    />

    <!-- Assigned Test Modal -->
    <AssignedTestModal 
      :show="isModalOpen" 
      :testData="selectedTest" 
      @close="isModalOpen = false"
    />
  </div>
</template>

<script>
import AssignedTestTable from '@/components/tester/AssignedTestTable.vue';
import AssignedTestModal from '@/components/tester/AssignedTestModal.vue';
import axios from "@/utils/axios.js";

export default {
  name: 'AssignedTestsView',
  components: { AssignedTestTable, AssignedTestModal },
  data() {
    return {
      assignedTests: [],
      selectedTest: null,
      isModalOpen: false,
    };
  },
  async created() {
    try {
      const response = await axios.get('/test-cases/');
      this.assignedTests = response.data;
    } catch (error) {
      console.error('Error fetching assigned tests:', error);
    }
  },
  methods: {
    async fetchTestDetails(test) {
      try {
        const response = await axios.get(`/test-cases/${test.id}`);
        this.selectedTest = response.data;
        this.isModalOpen = true;
      } catch (error) {
        console.error('Error fetching test details:', error);
      }
    }
  }
};
</script>
