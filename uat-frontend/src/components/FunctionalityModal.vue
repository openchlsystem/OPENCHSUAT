<template>
    <div class="modal fade" :id="id" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEdit ? 'Edit Functionality' : 'Add Functionality' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveFunctionality">
              <div class="mb-3">
                <label class="form-label">Functionality Name</label>
                <input type="text" class="form-control" v-model="form.name" required />
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
      functionality: Object,
      systems: Array, // ✅ Pass systems from parent
    },
    data() {
      return {
        form: {
          name: '',
          systemId: '',
          description: '',
        },
        isEdit: false,
      };
    },
    watch: {
      functionality(newVal) {
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
      saveFunctionality() {
        if (this.isEdit) {
          this.$emit('update-functionality', this.form);
        } else {
          this.$emit('add-functionality', this.form);
        }
        this.resetForm();
        this.closeModal();
      },
      resetForm() {
        this.form = {
          name: '',
          systemId: '',
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
  