<!-- TestStepsModal.vue - Updated with scrolling -->
<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h3 class="modal-title">Test Steps for {{ testCase?.title }}</h3>
        <button @click="$emit('close')" class="btn-close" aria-label="Close"></button>
      </div>
      
      <div class="modal-body">
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>Step Number</th>
                <th>Description</th>
                <th>Expected Result</th>
                <th>Attachment</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="step in testCase.steps" :key="step.id">
                <td>{{ step.step_number }}</td>
                <td>{{ step.description }}</td>
                <td>{{ step.expected_result }}</td>
                <td>
                  <a v-if="step.attachment" :href="step.attachment" target="_blank" class="attachment-link">
                    View Attachment
                  </a>
                  <span v-else>No Attachment</span>
                </td>
                <td>
                  <div class="d-flex gap-2">
                    <button @click="openEditStepModal(step)" class="btn btn-warning btn-sm">Edit</button>
                    <button @click="deleteStep(step.id)" class="btn btn-danger btn-sm">Delete</button>
                  </div>
                </td>
              </tr>
              <tr v-if="!testCase.steps || testCase.steps.length === 0">
                <td colspan="5" class="text-center">No steps found for this test case</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <div class="modal-footer">
        <button @click="openAddStepModal()" class="btn btn-success">Add Step</button>
        <button @click="$emit('close')" class="btn btn-secondary">Close</button>
      </div>
      
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
        const response = await axios.get(`/test-cases/${this.testCase.id}/`);
        // Update the testCase prop with the fetched data
        this.$emit("update:testCase", response.data);
      } catch (error) {
        console.error("Error fetching test steps:", error);
        this.$emit("error", error); // Emit error event for handling in parent
      }
    },
    async deleteStep(stepId) {
      if (confirm("Are you sure you want to delete this step?")) {
        try {
          await axios.delete(`/test-steps/${stepId}/`);
          this.fetchTestSteps(); // Refresh the list of steps after deletion
        } catch (error) {
          console.error("Error deleting test step:", error);
          this.$emit("error", error); // Emit error event for handling in parent
        }
      }
    },
    handleError(error) {
      console.error("Error in AddTestStepModal:", error);
      this.$emit("error", error); // Emit error event for handling in parent
    }
  },
  mounted() {
    this.fetchTestSteps(); // Fetch steps when the modal is opened
    
    // Prevent body scrolling when modal is open
    document.body.style.overflow = 'hidden';
  },
  beforeUnmount() {
    // Restore body scrolling when modal is closed
    document.body.style.overflow = 'auto';
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
  z-index: 1050;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 1000px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #dee2e6;
}

.modal-title {
  margin: 0;
  font-size: 1.25rem;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
  max-height: calc(90vh - 130px); /* Subtract header and footer height */
}

.modal-footer {
  padding: 15px 20px;
  border-top: 1px solid #dee2e6;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.table-responsive {
  overflow-x: auto;
}

.table {
  margin-bottom: 0;
}

.attachment-link {
  color: #007bff;
  text-decoration: none;
}

.attachment-link:hover {
  text-decoration: underline;
}

.gap-2 {
  gap: 0.5rem;
}

.btn-close {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1;
  color: #000;
  opacity: 0.5;
  cursor: pointer;
}

.btn-close:hover {
  opacity: 0.75;
}
</style>