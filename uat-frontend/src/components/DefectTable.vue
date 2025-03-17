<template>
    <div class="table-responsive">
      <table class="table table-bordered table-hover">
        <thead class="table-light">
          <tr>
            <th>#</th>
            <th>Title</th>
            <th>Description</th>
            <th>Severity</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(defect, index) in defects" :key="defect.id">
            <td>{{ index + 1 }}</td>
            <td>{{ defect.title }}</td>
            <td>{{ defect.description }}</td>
            <td>
              <span :class="`badge bg-${getSeverityClass(defect.severity)}`">
                {{ defect.severity }}
              </span>
            </td>
            <td>{{ defect.status }}</td>
            <td>
              <button 
                class="btn btn-sm btn-warning me-2" 
                @click="$emit('edit', defect)"
              >
                <i class="bi bi-pencil"></i> Edit
              </button>
              <button 
                class="btn btn-sm btn-danger" 
                @click="$emit('delete', defect.id)"
              >
                <i class="bi bi-trash"></i> Delete
              </button>
            </td>
          </tr>
          <tr v-if="!defects.length">
            <td colspan="6" class="text-center text-muted">
              No defects reported.
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  defineProps({
    defects: Array,
  });
  
  const getSeverityClass = (severity) => {
    switch (severity) {
      case 'Low': return 'success';
      case 'Medium': return 'warning';
      case 'High': return 'danger';
      default: return 'secondary';
    }
  };
  </script>
  
  <style scoped>
  .table {
    border-radius: 10px;
    overflow: hidden;
  }
  </style>
  