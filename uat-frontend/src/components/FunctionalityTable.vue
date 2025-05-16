<!-- Modified FunctionalityTable.vue to enhance navigation to test cases -->
<template>
  <div>
    <div style="margin-bottom: 20px;"></div>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <button @click="$emit('openModal')" class="btn btn-primary">+ Add Functionality</button>
    </div>
    <div style="margin-bottom: 20px;"></div>
    <table class="table table-striped">
      <thead class="table-dark">
        <tr>
          <th>Name</th>
          <th>System</th>
          <th>Description</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="functionality in functionalities" :key="functionality.id">
          <td>
            <a href="#" @click.prevent="navigateToTestCases(functionality)" class="functionality-name">
              {{ functionality.name }}
            </a>
          </td>
          <td>{{ getSystemName(functionality.system || functionality.system_id) }}</td>
          <td>{{ functionality.description }}</td>
          <td>
            <div class="d-flex gap-2">
              <button @click="$emit('edit', functionality)" class="btn btn-warning btn-sm">Edit</button>
              <button @click="$emit('delete', functionality.id)" class="btn btn-danger btn-sm">Delete</button>
              <button @click="navigateToTestCases(functionality)" class="btn btn-primary btn-sm">Test Cases</button>
            </div>
          </td>
        </tr>
        <tr v-if="functionalities.length === 0">
          <td colspan="4" class="text-center">No functionalities found.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script>
export default {
  props: {
    functionalities: Array,
    systems: Array
  },
  methods: {
    getSystemName(systemId) {
      if (!systemId || !this.systems) return 'N/A';
     
      // Handle if systemId is an object with an id property
      const id = typeof systemId === 'object' ? systemId.id : systemId;
     
      const system = this.systems.find(sys => sys.id === id);
      return system ? system.name : 'N/A';
    },

    // New method to navigate to test cases
    navigateToTestCases(functionality) {
      // Extract the ID and ensure it's defined
      const functionalityId = functionality.id;
      const functionalityName = functionality.name;
      
      if (functionalityId) {
        // Navigate to the test cases page with functionality filter
        window.location.href = `/admin/test-cases?functionality_id=${functionalityId}&functionality_name=${encodeURIComponent(functionalityName)}`;
      }
    }
  }
};
</script>

<style scoped>
.functionality-name {
  color: #007bff;
  font-weight: bold;
  text-decoration: none;
}

.functionality-name:hover {
  text-decoration: underline;
  cursor: pointer;
}
</style>