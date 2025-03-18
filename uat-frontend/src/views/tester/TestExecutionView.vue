<template>
  <div class="container mt-4">
    <h2 class="mb-4 text-center">🧪 Test Execution</h2>

    <TestExecutionTable 
      :testExecutions="testExecutions"
      @execute="openExecutionModal"
    />

    <!-- Test Execution Modal -->
    <TestExecutionModal
      v-if="showModal"
      :execution="selectedExecution"
      @close="closeModal"
      @save="submitExecution"
    />
  </div>
</template>

<script>
import axios from "@/utils/axios";
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
        const response = await axios.get("/testexecutions/");
        this.testExecutions = response.data;
      } catch (error) {
        console.error("Error fetching test executions:", error);
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
        await axios.post(`/testexecutions/${executionId}/execute/`, { steps });
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
