<template>
  <div class="assigned-tests-container">
    <h2>📋 Assigned Test Cases</h2>

    <!-- Show No Assigned Tests Message -->
    <div v-if="assignedTests.length === 0" class="no-tests-container">
      <img src="@/assets/data.png" alt="No Tests" class="no-tests-image" />
      <p class="no-tests-message">No test cases assigned to you yet.</p>
    </div>

    <!-- Assigned Test Cases Table -->
    <AssignedTestTable v-if="assignedTests.length > 0" :testCases="assignedTests" />
  </div>
</template>

<script>
import AssignedTestTable from '@/components/tester/AssignedTestTable.vue';
import axios from "@/utils/axios";

export default {
  name: 'AssignedTestsView',
  components: { AssignedTestTable },
  data() {
    return {
      assignedTests: [],
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
};
</script>

<style scoped>
.assigned-tests-container {
  padding: 20px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  max-width: 900px;
  margin: 30px auto;
  text-align: center;
}

h2 {
  color: #333;
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.no-tests-container {
  text-align: center;
  padding: 20px;
}

.no-tests-image {
  width: 180px;
  opacity: 0.7;
}

.no-tests-message {
  font-size: 18px;
  color: #555;
  margin-top: 10px;
}
</style>
