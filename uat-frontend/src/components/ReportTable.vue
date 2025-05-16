// ReportTable.vue - Complete Updated File
<template>
  <div class="table-responsive">
    <table class="table table-bordered table-hover">
      <thead class="thead-light">
        <tr>
          <th>#</th>
          <th>Test Case</th>
          <th>Tester</th>
          <th>Status</th>
          <th>Started</th>
          <th>Completed</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(exec, i) in executions" :key="exec.id">
          <td>{{ i + 1 }}</td>
          <td>{{ getTestCaseTitle(exec) }}</td>
          <td>{{ exec.tester?.first_name || 'N/A' }}</td>
          <td>
            <span :class="statusClass(exec.status)">
              {{ formatStatus(exec.status) }}
            </span>
          </td>
          <td>{{ formatDate(exec.started_at) }}</td>
          <td>{{ formatDate(exec.completed_at) }}</td>
          <td>
            <button class="btn btn-sm btn-outline-primary" @click="$emit('view', exec)">
              View
            </button>
          </td>
        </tr>
        <tr v-if="executions.length === 0">
          <td colspan="7" class="text-center">No reports found.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps(['executions'])
defineEmits(['view'])

/**
 * Get test case title with fallback handling
 * Now that the backend is fixed, the first case should normally apply
 */
const getTestCaseTitle = (execution) => {
  // Normal case - test_case is a full object with title
  if (execution.test_case?.title) {
    return execution.test_case.title
  }
  
  // Fallback 1: If we only have an ID
  if (execution.test_case?.id) {
    return `Test Case ${execution.test_case.id}`
  }
  
  // Fallback 2: If test_case is just an ID number
  if (typeof execution.test_case === 'number') {
    return `Test Case ${execution.test_case}`
  }
  
  // Final fallback
  return `Test Case ${execution.id || 'Unknown'}`
}

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