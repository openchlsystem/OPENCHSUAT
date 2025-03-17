<template>
  <div class="test-history-table">
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Test Name</th>
          <th>Status</th>
          <th>Execution Date</th>
          <th>Comments</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(test, index) in historyData" :key="index">
          <td>{{ test.testName }}</td>
          <td>
            <span :class="`badge bg-${getStatusBadgeColor(test.status)}`">{{ test.status }}</span>
          </td>
          <td>{{ formatDate(test.executionDate) }}</td>
          <td>{{ test.comments || 'N/A' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  historyData: {
    type: Array,
    required: true
  }
});

// Get status badge color based on the test status
const getStatusBadgeColor = (status) => {
  switch (status.toLowerCase()) {
    case 'completed':
      return 'success'; // Green
    case 'failed':
      return 'danger';  // Red
    case 'in-progress':
      return 'warning'; // Yellow
    default:
      return 'secondary'; // Grey
  }
};

// Format date to a readable format
const formatDate = (date) => {
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Date(date).toLocaleDateString('en-US', options);
};
</script>

<style scoped>
.test-history-table {
  margin-top: 20px;
}

.table th {
  text-align: center;
}

.badge {
  padding: 5px 10px;
  font-size: 0.875rem;
}

.table td {
  text-align: center;
  vertical-align: middle;
}
</style>
