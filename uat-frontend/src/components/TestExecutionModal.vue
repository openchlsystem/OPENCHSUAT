<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3 class="modal-title text-center text-primary">Execute Test</h3>

      <form @submit.prevent="submit">
        <!-- Status Selection -->
        <div class="form-group">
          <label class="form-label">Execution Status</label>
          <select v-model="executionData.status" class="form-control">
            <option value="in_progress">In Progress</option>
            <option value="completed">Completed</option>
            <option value="failed">Failed</option>
          </select>
        </div>

        <!-- Notes -->
        <div class="form-group">
          <label class="form-label">Execution Notes</label>
          <textarea v-model="executionData.notes" class="form-control" rows="3" placeholder="Add execution notes..."></textarea>
        </div>

        <!-- Steps Execution -->
        <div class="form-group" v-for="step in executionData.steps" :key="step.id">
          <label class="step-label">Step {{ step.step_number }}: {{ step.description }}</label>
          <select v-model="step.status" class="form-control">
            <option value="passed">Passed</option>
            <option value="failed">Failed</option>
            <option value="blocked">Blocked</option>
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

export default {
  props: ["execution"],
  data() {
    return {
      executionData: {
        status: "in_progress",
        notes: "",
        completed_at: new Date().toISOString(),
        test_case: this.execution.id,
        tester: null, // Will be set from Pinia
        steps: this.execution.steps.map((step) => ({
          id: step.id,
          step_number: step.step_number,
          description: step.description,
          status: "", // User will select status
        })),
      },
    };
  },
  mounted() {
    const authStore = useAuthStore();
    this.executionData.tester = authStore.user?.id || null; // Get tester ID from Pinia store
  },
  methods: {
    submit() {
      if (!this.executionData.tester) {
        alert("Tester ID not found. Please log in again.");
        return;
      }
      this.$emit("save", this.executionData);
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
