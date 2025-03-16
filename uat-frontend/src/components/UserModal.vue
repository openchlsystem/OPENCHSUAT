<template>
    <b-modal 
      :show="show" 
      @update:show="handleShowUpdate"  
      title="Manage User" 
      @ok="save"
    >
      <div>
        <div class="mb-3">
          <label class="form-label">Name</label>
          <input 
            v-model="formData.name"
            type="text"
            class="form-control"
            placeholder="Enter full name"
          />
        </div>
  
        <div class="mb-3">
          <label class="form-label">Email</label>
          <input 
            v-model="formData.email"
            type="email"
            class="form-control"
            placeholder="Enter email address"
          />
        </div>
  
        <div class="mb-3">
          <label class="form-label">Role</label>
          <select v-model="formData.role" class="form-control">
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
          />
        </div>
  
        <div class="mb-3">
          <label class="form-label">Status</label>
          <select v-model="formData.status" class="form-control">
            <option value="Active">Active</option>
            <option value="Inactive">Inactive</option>
          </select>
        </div>
      </div>
    </b-modal>
  </template>
  
  <script setup>
  import { defineProps, defineEmits, watch, ref } from 'vue';
  
  const props = defineProps({
    show: Boolean,
    userData: Object,
  });
  
  const emit = defineEmits(['update:show', 'save']);
  
  const formData = ref({
    id: null,
    name: '',
    email: '',
    role: 'Tester',
    password: '',  // New field for password
    status: 'Active',
  });
  
  // Watch for changes in userData
  watch(() => props.userData, (newValue) => {
    if (newValue) {
      formData.value = { ...newValue, password: '' };  // Reset password field for security
    } else {
      formData.value = { id: null, name: '', email: '', role: 'Tester', password: '', status: 'Active' };
    }
  }, { deep: true, immediate: true });
  
  const save = () => {
    emit('save', formData.value);
    emit('update:show', false);  // Close the modal after saving
  };
  
  // Handle modal visibility update
  const handleShowUpdate = (newVal) => {
    emit('update:show', newVal);  // Emit update:show to handle visibility change
  };
  </script>
  
  <style scoped>
  </style>
  