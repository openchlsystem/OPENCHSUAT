<template>
  <div class="table-responsive">
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
            <span :class="getPriorityClass(test.priority)">{{ test.priority }}</span>
          </td>
          <td>
            <span :class="getStatusClass(test.status)">{{ test.status }}</span>
          </td>
          <td>
            <router-link :to="'/tester/test-case/' + test.id" class="btn btn-primary btn-sm">
              View
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
        'badge bg-danger': priority === 'High',
        'badge bg-warning': priority === 'Medium',
        'badge bg-success': priority === 'Low',
      };
    },
    getStatusClass(status) {
      return {
        'badge bg-success': status === 'Passed',
        'badge bg-warning text-dark': status === 'Pending',
        'badge bg-danger': status === 'Failed',
      };
    }
  }
};
</script>

<style scoped>
.table {
  margin-top: 10px;
}

th {
  background: #f8f9fa;
  text-align: center;
  font-weight: bold;
}

td {
  text-align: center;
  vertical-align: middle;
}

.test-title {
  font-weight: bold;
  color: #007bff;
}

.badge {
  padding: 8px 12px;
  font-size: 14px;
  border-radius: 5px;
}

.btn-sm {
  padding: 5px 12px;
  font-size: 14px;
  transition: 0.3s ease;
}

.btn-sm:hover {
  background: #0056b3;
}
</style>
