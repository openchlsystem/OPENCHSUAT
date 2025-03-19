<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3" v-if="!showForm">
      <h3>Systems</h3>
      <button @click="showModal = true" class="btn btn-primary">+ Add System</button>
    </div>

    <!-- Modal (Only when showModal is true) -->
    <SystemModal 
      v-if="showModal" 
      @closeModal="showModal = false" 
      @openSystemForm="openSystemForm" 
    />

    <!-- System Form (Only when showForm is true) -->
    <div v-if="showForm" class="card p-4 mb-4 form-container">
      <h4 class="mb-3">Create New System</h4>
      <form @submit.prevent="createSystem">
        <div class="mb-3">
          <label class="form-label">System Name</label>
          <input v-model="form.name" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Organization</label>
          <select v-model="form.organization" class="form-control" required>
            <option v-for="org in organizations" :key="org.id" :value="org.id">
              {{ org.name }}
            </option>
          </select>
        </div>

        <div class="mb-3">
          <label class="form-label">Description</label>
          <textarea v-model="form.description" class="form-control" required></textarea>
        </div>

        <div class="d-flex justify-content-end">
          <button type="submit" class="btn btn-success me-2">Create</button>
          <button type="button" class="btn btn-outline-secondary" @click="showForm = false">Cancel</button>
        </div>
      </form>
    </div>

    <!-- Table (Hidden when form is shown) -->
    <table v-if="!showForm" class="table table-striped">
      <thead class="table-dark">
        <tr>
          <th>Name</th>
          <th>Organization</th>
          <th>Description</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="system in systems" :key="system.id">
          <td>{{ system.name }}</td>
          <td>{{ system.organization.name }}</td>
          <td>{{ system.description }}</td>
          <td>
            <button @click="$emit('view', system)" class="btn btn-info btn-sm">View</button>
            <button @click="$emit('edit', system)" class="btn btn-warning btn-sm">Edit</button>
            <button @click="$emit('delete', system.id)" class="btn btn-danger btn-sm">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import SystemModal from './SystemModal.vue';

export default {
  components: { SystemModal },
  props: {
    systems: Array,
    organizations: Array
  },
  data() {
    return {
      showModal: false,
      showForm: false,
      form: { name: '', organization: '', description: '' }
    };
  },
  methods: {
    openSystemForm() {
      this.showModal = false; // Close modal
      this.showForm = true;   // Show form
    },
    async createSystem() {
      await this.$axios.post('/api/systems/', this.form);
      this.showForm = false;
      this.$emit('refreshSystems');
    }
  }
}
</script>

<style scoped>
.form-container {
  max-width: 600px;
  margin: 0 auto;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}
</style>
