<template>
    <div class="modal d-block" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ step?.id ? 'Edit Step' : 'Add Step' }}</h5>
            <button type="button" class="btn-close" @click="$emit('close')"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="save">
              <div class="mb-3">
                <label class="form-label">Description</label>
                <input
                  v-model="form.description"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Expected Result</label>
                <input
                  v-model="form.expectedResult"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="d-flex justify-content-end">
                <button type="button" class="btn btn-secondary me-2" @click="$emit('close')">
                  Cancel
                </button>
                <button type="submit" class="btn btn-primary">
                  {{ step?.id ? 'Update' : 'Save' }}
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
      step: {
        type: Object,
        default: null,
      },
    },
    data() {
      return {
        form: {
          description: '',
          expectedResult: '',
        },
      };
    },
    watch: {
      step: {
        immediate: true,
        handler(newStep) {
          if (newStep) {
            this.form = { ...newStep };
          } else {
            this.form = {
              description: '',
              expectedResult: '',
            };
          }
        },
      },
    },
    methods: {
      save() {
        if (!this.form.description || !this.form.expectedResult) {
          alert('All fields are required');
          return;
        }
        this.$emit('save', { ...this.form });
      },
    },
  };
  </script>
  
  <style scoped>
  .modal {
    background-color: rgba(0, 0, 0, 0.5);
  }
  .modal-content {
    padding: 20px;
    border-radius: 8px;
  }
  .btn {
    font-size: 14px;
  }
  </style>
  