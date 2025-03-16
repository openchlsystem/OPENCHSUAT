<template>
  <b-modal 
    :model-value="showModal" 
    @update:modelValue="$emit('update:showModal', $event)"
    :title="modalTitle"
    centered
    size="md"
    @hidden="resetForm"
    hide-footer
  >
    <form @submit.prevent="handleSubmit">
      <div class="mb-3">
        <label class="form-label">Name</label>
        <input 
          v-model="formData.name" 
          type="text" 
          class="form-control"
          placeholder="Enter full name"
          required
        />
      </div>

      <div class="mb-3">
        <label class="form-label">Email</label>
        <input 
          v-model="formData.email" 
          type="email" 
          class="form-control"
          placeholder="Enter email"
          required
        />
      </div>

      <div class="mb-3">
        <label class="form-label">Role</label>
        <select v-model="formData.role" class="form-select" required>
          <option value="Admin">Admin</option>
          <option value="Tester">Tester</option>
          <option value="Viewer">Viewer</option>
        </select>
      </div>

      <div class="mb-3">
        <label class="form-label">Password</label>
        <input 
          v-model="formData.password" 
          type="password" 
          class="form-control"
          placeholder="Enter password"
          :required="!formData.id"
        />
      </div>

      <div class="mb-3">
        <label class="form-label">Status</label>
        <select v-model="formData.status" class="form-select" required>
          <option value="Active">Active</option>
          <option value="Inactive">Inactive</option>
        </select>
      </div>

      <!-- Modal Footer -->
      <div class="d-flex justify-content-end">
        <button 
          type="button" 
          class="btn btn-secondary me-2" 
          @click="$emit('update:showModal', false)"
        >
          Cancel
        </button>
        <button type="submit" class="btn btn-dark">
          {{ formData.id ? 'Update' : 'Create' }}
        </button>
      </div>
    </form>
  </b-modal>
</template>

<script setup>
import { ref, defineProps, defineEmits, watch } from 'vue';

const props = defineProps({
  showModal: Boolean,
  modalTitle: String,
  userData: Object
});

const emit = defineEmits(['update:showModal', 'submit']);

const formData = ref({
  id: null,
  name: '',
  email: '',
  role: 'Tester',
  password: '',
  status: 'Active'
});

watch(() => props.userData, (newValue) => {
  if (newValue) {
    formData.value = { ...newValue, password: '' };
  }
}, { immediate: true });

const handleSubmit = () => {
  emit('submit', formData.value);
};

const resetForm = () => {
  formData.value = {
    id: null,
    name: '',
    email: '',
    role: 'Tester',
    password: '',
    status: 'Active'
  };
};
</script>

<style scoped>
</style>
