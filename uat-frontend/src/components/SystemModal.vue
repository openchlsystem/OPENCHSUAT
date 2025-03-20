<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3 class="modal-title">{{ system ? 'Edit System' : 'Add New System' }}</h3>
      <form @submit.prevent="submitForm">
        <div class="mb-3">
          <label class="form-label">System Name</label>
          <input v-model="form.name" class="form-control" placeholder="Enter system name" required />
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
          <textarea v-model="form.description" class="form-control" rows="3" placeholder="Enter description"></textarea>
        </div>

        <div class="button-group">
          <button type="button" class="btn btn-secondary" @click="$emit('closeModal')">Cancel</button>
          <button type="submit" class="btn btn-primary">{{ system ? 'Update' : 'Create' }} System</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    organizations: {
      type: Array,
      required: true,
    },
    system: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      form: {
        name: '',
        organization: '',
        description: '',
      },
    };
  },
  watch: {
    system: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.form = { ...newVal };
        } else {
          this.form = { name: '', organization: '', description: '' };
        }
      },
    },
  },
  methods: {
     submitForm() {
            console.log('Form data:', this.form);
            console.log('Organization ID:', typeof this.form.organization, this.form.organization);
            this.$emit('saveSystem', this.form);
            this.$emit('closeModal');
        },
  },
};
</script>

<style scoped>
/* Overlay Styling */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000; /* Ensure it's on top */
}

/* Modal Content */
.modal-content {
  background: #ffffff;
  padding: 25px;
  width: 400px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  z-index: 1001; /* Ensure it's on top of the overlay */
}

/* Modal Title */
.modal-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #2c3e50;
}

/* Form Styling */
.form-label {
  font-weight: 600;
  color: #34495e;
}

.form-control {
  border-radius: 6px;
  padding: 10px;
  border: 1px solid #ccc;
  width: 100%; /* Ensure full width */
  box-sizing: border-box; /* Include padding and border in width */
}

textarea.form-control {
  resize: vertical; /* Allow vertical resizing */
}

/* Button Group */
.button-group {
  display: flex;
  justify-content: flex-end; /* Align buttons to the right */
  margin-top: 20px;
}

/* Buttons - Same Size & Feel */
.btn {
  padding: 10px 15px;
  font-weight: bold;
  border-radius: 6px;
  text-align: center;
  margin-left: 10px; /* Add spacing between buttons */
  cursor: pointer;
  border: none;
}

.btn-secondary {
  background-color: #6c757d;
  color: #fff;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
}

.btn-primary:hover {
  background-color: #0056b3;
}
</style>