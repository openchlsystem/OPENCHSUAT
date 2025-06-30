<template>
  <div class="table-container">
    <table class="table table-hover table-striped">
      <thead>
        <tr>
          <th>#</th>
          <th>Test Case Title</th>
          <th>Functionality</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(test, index) in testCases" :key="test.id">
          <td>{{ index + 1 }}</td>
          <td class="test-title">{{ test.title }}</td>
          <td>{{ getFunctionalityName(test) }}</td>
          <td>
            <button 
              class="btn btn-primary btn-sm"
              @click="navigateToTestExecution(test.id)"
            >
              <i class="fas fa-eye"></i> View
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
    testCases: Array,
  },
  methods: {
    getFunctionalityName(test) {
      if (!test) return 'N/A';
      
      // Check for functionality property
      if (test.functionality) {
        if (typeof test.functionality === 'string') return test.functionality;
        if (typeof test.functionality === 'object' && test.functionality.name) {
          return test.functionality.name;
        }
      }
      
      // Check for description property
      if (test.description) return test.description;
      
      // Check for system property
      if (test.system) {
        if (typeof test.system === 'string') return test.system;
        if (typeof test.system === 'object' && test.system.name) {
          return test.system.name;
        }
      }
      
      return 'N/A';
    },
    
    navigateToTestExecution(testId) {
      // Navigate to test execution page with the test case ID as a query parameter
      this.$router.push({
        path: '/tester/test-execution',
        query: { highlight: testId }
      });
    }
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

.btn-primary {
  background-color: #007bff;
  border: none;
  padding: 6px 12px;
  font-size: 14px;
  border-radius: 6px;
  transition: 0.3s;
  cursor: pointer;
}

.btn-primary:hover {
  background-color: #0056b3;
}
</style>