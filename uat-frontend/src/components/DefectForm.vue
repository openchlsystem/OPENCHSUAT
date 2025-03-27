<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3 class="modal-title">Report a Defect</h3>

      <form @submit.stop.prevent="submit">
        <!-- Defect Name -->
        <div class="form-group">
          <label>Defect Name <span class="required">*</span></label>
          <input type="text" v-model="defect.title" class="form-control" required />
        </div>

        <!-- Defect Description -->
        <div class="form-group">
          <label>Defect Description <span class="required">*</span></label>
          <textarea v-model="defect.description" class="form-control" rows="3" required></textarea>
        </div>

        <!-- Related Test Case -->
        <div class="form-group">
          <label>Related Test Case <span class="required">*</span></label>
          <select v-model="defect.execution" class="form-control" required>
            <option v-for="test in testCases" :key="test.id" :value="test.id">
              {{ test.title }}
            </option>
          </select>
        </div>

        <!-- Severity -->
        <div class="form-group">
          <label>Severity <span class="required">*</span></label>
          <select v-model="defect.severity" class="form-control" required>
            <option v-for="severity in defectOptions.severity_options" :key="severity.label" :value="severity.value">
              {{ severity.label }}
            </option>
          </select>
        </div>

        <!-- Attach Evidence -->
        <div class="form-group">
          <label>Attach Evidence</label>
          <input type="file" @change="handleFileUpload" class="form-control" />
        </div>

        <!-- Form Buttons -->
        <div class="form-buttons">
          <button type="submit" class="btn btn-orange">Submit</button>
          <button type="button" @click="$emit('close')" class="btn btn-secondary">Cancel</button>
        </div>

        <!-- Error Message -->
        <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  props: { 
    testCases: Array, 
    defectOptions: Array 
  },
  data() {
    return {
      defect: {
        title: "",
        description: "",
        execution: "",
        severity: "Medium",
        execution_id: "",
        reported_by_id: "",
        evidence: null
      },
      errorMessage: ""
    };
  },
  methods: {
    handleFileUpload(event) {
      this.defect.evidence = event.target.files[0];
    },
    async submit() {
      if (!this.defect.execution) {
        this.errorMessage = "Please select a related test case.";
        return;
      }

      this.errorMessage = "";

      const formData = new FormData();
      formData.append("title", this.defect.title);
      formData.append("description", this.defect.description);
      formData.append("execution_id", this.defect.execution);
      formData.append("severity", this.defect.severity);

      // formData.append("reported_by_id", testCases.assigned_user);
      const selectedTestCase = this.testCases.find(test => test.id === this.defect.execution);
      if (selectedTestCase && selectedTestCase.assigned_user) {
        console.log("{{reported_by_id}}")
        formData.append("reported_by_id", selectedTestCase.assigned_user);
      }


      if (this.defect.evidence) {
        formData.append("evidence", this.defect.evidence);
      }

      try {
        console.log("Submitting defect:", Object.fromEntries(formData));
        
        // Emit formData to parent
        this.$emit("submit", formData);
      } catch (error) {
        console.error("Error submitting defect:", error.response?.data || error);

        if (error.response?.data) {
          const errors = error.response.data;
          this.errorMessage = Object.values(errors).flat().join(" ");
        } else {
          this.errorMessage = "Failed to submit defect. Please check the required fields.";
        }
      }
    }
  }
};
</script>

<style scoped>
/* Modal Styling */
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
  padding: 25px;
  border-radius: 8px;
  width: 450px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.modal-title {
  color: #ff6600;
  text-align: center;
  margin-bottom: 15px;
}

/* Form Styling */
.form-group {
  margin-bottom: 15px;
}

label {
  font-weight: 600;
  display: block;
  margin-bottom: 5px;
}

.required {
  color: red;
}

input, textarea, select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 14px;
}

textarea {
  resize: vertical;
}

.file-input {
  border: none;
}

/* Buttons */
.form-buttons {
  display: flex;
  justify-content: space-between;
}

.btn {
  padding: 8px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  transition: 0.3s;
}

.btn-orange {
  background: #ff6600;
  color: white;
}

.btn-orange:hover {
  background: #e65c00;
}

.btn-secondary {
  background: black;
  color: white;
}

.btn-secondary:hover {
  background: #333;
}

/* Error Message */
.error-text {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}
</style>