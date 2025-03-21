<template>
  <div class="container mt-4">
    <h2 class="mb-4 text-center text-primary">Test Execution</h2>

    <TestExecutionTable 
      :testExecutions="testExecutions"
      @execute="openExecutionModal"
    />

    <!-- Execution Modal -->
    <TestExecutionModal
      v-if="showModal"
      :execution="selectedExecution"
      @close="closeModal"
      @save="submitExecution"
    />
  </div>
</template>

<script>
import axios from "@/utils/axios.js";
import TestExecutionTable from "@/components/TestExecutionTable.vue";
import TestExecutionModal from "@/components/TestExecutionModal.vue";

export default {
  components: {
    TestExecutionTable,
    TestExecutionModal
  },
  data() {
    return {
      testExecutions: [],
      selectedExecution: null,
      showModal: false,
    };
  },
  methods: {
    async fetchTestExecutions() {
      try {
        const response = await axios.get("/test-cases/");
        this.testExecutions = response.data;
      } catch (error) {
        console.error("Error fetching test executions:", error.response?.data || error.message);
      }
    },
    openExecutionModal(execution) {
      this.selectedExecution = { ...execution };
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.fetchTestExecutions();
    },
    async submitExecution({ executionId, steps }) {
      try {
        await axios.post(`/test-executions/${executionId}/execute/`, { steps });
        this.closeModal();
      } catch (error) {
        console.error("Error submitting execution:", error);
      }
    },
  },
  mounted() {
    this.fetchTestExecutions();
  },
};
</script>

<style scoped>
.container {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}
h2 {
  color: #ff6600; /* Orange */
  font-weight: bold;
}
</style>
