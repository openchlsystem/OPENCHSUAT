<template>
    <div class="modal fade show d-block" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title text-primary">Report Details</h5>
            <button type="button" class="btn-close" @click="$emit('close')"></button>
          </div>
          <div class="modal-body">
            <p><strong>Test Case:</strong> {{ execution.test_case?.title || 'N/A' }}</p>
            <p><strong>Tester:</strong> {{ execution.tester?.first_name || 'N/A' }}</p>
            <p><strong>Status:</strong> <span :class="statusClass(execution.status)">{{ execution.status }}</span></p>
            <p><strong>Notes:</strong> {{ execution.notes || 'N/A' }}</p>
            <p><strong>Started:</strong> {{ formatDate(execution.started_at) }}</p>
            <p><strong>Completed:</strong> {{ formatDate(execution.completed_at) }}</p>
  
            <h6 class="mt-3">Test Steps:</h6>
            <ul>
              <li v-for="step in execution.test_case?.steps || []" :key="step.step_number">
                <strong>Step {{ step.step_number }}:</strong> {{ step.description }} — 
                <span :class="statusClass(step.status)">{{ step.status }}</span>
              </li>
            </ul>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="$emit('close')">Close</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps(['execution'])
  
  const statusClass = (status) => {
    switch ((status || '').toLowerCase()) {
      case 'pass':
      case 'passed': return 'text-success fw-bold'
      case 'fail':
      case 'failed': return 'text-danger fw-bold'
      case 'in_progress': return 'text-warning fw-bold'
      default: return 'text-secondary'
    }
  }
  
  const formatDate = (iso) => {
    return iso ? new Date(iso).toLocaleString() : 'N/A'
  }
  </script>
  
  <style scoped>
  .modal {
    background-color: rgba(0, 0, 0, 0.4);
  }
  .modal-content {
    border-radius: 10px;
  }
  </style>
  