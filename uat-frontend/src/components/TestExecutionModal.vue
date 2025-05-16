<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3 class="modal-title text-center text-success">Execute Test</h3>

      <form @submit.prevent="submit">
        <!-- Test Case Info -->
        <div class="test-info">
          <h4>{{ getTestCaseTitle(execution) }}</h4>
          <p><strong>Functionality:</strong> {{ getFunctionalityName(execution) }}</p>
        </div>
        
        <!-- Steps Execution -->
        <div class="steps-section" v-if="executionData.steps && executionData.steps.length > 0">
          <h4>Test Steps</h4>
          <div class="form-group" v-for="step in executionData.steps" :key="step.id">
            <label class="step-label">Step {{ step.step_number }}: {{ step.description }}</label>
            <div class="step-detail" v-if="step.expected_result">
              <em>Expected Result: {{ step.expected_result }}</em>
            </div>
            <select v-model="step.status" class="form-control" required>
              <option v-for="status in stepStatusChoices" :key="status.value" :value="status.value">
                {{ status.label }}
              </option>
            </select>
            <textarea
              v-model="step.notes"
              class="form-control mt-2"
              rows="2"
              placeholder="Step notes (optional)"
            ></textarea>
          </div>
        </div>
        
        <!-- No Steps Message -->
        <div v-else class="alert alert-info">
          No steps defined for this test case. Please evaluate the overall test.
        </div>

        <!-- Notes - Moved to the end -->
        <div class="form-group mt-4">
          <label class="form-label">Execution Notes</label>
          <textarea
            v-model="executionData.notes"
            class="form-control"
            rows="3"
            placeholder="Add execution notes..."
            required
          ></textarea>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-danger" @click="$emit('close')">Cancel</button>
          <button type="submit" class="btn btn-success">Submit Test Execution</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    execution: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      executionData: {
        status: "completed", // Changed from "executed" to "completed"
        notes: "",
        completed_at: new Date().toISOString(),
        test_case: this.execution?.id,
        steps: this.prepareSteps(),
      },
      stepStatusChoices: [
        { value: "passed", label: "Passed" },
        { value: "failed", label: "Failed" },
        { value: "skipped", label: "Skipped" }
      ]
    };
  },
  methods: {
    prepareSteps() {
      if (!this.execution) return [];
      
      // Handle case where steps might be directly on the execution
      let steps = [];
      
      if (Array.isArray(this.execution.steps)) {
        steps = this.execution.steps;
      } else if (this.execution.steps && typeof this.execution.steps === 'object') {
        steps = Object.values(this.execution.steps);
      }
      
      // Map steps to include status field if it doesn't exist
      return steps.map(step => ({
        ...step,
        status: step.status || "passed", // Default to passed
        notes: step.notes || "",
      }));
    },
    
    getTestCaseTitle(test) {
      if (!test) return 'Unknown Test';
      
      // Handle cases where test case might be a JSON string
      if (typeof test === 'string') {
        try {
          // Try to parse as JSON
          const parsed = JSON.parse(test);
          return parsed.name || parsed.title || 'Untitled Test';
        } catch (e) {
          // Check if we have JSON string with name
          const match = test.match(/"name"\s*:\s*"([^"]+)"/);
          if (match && match[1]) return match[1];
          
          // Otherwise, return the string itself if it's not too long
          return test.length > 30 ? test.substring(0, 30) + '...' : test;
        }
      }
      
      // Handle object cases
      if (typeof test === 'object' && test !== null) {
        if (test.title) {
          if (typeof test.title === 'string') return test.title;
          if (typeof test.title === 'object' && test.title.name) return test.title.name;
        }
        if (test.name) return test.name;
      }
      
      return 'Untitled Test';
    },
    
    getFunctionalityName(test) {
      if (!test) return 'N/A';
      
      // Handle string case
      if (typeof test === 'string') {
        try {
          // Try to parse as JSON
          const parsed = JSON.parse(test);
          return parsed.functionality || parsed.description || 'N/A';
        } catch (e) {
          // Check if we have JSON string with description
          const match = test.match(/"description"\s*:\s*"([^"]+)"/);
          if (match && match[1]) return match[1];
          return 'N/A';
        }
      }
      
      // Handle object cases
      if (typeof test === 'object' && test !== null) {
        if (test.functionality) {
          if (typeof test.functionality === 'string') return test.functionality;
          if (typeof test.functionality === 'object' && test.functionality.name) {
            return test.functionality.name;
          }
        }
        if (test.description) return test.description;
      }
      
      return 'N/A';
    },
    
    submit() {
      // Validate notes
      if (!this.executionData.notes || this.executionData.notes.trim() === '') {
        if (this.$toast) {
          this.$toast.error("Please add execution notes");
        } else {
          alert("Please add execution notes");
        }
        return;
      }

      // Check that all steps have a status
      const incompleteSteps = this.executionData.steps.filter(step => !step.status);
      if (incompleteSteps.length > 0) {
        if (this.$toast) {
          this.$toast.error("Please select a status for all steps");
        } else {
          alert("Please select a status for all steps");
        }
        return;
      }

      // Prepare steps data for submission
      const processedSteps = this.executionData.steps.map(step => ({
        id: step.id,
        step_number: step.step_number,
        status: step.status,
        notes: step.notes || ''
      }));

      // Calculate overall status based on step statuses
      let overallStatus = "completed";
      if (processedSteps.length > 0) {
        // If all steps passed, mark as passed
        if (processedSteps.every(step => step.status === 'passed')) {
          overallStatus = "passed";
        }
        // If any step failed, mark as failed
        else if (processedSteps.some(step => step.status === 'failed')) {
          overallStatus = "failed";
        }
      }

      // Log the execution data for debugging
      console.log("Submitting test execution:", {
        executionId: this.execution.id,
        steps: processedSteps,
        status: overallStatus,
        notes: this.executionData.notes
      });

      // Emit the save event with all the necessary data
      this.$emit("save", {
        executionId: this.execution.id,
        steps: processedSteps,
        status: overallStatus,
        notes: this.executionData.notes
      });
    }
  },
  mounted() {
    // Initialize data when component mounts
    this.executionData = {
      status: "completed", // Changed from "executed" to "completed"
      notes: "",
      completed_at: new Date().toISOString(),
      test_case: this.execution?.id,
      steps: this.prepareSteps()
    };

    // Log initial execution data
    console.log("Initial execution data:", this.executionData);
  },
  watch: {
    // Watch for changes to the execution prop
    execution: {
      handler(newVal) {
        if (newVal) {
          this.executionData.test_case = newVal.id;
          this.executionData.steps = this.prepareSteps();
          console.log("Updated execution data:", this.executionData);
        }
      },
      deep: true
    }
  }
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
  z-index: 1000;
}

/* Modal Box */
.modal-content {
  background: #fff;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.2);
  width: 600px;
  max-height: 80vh;
  overflow-y: auto;
}

/* Title */
.modal-title {
  color: #28a745; /* Changed from blue to green */
  margin-bottom: 15px;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
}

/* Test Info */
.test-info {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 20px;
}

.test-info h4 {
  margin-top: 0;
  color: #333;
}

/* Steps Section */
.steps-section {
  margin-top: 20px;
  border-top: 1px solid #eee;
  padding-top: 15px;
}

.steps-section h4 {
  margin-bottom: 15px;
  color: #555;
}

/* Form Styling */
.form-group {
  margin-bottom: 15px;
}

.form-label {
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 5px;
}

.step-label {
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 5px;
}

.step-detail {
  color: #666;
  font-size: 0.9em;
  margin-bottom: 8px;
}

.form-control {
  width: 100%;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.form-control:focus {
  border-color: #28a745;
  box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.25);
}

/* Alert */
.alert {
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 15px;
}

.alert-info {
  background-color: #d1f7dd;
  color: #0c5460;
  border: 1px solid #bee5eb;
}

/* Buttons */
.modal-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.btn {
  padding: 10px 15px;
  border-radius: 5px;
  font-weight: bold;
  cursor: pointer;
  border: none;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-danger:hover {
  background: #c82333;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-success:hover {
  background: #218838;
}

.text-success {
  color: #28a745 !important;
}

.mt-2 {
  margin-top: 0.5rem;
}

.mt-4 {
  margin-top: 1.5rem;
}
</style>