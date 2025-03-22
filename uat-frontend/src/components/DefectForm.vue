<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3 class="modal-title"> Report a Defect</h3>

      <form @submit.prevent="submit">
        <div class="form-group">
          <label>Defect Name <span class="required">*</span></label>
          <input type="text" v-model="defect.name" class="form-control" required />
        </div>

        <div class="form-group">
          <label>Defect Description <span class="required">*</span></label>
          <textarea v-model="defect.description" class="form-control" rows="3" required></textarea>
        </div>

        <div class="form-group">
          <label>Related Test Case <span class="required">*</span></label>
          <select v-model="defect.test_case_id" class="form-control" required>
            <option v-for="test in testCases" :key="test.id" :value="test.id">
              {{ test.title }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>Severity <span class="required">*</span></label>
          <select v-model="defect.severity" class="form-control custom-select" required>
            <option value="Critical"> Critical</option>
            <option value="High"> High</option>
            <option value="Medium"> Medium</option>
            <option value="Low"> Low</option>
          </select>
        </div>

        <div class="form-group">
          <label>Attach Evidence</label>
          <input type="file" @change="handleFileUpload" class="form-control file-input" />
        </div>

        <div class="form-buttons">
          <button type="submit" class="btn btn-orange">Submit</button>
          <button type="button" @click="$emit('close')" class="btn btn-secondary">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  props: { testCases: Array },
  data() {
    return {
      defect: {
        name: "",
        description: "",
        test_case_id: "",
        severity: "Medium",
        evidence: null
      }
    };
  },
  methods: {
    handleFileUpload(event) {
      this.defect.evidence = event.target.files[0];
    },
    submit() {
      const formData = new FormData();
      formData.append("name", this.defect.name);
      formData.append("description", this.defect.description);
      formData.append("test_case_id", this.defect.test_case_id);
      formData.append("severity", this.defect.severity);
      if (this.defect.evidence) {
        formData.append("evidence", this.defect.evidence);
      }
      this.$emit("submit", formData);
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
</style>
