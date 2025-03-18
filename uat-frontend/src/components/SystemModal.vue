<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3 class="modal-title">Add New System</h3>
      <form @submit.prevent="submitForm">
        <!-- System Name -->
        <div class="mb-3">
          <label class="form-label">System Name</label>
          <input v-model="form.name" class="form-control" placeholder="Enter system name" required />
        </div>

        <!-- Organization Dropdown -->
        <div class="mb-3">
          <label class="form-label">Organization</label>
          <select v-model="form.organization" class="form-control" required>
            <option v-for="org in organizations" :key="org.id" :value="org.id">
              {{ org.name }}
            </option>
          </select>
        </div>

        <!-- Description -->
        <div class="mb-3">
          <label class="form-label">Description</label>
          <textarea v-model="form.description" class="form-control" rows="3" placeholder="Enter description"></textarea>
        </div>

        <!-- Action Buttons -->
        <div class="button-group">
          <button type="button" class="btn btn-secondary" @click="$emit('closeModal')">Cancel</button>
          <button type="submit" class="btn btn-primary">Create System</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    organizations: Array
  },
  data() {
    return {
      form: { name: '', organization: '', description: '' }
    };
  },
  methods: {
    submitForm() {
      this.$emit('createSystem', this.form);
      this.$emit('closeModal');
    }
  }
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
}

/* Modal Content */
.modal-content {
  background: #ffffff;
  padding: 25px;
  width: 400px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
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
}

textarea.form-control {
  resize: none;
}

/* Button Group */
.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
}

/* Buttons - Same Size & Feel */
.btn {
  flex: 1;
  padding: 10px;
  font-weight: bold;
  border-radius: 6px;
  text-align: center;
}

.btn-secondary {
  background-color: #6c757d;
  color: #fff;
  border: none;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
  border: none;
}

.btn-primary:hover {
  background-color: #0056b3;
}

</style>
