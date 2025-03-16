<template>
    <div class="modal" tabindex="-1" style="display: block; background-color: rgba(0, 0, 0, 0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Test Execution - {{ test.title }}</h5>
            <button type="button" class="btn-close" @click="$emit('closeModal')"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label for="status" class="form-label">Test Status</label>
              <select v-model="status" class="form-select">
                <option value="Pending">Pending</option>
                <option value="In Progress">In Progress</option>
                <option value="Completed">Completed</option>
              </select>
            </div>
  
            <div class="mb-3">
              <label for="evidence" class="form-label">Attach Supporting Evidence</label>
              <input type="file" id="evidence" class="form-control" />
            </div>
  
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
  const evidence = ref(null);
  
  const submitTestExecution = () => {
    // Send the updated status, comments, and evidence to the backend API
    const testData = {
      status: status.value,
      comments: comments.value,
      evidence: evidence.value // Handle file upload logic here
    };
    // Call the backend API to update the test status
    $emit('updateStatus', test.id, status.value);
  };
  </script>
  
  <style scoped>
  .modal {
    display: block;
    background-color: rgba(0, 0, 0, 0.5);
  }
  </style>
  