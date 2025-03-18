<template>
  <div>
    <div v-if="testExecutions.length === 0" class="no-tests">
      <p>No test cases assigned to you yet. </p>
    </div>

    <table v-else class="table custom-table shadow-sm">
      <thead>
        <tr>
          <th>Test Case</th>
          <th>Functionality</th>
          <th>Assigned By</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="execution in testExecutions" :key="execution.id">
          <td>{{ execution.test_case.title }}</td>
          <td>{{ execution.test_case.functionality?.name || 'N/A' }}</td>
          <td>{{ execution.assigned_by?.name || 'N/A' }}</td>
          <td>
            <span :class="statusClass(execution.status)">
              {{ execution.status || "Pending" }}
            </span>
          </td>
          <td>
            <button class="btn btn-primary btn-sm" @click="$emit('execute', execution)">
              🚀 Execute
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    testExecutions: Array
  },
  methods: {
    statusClass(status) {
      return {
        "badge bg-success": status === "Passed",
        "badge bg-danger": status === "Failed",
        "badge bg-warning": !status,
      };
    },
  },
};
</script>

<style scoped>
.custom-table {
  background: #ffffff;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #ccc;
}

.custom-table thead {
  background: #004085;
  color: white;
}

.custom-table tbody tr:hover {
  background: #f1f1f1;
}

.no-tests {
  text-align: center;
  font-size: 18px;
  padding: 20px;
  color: #555;
  background: #e9ecef;
  border-radius: 8px;
  margin-top: 20px;
}

.badge {
  padding: 5px 10px;
  font-size: 14px;
}
</style>
