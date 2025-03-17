<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-container">
      <div class="modal-header">
        <h5>Edit User</h5>
        <button 
          type="button" 
          class="close-btn" 
          @click="$emit('close')"
        >
          ✕
        </button>
      </div>

      <form @submit.prevent="saveUser" class="modal-form">
        <!-- ✅ Full Name -->
        <div class="form-group">
          <label>Full Name</label>
          <input 
            type="text" 
            v-model="form.name" 
            disabled
          />
        </div>

        <!-- ✅ Email -->
        <div class="form-group">
          <label>Email</label>
          <input 
            type="email" 
            v-model="form.email" 
            disabled
          />
        </div>

        <!-- ✅ Role -->
        <div class="form-group">
          <label>Role</label>
          <select v-model="form.role" required>
            <option value="admin">Admin</option>
            <option value="tester">Tester</option>
            <option value="viewer">Viewer</option>
          </select>
        </div>

        <!-- ✅ Status -->
        <div class="form-group">
          <label>Status</label>
          <select v-model="form.is_active" required>
            <option :value="true">Active</option>
            <option :value="false">Inactive</option>
          </select>
        </div>

        <!-- ✅ Footer -->
        <div class="modal-footer">
          <button 
            type="button" 
            class="btn-secondary" 
            @click="$emit('close')"
          >
            Cancel
          </button>
          <button 
            type="submit" 
            class="btn-primary"
          >
            Save
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, watch } from 'vue';

const props = defineProps({ user: Object });
const emit = defineEmits(['save', 'close']);

const form = ref({
  name: '',
  email: '',
  role: 'tester',
  is_active: true
});

// ✅ Sync Form Data
watch(() => props.user, (newUser) => {
  if (newUser) form.value = { ...newUser };
});

const saveUser = () => emit('save', form.value);
</script>

<<style scoped>
/* ✅ Overlay to cover the entire screen */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7); /* Darker background for better contrast */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

/* ✅ Modal Container */
.modal-container {
  background-color: #ffffff;
  width: 90%;
  max-width: 500px;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  overflow-y: auto;
  max-height: 90vh;
}

/* ✅ Modal Header */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  border-bottom: 1px solid #e0e0e0;
}

.modal-header h5 {
  font-size: 1.25rem;
  color: #000;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #ff7f0e;
  cursor: pointer;
}

/* ✅ Form Styling */
.modal-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 16px;
}

label {
  display: block;
  font-size: 0.95rem;
  font-weight: 500;
  color: #000;
  margin-bottom: 4px;
}

input,
textarea,
select {
  width: 100%;
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  color: #000;
  transition: border-color 0.2s;
}

input:focus,
textarea:focus,
select:focus {
  border-color: #ff7f0e;
  outline: none;
}

/* ✅ Footer Styling */
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 16px;
}

/* ✅ Primary Button */
.btn-primary {
  background-color: #ff7f0e;
  color: #ffffff;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #e67300;
}

/* ✅ Secondary Button */
.btn-secondary {
  background-color: #000;
  color: #ffffff;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-secondary:hover {
  background-color: #333;
}

/* ✅ Responsive Sizing */
@media (max-width: 480px) {
  .modal-container {
    width: 100%;
    padding: 16px;
  }
}
</style>
