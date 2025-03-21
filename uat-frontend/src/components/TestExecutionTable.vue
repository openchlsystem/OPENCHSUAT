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
        <tr v-for="(test, index) in testExecutions" :key="test.id">
          <td>{{ index + 1 }}</td>
          <td>{{ test.title }}</td>
          <td>{{ test.functionality }}</td>
          <td>
            <span :class="getStatusClass(test.status)">{{ test.status || 'Pending' }}</span>
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
    testExecutions: Array,
  },
  methods: {
    getStatusClass(status) {
      if (status === "Passed") return "badge badge-success";
      if (status === "Failed") return "badge badge-danger";
      return "badge badge-secondary";
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
}

.btn {
  font-size: 14px;
}
</style>
