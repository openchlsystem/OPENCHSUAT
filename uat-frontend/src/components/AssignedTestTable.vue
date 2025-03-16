<template>
    <div class="table-responsive">
      <table class="table table-bordered table-hover">
        <thead class="table-light">
          <tr>
            <th>#</th>
            <th>Title</th>
            <th>System</th>
            <th>Status</th>
            <th>Assigned Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(test, index) in tests" :key="test.id">
            <td>{{ index + 1 }}</td>
            <td>{{ test.title }}</td>
            <td>{{ test.system }}</td>
            <td>
              <span :class="test.status === 'Completed' ? 'text-success' : 'text-warning'">
                {{ test.status }}
              </span>
            </td>
            <td>{{ formatDate(test.assigned_date) }}</td>
            <td>
              <button class="btn btn-sm btn-primary" @click="$emit('view', test)">
                <i class="bi bi-eye"></i> View
              </button>
            </td>
          </tr>
          <tr v-if="!tests.length">
            <td colspan="6" class="text-center text-muted">No assigned tests available.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  defineProps({
    tests: Array
  });
  
  const formatDate = (date) => {
    return new Date(date).toLocaleDateString();
  };
  </script>
  
  <style scoped>
  .table {
    border-radius: 10px;
    overflow: hidden;
  }
  </style>
  