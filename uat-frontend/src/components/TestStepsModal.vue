<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3 class="modal-title">Test Steps for {{ testCase?.title }}</h3>

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
    </div>
  </div>
</template>

<script>
import axios from "@/utils/axios";

export default {
  props: {
    testCase: Object
  },
  data() {
    return {
      testSteps: [],
      newStep: { description: "" },
      isEditing: false,
      editingIndex: null
    };
  },
  methods: {
    // 🔹 Fetch Test Steps from API
    async fetchTestSteps() {
      if (!this.testCase?.id) return;
      try {
        const response = await axios.get(`/test-steps/?test_case=${this.testCase.id}`);
        this.testSteps = response.data; // Load steps
      } catch (error) {
        console.error("Error fetching test steps:", error);
      }
    },

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
  }
};
</script>

<style scoped>
/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
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
