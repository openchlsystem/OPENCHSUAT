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
          <td>{{ functionality.name }}</td>
          <td>{{ getSystemName(functionality.system) }}</td>
          <td>{{ functionality.description }}</td>
          <td>
            <div class="d-flex gap-2">
              <button @click="$emit('edit', functionality)" class="btn btn-warning btn-sm">Edit</button>
              <button @click="$emit('delete', functionality.id)" class="btn btn-danger btn-sm">Delete</button>
              <button @click="$emit('viewTestCases', functionality)" class="btn btn-primary btn-sm">Test Cases</button>
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
    functionalities: Array,
    systems: Array
  },
  methods: {
    getSystemName(systemId) {
      if (!systemId || !this.systems) return 'N/A';
      
      const system = this.systems.find(sys => sys.id === systemId);
      return system ? system.name : 'N/A';
    }
  }
};
</script>