<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3 class="modal-title">Test Steps for {{ testCase?.title }}</h3>

      <table class="table">
        <thead>
          <tr>
            <th>Step Number</th>
            <th>Description</th>
            <th>Expected Result</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="step in testCase.steps" :key="step.id">
            <td>{{ step.step_number }}</td>
            <td>{{ step.description }}</td>
            <td>{{ step.expected_result }}</td>
            <td>
              <button @click="openEditStepModal(step)" class="btn btn-warning btn-sm">Edit</button>
              <button @click="deleteStep(step.id)" class="btn btn-danger btn-sm">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>

      <button @click="openAddStepModal" class="btn btn-primary">+ Add Step</button>
      <button @click="$emit('close')" class="btn btn-secondary">Close</button>

      <!-- Add/Edit Test Step Modal -->
      <AddTestStepModal
        v-if="showStepModal"
        :testCaseId="testCase.id"
        :stepToEdit="stepToEdit"
        @close="closeStepModal"
        @saved="fetchTestSteps"
        @error="handleError"
      />
    </div>
  </div>
</template>

<script>
import axios from "@/utils/axios";
import AddTestStepModal from "@/components/AddStepModal.vue";

export default {
  components: {
    AddTestStepModal
  },
  props: {
    testCase: Object
  },
  data() {
    return {
      showStepModal: false,
      stepToEdit: null
    };
  },
  methods: {
    openAddStepModal() {
      this.stepToEdit = null;
      this.showStepModal = true;
    },
    openEditStepModal(step) {
      this.stepToEdit = { ...step };
      this.showStepModal = true;
    },
    closeStepModal() {
      this.showStepModal = false;
    },
    async fetchTestSteps() {
      if (!this.testCase?.id) return;
      try {
        // Fetch the test case with its steps
        const response = await axios.get(`/api/test-cases/${this.testCase.id}/`);
        // Update the testCase prop with the fetched data
        this.$emit("update:testCase", response.data);
      } catch (error) {
        console.error("Error fetching test steps:", error);
        this.$emit("error", error); // Emit error event for handling in parent
      }
    },
    async deleteStep(stepId) {
      try {
        await axios.delete(`/api/test-steps/${stepId}/`);
        this.fetchTestSteps(); // Refresh the list of steps after deletion
      } catch (error) {
        console.error("Error deleting test step:", error);
        this.$emit("error", error); // Emit error event for handling in parent
      }
    },
    handleError(error) {
      console.error("Error in AddTestStepModal:", error);
      this.$emit("error", error); // Emit error event for handling in parent
    }
  },
  mounted() {
    this.fetchTestSteps(); // Fetch steps when the modal is opened
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 500px;
}

.table {
  margin-top: 20px;
}

button {
  margin-right: 10px;
}
</style>
