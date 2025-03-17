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
            <button class="btn btn-sm btn-info" @click="$emit('view', test)">
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
  border-radius: 12px;
  overflow: hidden;
}

.table-light th {
  background-color: #0066cc; /* Blue */
  color: white;
}

.table td {
  background-color: #fff;
}

.text-success {
  color: #28a745; /* Green */
}

.text-warning {
  color: #ff8c00; /* Orange */
}

.btn-info {
  background-color: #0066cc; /* Blue */
  color: white;
  border-radius: 8px;
}

.btn-info:hover {
  background-color: #004c99; /* Darker Blue */
}
</style>
