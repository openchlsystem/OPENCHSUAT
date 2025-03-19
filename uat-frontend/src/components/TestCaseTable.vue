<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h3>Test Cases</h3>
      <button @click="$emit('openModal')" class="btn btn-primary">+ Add Test Case</button>
    </div>

    <table class="table table-striped">
      <thead class="table-dark">
        <tr>
          <th>Title</th>
          <th>Functionality</th>
          <th>Expected Result</th>
          <th>Created By</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="testCase in testCases" :key="testCase.id">
          <td>{{ testCase.title }}</td>
          <td>{{ testCase.functionality?.name || 'N/A' }}</td>
          <td>{{ testCase.expected_result }}</td>
          <td>{{ testCase.created_by?.name || 'N/A' }}</td>
          <td>
            <button 
              :class="['btn', testCase.assigned_user ? 'btn-success' : 'btn-secondary']"
              @click="$emit('assign', testCase)"
            >
              {{ testCase.assigned_user ? "Assigned" : "Not Assigned" }}
            </button>
          </td>
          <td>
            <button @click="$emit('edit', testCase)" class="btn btn-warning btn-sm">Edit</button>
            <button @click="$emit('delete', testCase.id)" class="btn btn-danger btn-sm">Delete</button>
            <button @click="$emit('viewSteps', testCase)" class="btn btn-info btn-sm">View Steps</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    testCases: Array
  }
};
</script>
