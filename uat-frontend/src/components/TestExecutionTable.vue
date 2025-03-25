<template>
  <div class="table-responsive">
    <table class="table table-striped table-hover">
      <thead class="thead-dark">
        <tr>
          <th>#</th>
          <th>Test Case</th>
          <th>Functionality</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <!-- Loading State -->
        <tr v-if="loading">
          <td colspan="5" class="text-center">
            <div class="spinner-border text-primary" role="status">
              <span class="sr-only">Loading...</span>
            </div>
          </td>
        </tr>

        <!-- Empty State -->
        <tr v-else-if="testExecutions.length === 0">
          <td colspan="5" class="text-center">No test executions found.</td>
        </tr>

        <!-- Data Rows -->
        <tr v-for="(test, index) in testExecutions" :key="test.id">
          <td>{{ index + 1 }}</td>
          <td>{{ test.title }}</td>
          <td>{{ test.functionality }}</td>
          <td>
            <span :class="getStatusClass(test.status)">{{ test.status || "Pending" }}</span>
          </td>
          <td>
            <button class="btn btn-primary btn-sm" @click="$emit('execute', test)">Execute</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    testExecutions: {
      type: Array,
      default: () => [],
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    getStatusClass(status) {
      switch (status) {
        case "Passed":
          return "badge badge-success";
        case "Failed":
          return "badge badge-danger";
        case "In Progress":
          return "badge badge-warning";
        default:
          return "badge badge-secondary";
      }
    },
  },
};
</script>

<style scoped>
.table {
  width: 100%;
  border-collapse: collapse;
}

.badge {
  padding: 5px 10px;
  font-size: 14px;
  border-radius: 4px;
}

.badge-success {
  background-color: #28a745;
  color: white;
}

.badge-danger {
  background-color: #dc3545;
  color: white;
}

.badge-warning {
  background-color: #ffc107;
  color: black;
}

.badge-secondary {
  background-color: #6c757d;
  color: white;
}

.btn {
  font-size: 14px;
  padding: 5px 10px;
  border-radius: 4px;
}

.text-center {
  text-align: center;
}

.spinner-border {
  display: inline-block;
  width: 2rem;
  height: 2rem;
  vertical-align: text-bottom;
  border: 0.25em solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spinner-border 0.75s linear infinite;
}

@keyframes spinner-border {
  to {
    transform: rotate(360deg);
  }
}
</style>