<template>
    <div class="modal fade" :id="id" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEdit ? 'Edit Test Case' : 'Add Test Case' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveTestCase">
              <div class="mb-3">
                <label class="form-label">Title</label>
                <input type="text" class="form-control" v-model="form.title" required />
              </div>
              <div class="mb-3">
                <label class="form-label">System</label>
                <select class="form-select" v-model="form.systemId" required>
                  <option v-for="system in systems" :key="system.id" :value="system.id">
                    {{ system.name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Functionality</label>
                <select class="form-select" v-model="form.functionalityId" required>
                  <option v-for="functionality in functionalities" :key="functionality.id" :value="functionality.id">
                    {{ functionality.name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea class="form-control" v-model="form.description" required></textarea>
              </div>
              <div class="text-end">
                <button type="button" class="btn btn-secondary me-2" data-bs-dismiss="modal">
                  Cancel
                </button>
                <button type="submit" class="btn btn-primary">
                  {{ isEdit ? 'Update' : 'Save' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      id: String,
      testCase: Object,
      systems: Array,
      functionalities: Array,
    },
    data() {
      return {
        form: {
          title: '',
          systemId: '',
          functionalityId: '',
          description: '',
        },
        isEdit: false,
      };
    },
    watch: {
      testCase(newVal) {
        if (newVal) {
          this.form = { ...newVal };
          this.isEdit = true;
        } else {
          this.isEdit = false;
          this.resetForm();
        }
      },
    },
    methods: {
      saveTestCase() {
        if (this.isEdit) {
          this.$emit('update-test-case', this.form);
        } else {
          this.$emit('add-test-case', this.form);
        }
        this.resetForm();
        this.closeModal();
      },
      resetForm() {
        this.form = {
          title: '',
          systemId: '',
          functionalityId: '',
          description: '',
        };
      },
      closeModal() {
        const modal = new bootstrap.Modal(document.getElementById(this.id));
        modal.hide();
      },
    },
  };
  </script>
  
  <style scoped>
  .modal-title {
    font-weight: 600;
  }
  
  .form-control,
  .form-select {
    border-radius: 5px;
  }
  
  .btn-primary {
    background-color: #007bff;
    border-color: #007bff;
  }
  
  .btn-secondary {
    background-color: #6c757d;
    border-color: #6c757d;
  }
  </style>
  