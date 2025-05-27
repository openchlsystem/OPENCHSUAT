// ReportModal.vue - Fixed Version
<template>
  <div class="modal fade show d-block" tabindex="-1" role="dialog">
    <div class="modal-dialog modal-lg" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title text-primary">Report Details</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>
        <div class="modal-body">
          <p><strong>Test Case:</strong> {{ getTestCaseTitle(execution) }}</p>
          <p><strong>Description:</strong> {{ getTestCaseDescription(execution) }}</p>
          <p><strong>Tester:</strong> {{ getTesterName(execution) }}</p>
          <p><strong>Status:</strong> <span :class="statusClass(execution.status)">{{ formatStatus(execution.status) }}</span></p>
          <p><strong>Notes:</strong> {{ execution.notes || 'N/A' }}</p>
          <p><strong>Started:</strong> {{ formatDate(execution.started_at) }}</p>
          <p><strong>Completed:</strong> {{ formatDate(execution.completed_at) }}</p>

          <h6 class="mt-4 mb-3">Test Steps:</h6>
          <div v-if="hasTestSteps" class="test-steps">
            <div v-for="step in getTestSteps(execution)" :key="step.id" class="test-step card mb-2">
              <div class="card-body p-3">
                <h6 class="step-number">Step {{ step.step_number }}</h6>
                <div class="step-description mb-1">{{ step.description }}</div>
                <div class="expected-result text-muted small">
                  <strong>Expected:</strong> {{ step.expected_result }}
                </div>
              </div>
            </div>
          </div>
          <p v-else class="text-muted">No test steps available for this test case.</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps(['execution'])
defineEmits(['close'])

/**
 * Get test case title with improved fallback handling
 */
const getTestCaseTitle = (execution) => {
  console.log('Getting test case title for:', execution); // Debug log
  
  // Try multiple data structures
  if (execution.test_case?.title) {
    return execution.test_case.title
  }
  
  if (execution.test_case_title) {
    return execution.test_case_title
  }
  
  if (execution.test_case_details?.title) {
    return execution.test_case_details.title
  }
  
  // Fallback to ID if available
  if (execution.test_case?.id) {
    return `Test Case ${execution.test_case.id}`
  }
  
  if (typeof execution.test_case === 'number') {
    return `Test Case ${execution.test_case}`
  }
  
  return `Test Case ${execution.id || 'Unknown'}`
}

/**
 * Get test case description with improved fallback
 */
const getTestCaseDescription = (execution) => {
  if (execution.test_case_details?.description) {
    return execution.test_case_details.description
  }
  
  if (execution.test_case_description) {
    return execution.test_case_description
  }
  
  if (execution.test_case?.description) {
    return execution.test_case.description
  }
  
  return 'No description available'
}

/**
 * Get tester name with fallback handling
 */
const getTesterName = (execution) => {
  if (execution.tester_name) {
    return execution.tester_name
  }
  
  if (execution.tester?.first_name) {
    return execution.tester.first_name
  }
  
  return 'N/A'
}

/**
 * Get test steps from multiple possible data structures
 */
const getTestSteps = (execution) => {
  if (execution.test_case_details?.steps) {
    return execution.test_case_details.steps
  }
  
  if (execution.test_case?.steps) {
    return execution.test_case.steps
  }
  
  return []
}

// Check if test steps exist
const hasTestSteps = computed(() => {
  const steps = getTestSteps(props.execution)
  return steps && steps.length > 0
})

/**
 * Get appropriate CSS class for status display
 */
const statusClass = (status) => {
  const statusLower = (status || '').toLowerCase()
  switch (statusLower) {
    case 'pass':
    case 'passed': 
      return 'text-success fw-bold'
    case 'fail':
    case 'failed': 
      return 'text-danger fw-bold'
    case 'in_progress': 
      return 'text-warning fw-bold'
    default: 
      return 'text-secondary'
  }
}

/**
 * Format status for display - convert to user-friendly text
 */
const formatStatus = (status) => {
  if (!status) return 'N/A'
  
  const statusLower = status.toLowerCase()
  
  // Special cases
  if (statusLower === 'in_progress') {
    return 'In Progress'
  }
  
  // Capitalize first letter of each word
  return status.split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ')
}

/**
 * Format date for display
 */
const formatDate = (iso) => {
  if (!iso) return 'N/A'
  
  try {
    const date = new Date(iso)
    return date.toLocaleString()
  } catch (e) {
    console.error('Error formatting date:', e)
    return iso // Return original value if parsing fails
  }
}
</script>

<style scoped>
.modal {
  background-color: rgba(0, 0, 0, 0.4);
}
.modal-content {
  border-radius: 10px;
}
.test-step {
  border-left: 4px solid #6c757d;
}
.step-number {
  font-weight: 600;
  color: #495057;
  margin-bottom: 0.5rem;
}
</style>