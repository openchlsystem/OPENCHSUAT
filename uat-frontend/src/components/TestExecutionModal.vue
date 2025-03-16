<template>
  <div class="modal" tabindex="-1" style="display: block; background-color: rgba(0, 0, 0, 0.5);">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Test Execution - {{ test.title }}</h5>
          <button type="button" class="btn-close" @click="$emit('closeModal')"></button>
        </div>
        <div class="modal-body">
          <!-- Test Status Selection -->
          <div class="mb-3">
            <label for="status" class="form-label">Test Status</label>
            <select v-model="status" class="form-select">
              <option value="Pending">Pending</option>
              <option value="In Progress">In Progress</option>
              <option value="Completed">Completed</option>
            </select>
          </div>

          <!-- Test Execution Steps -->
          <div class="mb-3">
            <label for="steps" class="form-label">Test Steps</label>
            <div v-for="(step, index) in steps" :key="index" class="mb-2">
              <div class="d-flex justify-content-between">
                <span>Step {{ index + 1 }}: {{ step.name }}</span>
                <select v-model="step.status" class="form-select form-select-sm w-25">
                  <option value="Pending">Pending</option>
                  <option value="Pass">Pass</option>
                  <option value="Fail">Fail</option>
                  <option value="Blocked">Blocked</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Attach Supporting Evidence -->
          <div class="mb-3">
            <label for="evidence" class="form-label">Attach Supporting Evidence</label>
            <input type="file" id="evidence" class="form-control" @change="handleFileUpload" />
            <small v-if="fileName" class="text-muted">File Selected: {{ fileName }}</small>
          </div>

          <!-- Comments -->
          <div class="mb-3">
            <label for="comments" class="form-label">Comments</label>
            <textarea v-model="comments" class="form-control" rows="3"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('closeModal')">Close</button>
          <button type="button" class="btn btn-primary" @click="submitTestExecution">Submit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

defineProps({
  test: Object
});

const status = ref('Pending');
const comments = ref('');
const steps = ref([
  { name: 'Step 1', status: 'Pending' },
  { name: 'Step 2', status: 'Pending' },
  { name: 'Step 3', status: 'Pending' },
]); 
const fileName = ref('');

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    fileName.value = file.name;
  }
};

const submitTestExecution = () => {
  const testData = {
    status: status.value,
    comments: comments.value,
    steps: steps.value, // Include step statuses
    evidence: fileName.value // Handle file upload logic here (e.g., upload to backend)
  };
  $emit('updateStatus', test.id, testData);
};
</script>

<style scoped>
.modal-dialog {
  max-width: 600px;
  border-radius: 10px;
}

.modal-header {
  background-color: #007bff;
  color: white;
  font-weight: bold;
}

.modal-footer button {
  border-radius: 20px;
}

.form-select {
  border-radius: 10px;
}
</style>
