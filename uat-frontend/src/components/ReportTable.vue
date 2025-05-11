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
            <td>{{ exec.test_case?.title || 'N/A' }}</td>
            <td>{{ exec.tester?.first_name || 'N/A' }}</td>
            <td>
              <span :class="statusClass(exec.status)">
                {{ exec.status }}
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
  