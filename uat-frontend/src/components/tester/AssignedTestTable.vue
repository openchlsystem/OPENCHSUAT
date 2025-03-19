<template>
  <table class="test-table">
    <thead>
      <tr>
        <th>#</th>
        <th>Title</th>
        <th>Functionality</th>
        <th>Status</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(test, index) in testCases" :key="test.id">
        <td>{{ index + 1 }}</td>
        <td>{{ test.title }}</td>
        <td>{{ test.functionality }}</td>
        <td>{{ test.status }}</td>
        <td>
          <button class="execute-btn" @click="executeTest(test.id)">Execute</button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'AssignedTestTable',
  props: {
    testCases: Array,
  },
  methods: {
    executeTest(testId) {
      this.$router.push({ name: 'TestExecutionView', params: { id: testId } });
    },
  },
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
