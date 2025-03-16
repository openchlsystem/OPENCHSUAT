<template>
    <div class="table-responsive">
      <table class="table table-bordered table-hover">
        <thead class="table-light">
          <tr>
            <th>#</th>
            <th>Title</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(test, index) in tests" :key="test.id">
            <td>{{ index + 1 }}</td>
            <td>{{ test.title }}</td>
            <td>
              <span :class="{
                'text-warning': test.status === 'Pending',
                'text-primary': test.status === 'In Progress',
                'text-success': test.status === 'Completed'
              }">
                {{ test.status }}
              </span>
            </td>
            <td>
              <button class="btn btn-sm btn-primary" @click="$emit('openExecutionModal', test)">
                <i class="bi bi-play-circle"></i> Execute
              </button>
            </td>
          </tr>
          <tr v-if="!tests.length">
            <td colspan="4" class="text-center text-muted">No tests assigned.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  defineProps({
    tests: Array
  });
  </script>
  
  <style scoped>
  .table {
    border-radius: 10px;
    overflow: hidden;
  }
  </style>
  