<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3 class="modal-title">Test Steps for {{ testCase?.title }}</h3>

<<<<<<< HEAD
      <!-- Add/Edit Step Form -->
      <div class="add-step-form">
        <input v-model="newStep.description" placeholder="Enter test step..." class="form-control" />
        <button v-if="isEditing" @click="updateStep" class="btn btn-warning">Update</button>
        <button v-else @click="addStep" class="btn btn-success">➕ Add Step</button>
      </div>

      <!-- Steps List -->
      <ul class="test-steps-list">
        <li v-for="(step, index) in testSteps" :key="step.id">
          <span><strong>Step {{ index + 1 }}:</strong> {{ step.description }}</span>
          <div class="step-actions">
            <button @click="editStep(index)" class="btn btn-info btn-sm">Edit</button>
            <button @click="removeStep(step.id, index)" class="btn btn-danger btn-sm">Delete</button>
          </div>
        </li>
      </ul>

      <!-- Modal Footer -->
      <div class="modal-footer">
        <button @click="saveSteps" class="btn btn-primary">Save Steps</button>
        <button @click="$emit('close')" class="btn btn-secondary">Close</button>
      </div>
=======
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
>>>>>>> 74a37cbf7005864b84cc234115ab5b249abeb296
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
<<<<<<< HEAD
      testSteps: [],
      newStep: { description: "" },
      isEditing: false,
      editingIndex: null
    };
  },
  methods: {
    // 🔹 Fetch Test Steps from API
=======
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
>>>>>>> 74a37cbf7005864b84cc234115ab5b249abeb296
    async fetchTestSteps() {
      if (!this.testCase?.id) return;
      try {
<<<<<<< HEAD
        const response = await axios.get(`/test-steps/?test_case=${this.testCase.id}`);
        this.testSteps = response.data; // Load steps
=======
        // Fetch the test case with its steps
        const response = await axios.get(`/api/test-cases/${this.testCase.id}/`);
        // Update the testCase prop with the fetched data
        this.$emit("update:testCase", response.data);
>>>>>>> 74a37cbf7005864b84cc234115ab5b249abeb296
      } catch (error) {
        console.error("Error fetching test steps:", error);
        this.$emit("error", error); // Emit error event for handling in parent
      }
    },
<<<<<<< HEAD

    // 🔹 Add New Step
    addStep() {
      if (this.newStep.description.trim()) {
        this.testSteps.push({ description: this.newStep.description });
        this.newStep.description = "";
      }
    },

    // 🔹 Edit Step
    editStep(index) {
      this.newStep.description = this.testSteps[index].description;
      this.isEditing = true;
      this.editingIndex = index;
    },

    // 🔹 Update Step
    updateStep() {
      if (this.editingIndex !== null) {
        this.testSteps[this.editingIndex].description = this.newStep.description;
        this.newStep.description = "";
        this.isEditing = false;
        this.editingIndex = null;
      }
    },

    // 🔹 Delete Step
    async removeStep(stepId, index) {
      if (stepId) {
        try {
          await axios.delete(`/test-steps/${stepId}/`);
        } catch (error) {
          console.error("Error deleting step:", error);
        }
      }
      this.testSteps.splice(index, 1);
    },

    // 🔹 Save Steps to API (PUT)
    async saveSteps() {
      if (!this.testCase?.id) return;

      try {
        await axios.put(`/test-steps/${this.testCase.id}/`, { steps: this.testSteps });
        this.$emit("close"); // Close modal after saving
      } catch (error) {
        console.error("Error saving test steps:", error);
      }
    }
  },

  watch: {
    testCase: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.fetchTestSteps(); // Load steps when modal opens
        }
      }
    }
=======
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
>>>>>>> 74a37cbf7005864b84cc234115ab5b249abeb296
  }
};
</script>

<style scoped>
<<<<<<< HEAD
/* Modal Overlay */
=======
>>>>>>> 74a37cbf7005864b84cc234115ab5b249abeb296
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
<<<<<<< HEAD
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

/* Modal Content */
.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  width: 450px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
}

/* Modal Title */
.modal-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 15px;
}

/* Add Step Form */
.add-step-form {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.form-control {
  flex: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* Test Steps List */
.test-steps-list {
  list-style: none;
  padding: 0;
  max-height: 200px;
  overflow-y: auto;
}

.test-steps-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px;
  background: #f8f9fa;
  border-radius: 5px;
  margin-bottom: 5px;
}

.step-actions {
  display: flex;
  gap: 5px;
}

/* Modal Footer */
.modal-footer {
  margin-top: 15px;
}
</style>
=======
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
>>>>>>> 74a37cbf7005864b84cc234115ab5b249abeb296
