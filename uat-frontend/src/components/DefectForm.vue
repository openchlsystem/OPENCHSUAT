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
          <select v-model="defect.test_case_id" class="form-control" required>
            <option value="">-- Select a test case --</option>
            <option v-for="test in testCases" :key="test.id" :value="test.id">
              {{ test.title }}
            </option>
          </select>
        </div>

        <!-- Severity -->
        <div class="form-group">
          <label>Severity <span class="required">*</span></label>
          <select v-model="defect.severity" class="form-control" required>
            <option value="">-- Select severity --</option>
            <option v-for="severity in severityOptions" :key="severity.value" :value="severity.value">
              {{ severity.label }}
            </option>
          </select>
        </div>

        <!-- Attach Evidence -->
        <div class="form-group">
          <label>Attach Evidence</label>
          <input type="file" @change="handleFileUpload" class="form-control" />
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="alert alert-danger mt-3">
          {{ errorMessage }}
        </div>

        <!-- Form Buttons -->
        <div class="form-buttons mt-4">
          <button type="button" @click="$emit('close')" class="btn btn-secondary">Cancel</button>
          <button type="submit" class="btn btn-orange" :disabled="isSubmitting">
            <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-1" role="status"></span>
            Submit
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from '@/utils/axios';

export default {
  props: { 
    testCases: {
      type: Array,
      required: true
    },
    defectOptions: {
      type: Object,
      required: true
    }
  },
  
  data() {
    return {
      defect: {
        title: "",
        description: "",
        test_case_id: "",
        severity: "",
        attachment: null
      },
      errorMessage: "",
      isSubmitting: false
    };
  },
  
  computed: {
    severityOptions() {
      return this.defectOptions?.severity_options || [];
    }
  },
  
  methods: {
    handleFileUpload(event) {
      this.defect.attachment = event.target.files[0];
    },
    
    async submit() {
      if (!this.validate()) return;
      
      this.errorMessage = "";
      this.isSubmitting = true;
      
      try {
        const formData = new FormData();
        formData.append("title", this.defect.title);
        formData.append("description", this.defect.description);
        formData.append("test_case_id", this.defect.test_case_id);
        formData.append("severity", this.defect.severity);
        
        if (this.defect.attachment) {
          formData.append("attachment", this.defect.attachment);
        }
        
        // Log form data for debugging
        console.log("Submitting defect with data:");
        for (let [key, value] of formData.entries()) {
          console.log(`${key}: ${value}`);
        }
        
        // Send the request to the correct endpoint
        const response = await axios.post("uat/defects/", formData, {
          headers: { "Content-Type": "multipart/form-data" }
        });
        
        console.log("Defect created successfully:", response.data);
        
        // Emit success event to parent
        this.$emit("submit-success", response.data);
        
        // Close the modal
        this.$emit("close");
        
      } catch (error) {
        console.error("Error submitting defect:", error);
        
        // Set error message
        if (error.response && error.response.data) {
          // Extract error message from response
          const errorData = error.response.data;
          
          if (typeof errorData === 'object') {
            const errorMessages = [];
            
            // Format error messages for display
            Object.entries(errorData).forEach(([field, errors]) => {
              if (Array.isArray(errors)) {
                errors.forEach(error => errorMessages.push(`${field}: ${error}`));
              } else if (typeof errors === 'string') {
                errorMessages.push(`${field}: ${errors}`);
              }
            });
            
            if (errorMessages.length > 0) {
              this.errorMessage = errorMessages.join(', ');
            } else {
              this.errorMessage = "Failed to submit defect. Please check the form.";
            }
          } else {
            this.errorMessage = errorData.toString();
          }
        } else {
          this.errorMessage = error.message || "Failed to submit defect";
        }
      } finally {
        this.isSubmitting = false;
      }
    },
    
    validate() {
      if (!this.defect.title.trim()) {
        this.errorMessage = "Defect name is required.";
        return false;
      }
      
      if (!this.defect.description.trim()) {
        this.errorMessage = "Defect description is required.";
        return false;
      }
      
      if (!this.defect.test_case_id) {
        this.errorMessage = "Please select a test case.";
        return false;
      }
      
      if (!this.defect.severity) {
        this.errorMessage = "Please select a severity level.";
        return false;
      }
      
      return true;
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
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 25px;
  border-radius: 8px;
  width: 500px;
  max-width: 90vw;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.modal-title {
  color: #ff6600;
  text-align: center;
  margin-bottom: 20px;
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

/* Alert */
.alert {
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 15px;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

/* Buttons */
.form-buttons {
  display: flex;
  justify-content: space-between;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  transition: 0.3s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-orange {
  background: #ff6600;
  color: white;
}

.btn-orange:hover:not(:disabled) {
  background: #e65c00;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}

/* Spinner */
.spinner-border-sm {
  width: 1rem;
  height: 1rem;
  border-width: 0.15em;
}

.spinner-border {
  display: inline-block;
  vertical-align: text-bottom;
  border: 0.25em solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spinner-border 0.75s linear infinite;
}

@keyframes spinner-border {
  to {
    transform: rotate(360deg);
  }
}

.mt-3 {
  margin-top: 1rem;
}

.mt-4 {
  margin-top: 1.5rem;
}

.me-1 {
  margin-right: 0.25rem;
}
</style>