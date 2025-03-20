<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3" v-if="!showForm">
      <h3>Systems</h3>
      <button @click="showModal = true" class="btn btn-primary">+ Add System</button>
    </div>

    <SystemModal
      v-if="showModal"
      :system="selectedSystem"
      :organizations="organizations"
      @closeModal="closeModal"
      @saveSystem="saveSystem"
    />

    <div v-if="showForm" class="card p-4 mb-4 form-container">
      <h4 class="mb-3">{{ selectedSystem ? 'Edit System' : 'Create New System' }}</h4>
      <form @submit.prevent="selectedSystem ? updateSystem() : createSystem(form)">
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
          <button type="submit" class="btn btn-success me-2">{{ selectedSystem ? 'Update' : 'Create' }}</button>
          <button type="button" class="btn btn-outline-secondary" @click="showForm = false">Cancel</button>
        </div>
      </form>
    </div>

    <table v-if="!showForm" class="table table-striped systems-table">
      <thead class="table-dark">
        <tr>
          <th>Name</th>
          <th>Organization</th>
          <th>Description</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="system in systemsWithOrganization" :key="system.id">
          <td>{{ system.name }}</td>
          <td>{{ system.organizationName }}</td>
          <td>{{ system.description }}</td>
          <td>
            <button @click="$emit('view', system)" class="btn btn-info btn-sm">View</button>
            <button @click="editSystem(system)" class="btn btn-warning btn-sm">Edit</button>
            <button @click="$emit('delete', system.id)" class="btn btn-danger btn-sm">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import SystemModal from './SystemModal.vue';
import axios from 'axios';

export default {
  components: { SystemModal },
  props: {
    systems: Array,
    organizations: Array,
  },
  data() {
    return {
      showModal: false,
      showForm: false,
      selectedSystem: null,
      form: { name: '', organization: '', description: '' },
    };
  },
  computed: {
    systemsWithOrganization() {
      return this.systems.map((system) => {
        console.log('System:', system); // Debugging
        const organization = this.organizations.find((org) => org.id === system.organization);
        return {
          ...system,
          organizationName: organization ? organization.name : 'N/A',
        };
      });
    },
  },
  methods: {
    openSystemForm() {
      this.showModal = false;
      this.showForm = true;
    },
    editSystem(system) {
      this.selectedSystem = system;
      this.form = { ...system };
      this.showForm = true;
    },
    async createSystem(data) {
      try {
        console.log('Data being sent in createSystem:', data);
        await axios.post('/systems/', data);
        this.$emit('refreshSystems');
      } catch (error) {
        console.error('Error creating system:', error);
      }
    },
    async updateSystem() {
      try {
        const response = await axios.put(`/systems/${this.selectedSystem.id}/`, this.form);
        console.log('Update Response:', response.data); // Debugging
        this.showForm = false;
        this.$emit('refreshSystems');
      } catch (error) {
        console.error('Error updating system:', error);
      }
    },
    closeModal() {
      this.showModal = false;
      this.selectedSystem = null;
    },
    saveSystem(formData) {
      if (this.selectedSystem) {
        this.updateSystem();
      } else {
        this.createSystem(formData); // pass form data to createSystem
      }
    },
  },
};
</script>

<style scoped>
.form-container {
  max-width: 600px;
  margin: 0 auto;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}

.systems-table {
  width: 100%;
}

.systems-table th,
.systems-table td {
  padding: 10px;
  text-align: left;
}

.systems-table th {
  background-color: #343a40;
  color: white;
}

.systems-table tbody tr:nth-child(even) {
  background-color: #f2f2f2;
}

.systems-table .btn-sm {
  padding: 5px 10px;
  font-size: 0.8rem;
}
</style>