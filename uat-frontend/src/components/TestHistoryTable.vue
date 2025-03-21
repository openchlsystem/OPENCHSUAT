<template>
  <div>
    <table v-if="executions.length > 0" class="table">
      <thead>
        <tr>
          <th @click="sortBy('test_case.name')">Test Case</th>
          <th @click="sortBy('execution_date')">Execution Date</th>
          <th @click="sortBy('status')">Status</th>
          <th>Comments</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="execution in sortedExecutions" :key="execution.id">
          <td>{{ execution.test_case.name }}</td>
          <td>{{ formatDate(execution.execution_date) }}</td>
          <td :class="statusClass(execution.status)">
            {{ execution.status }}
          </td>
          <td>{{ execution.notes || "No comments" }}</td>
        </tr>
      </tbody>
    </table>

    <p v-else class="no-data-message">🚫 No test executions found.</p>
  </div>
</template>

<script>
export default {
  props: { executions: Array, sortOrder: String },
  computed: {
    sortedExecutions() {
      return [...this.executions].sort((a, b) => {
        const dateA = new Date(a.execution_date);
        const dateB = new Date(b.execution_date);
        return this.sortOrder === "asc" ? dateA - dateB : dateB - dateA;
      });
    }
  },
  methods: {
    formatDate(date) {
      return new Date(date).toLocaleString();
    },
    statusClass(status) {
      return status === "passed" ? "status-pass" : "status-fail";
    }
  }
};
</script>

<style scoped>
/* Table */
.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

th {
  background: #007bff;
  color: white;
  padding: 10px;
  cursor: pointer;
}

td {
  padding: 8px;
  border-bottom: 1px solid #ddd;
}

th:hover {
  background: #0056b3;
}

.status-pass {
  color: green;
  font-weight: bold;
}

.status-fail {
  color: red;
  font-weight: bold;
}

/* No Data */
.no-data-message {
  text-align: center;
  color: #666;
  font-size: 16px;
  margin-top: 20px;
}
</style>
