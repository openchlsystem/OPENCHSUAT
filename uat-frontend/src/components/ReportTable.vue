<!-- In ReportTable.vue -->
<template>
  <div class="table-responsive">
    <table class="table table-striped table-hover">
      <thead class="bg-success text-white">
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
        <tr v-for="(execution, index) in executions" :key="execution.id">
          <td>{{ index + 1 }}</td>
          <td>{{ getTestCaseTitle(execution) }}</td>
          <td>{{ getTesterName(execution) }}</td>
          <td>
            <span :class="getStatusClass(execution.status)">
              {{ formatStatus(execution.status) }}
            </span>
          </td>
          <td>{{ formatDate(execution.started_at) }}</td>
          <td>{{ formatDate(execution.completed_at) }}</td>
          <td>
            <button 
              @click="$emit('view', execution)" 
              class="btn btn-primary btn-sm"
            >
              View
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: ['executions'],
  emits: ['view'],
  methods: {
    getTestCaseTitle(execution) {
      if (execution.test_case?.title) {
        return execution.test_case.title
      }
      
      if (execution.test_case_title) {
        return execution.test_case_title
      }
      
      return `Test Case ${execution.test_case?.id || execution.id || 'Unknown'}`
    },
    
    getTesterName(execution) {
      if (execution.tester?.first_name) {
        return execution.tester.first_name
      }
      
      if (execution.tester_name) {
        return execution.tester_name
      }
      
      return 'N/A'
    },
    
    getStatusClass(status) {
      const statusLower = (status || '').toLowerCase()
      switch (statusLower) {
        case 'passed': return 'badge bg-success'
        case 'failed': return 'badge bg-danger'
        case 'in_progress': return 'badge bg-warning'
        default: return 'badge bg-secondary'
      }
    },
    
    formatStatus(status) {
      if (!status) return 'N/A'
      return status.charAt(0).toUpperCase() + status.slice(1).replace('_', ' ')
    },
    
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      try {
        return new Date(dateString).toLocaleString()
      } catch (e) {
        return dateString
      }
    }
  }
}
</script>