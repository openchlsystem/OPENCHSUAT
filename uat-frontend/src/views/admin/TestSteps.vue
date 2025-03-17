<template>
    <div class="container mt-4">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h3 class="text-primary">Test Steps for "{{ testCase?.title }}"</h3>
        <button class="btn btn-success" @click="openModal(null)">+ Add Step</button>
      </div>
  
      <!-- Test Steps Table -->
      <div class="table-responsive">
        <table class="table table-bordered table-hover">
          <thead class="table-dark">
            <tr>
              <th>#</th>
              <th>Description</th>
              <th>Expected Result</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(step, index) in testSteps" :key="step.id">
              <td>{{ index + 1 }}</td>
              <td>{{ step.description }}</td>
              <td>{{ step.expectedResult }}</td>
              <td>
                <button class="btn btn-warning btn-sm me-2" @click="openModal(step)">
                  ✏️ Edit
                </button>
                <button class="btn btn-danger btn-sm" @click="deleteStep(step.id)">
                  🗑️ Delete
                </button>
              </td>
            </tr>
            <tr v-if="testSteps.length === 0">
              <td colspan="4" class="text-center text-muted">No steps found</td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- Test Step Modal -->
      <TestStepModal
        v-if="showModal"
        :step="selectedStep"
        @close="closeModal"
        @save="saveStep"
      />
    </div>
  </template>
  
  <script>
  import TestStepModal from '@/components/TestStepsModal.vue';
  
  export default {
    name: 'TestStepsView',
    components: {
      TestStepModal,
    },
    data() {
      return {
        testCase: null,
        testSteps: [],
        showModal: false,
        selectedStep: null,
      };
    },
    created() {
      this.loadTestSteps();
    },
    methods: {
      loadTestSteps() {
        // Mock data (replace with API call later)
        this.testCase = {
          id: 1,
          title: 'Sample Test Case',
        };
        this.testSteps = [
          {
            id: 1,
            description: 'Open the login page',
            expectedResult: 'Login page should load successfully',
          },
          {
            id: 2,
            description: 'Enter valid credentials',
            expectedResult: 'User should be logged in',
          },
        ];
      },
      openModal(step) {
        this.selectedStep = step ? { ...step } : null;
        this.showModal = true;
      },
      closeModal() {
        this.showModal = false;
      },
      saveStep(step) {
        if (step.id) {
          // Update existing step
          const index = this.testSteps.findIndex((s) => s.id === step.id);
          if (index !== -1) {
            this.testSteps.splice(index, 1, step);
          }
        } else {
          // Add new step
          step.id = this.testSteps.length + 1;
          this.testSteps.push(step);
        }
        this.closeModal();
      },
      deleteStep(id) {
        if (confirm('Are you sure you want to delete this step?')) {
          this.testSteps = this.testSteps.filter((step) => step.id !== id);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    background-color: #fff;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  h3 {
    color: #0d6efd;
  }
  .table th,
  .table td {
    vertical-align: middle;
  }
  .btn {
    font-size: 14px;
  }
  </style>
  