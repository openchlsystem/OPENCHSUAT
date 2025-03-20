<template>
  <div class="test-case-table">
    <!-- Header -->
    <div class="table-header">
      <h3>📝 Test Cases</h3>
      <button @click="$emit('openModal')" class="btn btn-primary">+ Add Test Case</button>
    </div>

    <!-- Test Case Table -->
    <table class="table table-hover">
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
              class="btn status-btn"
              :class="testCase.assigned_user ? 'btn-success' : 'btn-secondary'"
              @click="$emit('assign', testCase)"
            >
              {{ testCase.assigned_user ? "Assigned" : "Not Assigned" }}
            </button>
          </td>
          <td>
            <div class="action-buttons">
              <button @click="$emit('edit', testCase)" class="btn btn-warning">✏️ Edit</button>
              <button @click="$emit('delete', testCase.id)" class="btn btn-danger">🗑 Delete</button>
              <button @click="$emit('viewSteps', testCase)" class="btn btn-info">📜 View Steps</button>
            </div>
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

<style scoped>
/* Table Container */
.test-case-table {
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Header Styling */
.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

/* Table Styling */
.table {
  border-radius: 8px;
  overflow: hidden;
}

/* Status Button */
.status-btn {
  width: 120px;
  font-weight: bold;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 8px;
}

.btn {
  font-size: 14px;
  padding: 6px 12px;
  border-radius: 5px;
}
</style>
