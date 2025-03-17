<template>
    <div class="card">
      <div class="card-header fw-bold">📋 Test Result</div>
      <div class="card-body">
        <form @submit.prevent="submit">
          <!-- Result Selection -->
          <div class="mb-3">
            <label class="form-label">Test Outcome</label>
            <select v-model="result.status" class="form-control" required>
              <option value="Pass">Pass</option>
              <option value="Fail">Fail</option>
              <option value="Blocked">Blocked</option>
            </select>
          </div>
  
          <!-- Notes -->
          <div class="mb-3">
            <label class="form-label">Notes</label>
            <textarea v-model="result.notes" class="form-control" rows="3" placeholder="Add any relevant details"></textarea>
          </div>
  
          <!-- Submit Button -->
          <button type="submit" class="btn btn-success">
            <i class="bi bi-check-circle"></i> Submit Result
          </button>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const emit = defineEmits(['submitResult']);
  
  const result = ref({
    status: 'Pass',
    notes: ''
  });
  
  const submit = () => {
    emit('submitResult', result.value);
  };
  </script>
  
  <style scoped>
  .card {
    margin-top: 20px;
  }
  </style>
  