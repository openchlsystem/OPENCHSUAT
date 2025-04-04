<template>
  <div class="table-container">
    <table class="table table-hover table-striped">
      <thead>
        <tr>
          <th>#</th>
          <th>Test Case Title</th>
          <th>Priority</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(test, index) in testCases" :key="test.id">
          <td>{{ index + 1 }}</td>
          <td class="test-title">{{ test.title }}</td>
          <td>
            <span class="badge" :class="getPriorityClass(test.priority)">
              {{ test.priority }}
            </span>
          </td>
          <td>
            <span class="badge" :class="getStatusClass(test.status)">
              {{ test.status }}
            </span>
          </td>
          <td>
            <router-link :to="'/tester/assigned-tests/' + test.id">
  <button class="btn btn-primary btn-sm">
    <i class="fas fa-eye"></i> View
  </button>
</router-link>

          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    testCases: Array,
  },
  methods: {
    getPriorityClass(priority) {
      return {
        "badge-danger": priority === "High",
        "badge-warning": priority === "Medium",
        "badge-success": priority === "Low",
      };
    },
    getStatusClass(status) {
      return {
        "badge-success": status === "Passed",
        "badge-warning": status === "Pending",
        "badge-danger": status === "Failed",
      };
    },
  },
};
</script>

<style scoped>
.table-container {
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  background: white;
  padding: 15px;
}

.table thead {
  background-color: #0056b3;
  color: white;
}

.test-title {
  font-weight: 500;
}

.badge {
  padding: 6px 12px;
  font-size: 13px;
  border-radius: 12px;
}

.badge-danger {
  background-color: #dc3545;
  color: white;
}

.badge-warning {
  background-color: #ffc107;
  color: black;
}

.badge-success {
  background-color: #28a745;
  color: white;
}

.btn-primary {
  background-color: #007bff;
  border: none;
  padding: 6px 12px;
  font-size: 14px;
  border-radius: 6px;
  transition: 0.3s;
}

.btn-primary:hover {
  background-color: #0056b3;
}
</style>
