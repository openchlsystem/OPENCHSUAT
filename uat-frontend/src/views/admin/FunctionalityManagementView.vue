<template>
    <div class="container">
      <div class="d-flex justify-content-between align-items-center my-4">
        <h2 class="fw-bold">Functionality Management</h2>
        <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addFunctionalityModal">
          + Add Functionality
        </button>
      </div>
  
      <div v-if="functionalities.length" class="table-responsive">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>#</th>
              <th>Functionality</th>
              <th>System</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(functionality, index) in functionalities" :key="functionality.id">
              <td>{{ index + 1 }}</td>
              <td>{{ functionality.name }}</td>
              <td>{{ getSystemName(functionality.systemId) }}</td>
              <td>{{ functionality.description }}</td>
              <td>
                <button class="btn btn-sm btn-warning me-2" @click="editFunctionality(functionality)">
                  Edit
                </button>
                <button class="btn btn-sm btn-danger" @click="deleteFunctionality(functionality.id)">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="alert alert-info">No functionalities found.</div>
  
      <!-- Modal for adding/editing functionalities -->
      <FunctionalityModal
        id="addFunctionalityModal"
        :functionality="selectedFunctionality"
        :systems="systems"
        @add-functionality="addFunctionality"
        @update-functionality="updateFunctionality"
      />
    </div>
  </template>
  
  <script>
  import FunctionalityModal from '@/components/FunctionalityModal.vue';
  
  export default {
    components: { FunctionalityModal },
    data() {
      return {
        functionalities: [
          {
            id: 1,
            name: 'Login',
            systemId: 1,
            description: 'Handles user login',
          },
          {
            id: 2,
            name: 'User Registration',
            systemId: 1,
            description: 'Handles new user registration',
          },
        ],
        systems: [
          { id: 1, name: 'Helpline System' },
          { id: 2, name: 'HR Portal' },
        ],
        selectedFunctionality: null,
      };
    },
    methods: {
      addFunctionality(functionality) {
        const newFunctionality = {
          id: this.functionalities.length + 1,
          ...functionality,
        };
        this.functionalities.push(newFunctionality);
      },
      editFunctionality(functionality) {
        this.selectedFunctionality = { ...functionality };
        const modal = new bootstrap.Modal(document.getElementById('addFunctionalityModal'));
        modal.show();
      },
      updateFunctionality(updatedFunctionality) {
        const index = this.functionalities.findIndex(
          (func) => func.id === updatedFunctionality.id
        );
        if (index !== -1) {
          this.functionalities[index] = { ...updatedFunctionality };
        }
      },
      deleteFunctionality(id) {
        this.functionalities = this.functionalities.filter((func) => func.id !== id);
      },
      getSystemName(systemId) {
        const system = this.systems.find((sys) => sys.id === systemId);
        return system ? system.name : 'Unknown';
      },
    },
  };
  </script>
  
  <style scoped>
  h2 {
    color: #212529;
  }
  
  .table {
    background-color: #ffffff;
  }
  
  .btn-success {
    background-color: #28a745;
  }
  
  .btn-warning {
    background-color: #ffc107;
    color: #212529;
  }
  
  .btn-danger {
    background-color: #dc3545;
  }
  </style>
  