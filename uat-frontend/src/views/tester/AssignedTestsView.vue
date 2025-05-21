<template>
  <div class="assigned-tests-container">
    <h2>📋 Assigned Test Cases</h2>

    <div v-if="assignedTests.length === 0" class="no-tests-container">
      <img src="@/assets/data.png" alt="No Tests" class="no-tests-image" />
      <p class="no-tests-message">No test cases assigned to you yet.</p>
    </div>

    <AssignedTestTable v-if="assignedTests.length > 0" :testCases="assignedTests" />
  </div>
</template>

<script>
import AssignedTestTable from "@/components/tester/AssignedTestTable.vue";
import axiosInstance from "@/utils/axios.js";;

export default {
  name: "AssignedTestsView",
  components: { AssignedTestTable },
  data() {
    return {
      assignedTests: [],
    };
  },
  async created() {
    try {
      const response = await axiosInstance.get("uat/test-cases/");
      this.assignedTests = response.data;
    } catch (error) {
      console.error("Error fetching assigned tests:", error);
    }
  },
};
</script>
