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
      const response = await this.$axios.get('/api/tester/assigned-tests/');
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
  background: white;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #333;
  font-size: 24px;
  font-weight: bold;
}

.no-tests-container {
  text-align: center;
  margin-top: 50px;
}

.no-tests-image {
  width: 200px;
  opacity: 0.8;
}

.no-tests-message {
  font-size: 18px;
  color: #777;
  margin-top: 10px;
}
</style>
