<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3 class="modal-title text-center text-primary">Execute Test</h3>

      <form @submit.prevent="submit">
        <!-- Status Selection -->
        <div class="form-group">
          <label class="form-label">Execution Status</label>
          <select v-model="executionData.status" class="form-control" required>
            <option v-for="status in statusChoices" :key="status.value" :value="status.value">
              {{ status.label }}
            </option>
          </select>
        </div>

        <!-- Notes -->
        <div class="form-group">
          <label class="form-label">Execution Notes</label>
          <textarea
            v-model="executionData.notes"
            class="form-control"
            rows="3"
            placeholder="Add execution notes..."
            required
          ></textarea>
        </div>

        <!-- Steps Execution -->
        <div class="form-group" v-for="step in executionData.steps" :key="step.id">
          <label class="step-label">Step {{ step.step_number }}: {{ step.description }}</label>
          <select v-model="step.status" class="form-control" required>
            <option v-for="status in statusChoices" :key="status.value" :value="status.value">
              {{ status.label }}
            </option>
          </select>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-danger" @click="$emit('close')">Cancel</button>
          <button type="submit" class="btn btn-success">Submit</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from "@/store/auth.js"; // Import Pinia store
import axios from "@/utils/axios"; // Import axios for API calls
import { useToast } from 'vue-toastification';

const toast = useToast();
export default {
  props: ["execution"],
  data() {
    return {
      executionData: {
        status: "in_progress", // Default status
        notes: "",
        completed_at: new Date().toISOString(),
        test_case: this.execution.id,
        tester: this.execution.assigned_user || null, // Use assigned_user from the prop
        steps: this.execution.steps.map((step) => ({
          id: step.id,
          step_number: step.step_number,
          description: step.description,
          status: "", // User will select status
        })),
      },
      statusChoices: [], // To store status options fetched from the backend
    };
  },
  async mounted() {
    // Fetch status choices from the backend
    try {
      const response = await axios.get("/status-choices/"); // Replace with your actual endpoint
      this.statusChoices = response.data; // Assuming the response is in the format [{ value: "in_progress", label: "In Progress" }, ...]
    } catch (error) {
      console.error("Error fetching status choices:", error);
    }
  },
  methods: {
    async submit() {
      if (!this.executionData.tester) {
        toast.error("Tester ID not found. Please log in again.");
        return;
      }

      // Validate that all steps have a status
      const hasEmptyStepStatus = this.executionData.steps.some((step) => !step.status);
      if (hasEmptyStepStatus) {
        toast.warning("Please select a status for all steps.");
        return;
      }

      try {
        // Prepare the payload for the backend
        const payload = {
          status: this.executionData.status,
          notes: this.executionData.notes,
          completed_at: this.executionData.completed_at,
          test_case: this.executionData.test_case,
          tester: this.executionData.tester,
          steps: this.executionData.steps.map((step) => ({
            id: step.id,
            status: step.status,
          })),
        };

        // Send the payload to the backend
        const response = await axios.post("/test-executions/", payload);

        // Notify the parent component of successful submission
        this.$emit("save", response.data);

        // Show a success message
        toast.success("Test execution submitted successfully!");

        // Close the modal
        this.$emit("close");
      } catch (error) {
        console.error("Error submitting test execution:", error);
        toast.error("Failed to submit test execution. Please try again.");
      }
    },
  },
};
</script>

<style scoped>
/* Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Modal Box */
.modal-content {
  background: #fff;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.2);
  width: 500px;
}

/* Title */
.modal-title {
  color: #007bff;
  margin-bottom: 15px;
}

/* Form Styling */
.form-group {
  margin-bottom: 15px;
}
.form-label {
  font-weight: bold;
  color: #333;
}
.step-label {
  font-weight: bold;
  color: #333;
}
.form-control {
  width: 100%;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ddd;
}

/* Buttons */
.modal-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}
.btn {
  padding: 10px 15px;
  border-radius: 5px;
  font-weight: bold;
}
.btn-danger {
  background: #dc3545;
  color: white;
}
.btn-success {
  background: #28a745;
  color: white;
}
</style>