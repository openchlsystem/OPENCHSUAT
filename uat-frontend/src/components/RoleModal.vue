<template>
    <b-modal 
      :show="show"                      
      @update:show="handleShowUpdate"    
      title="Manage Roles & Permissions"
      @ok="save"
    >
      <div>
        <div class="mb-3">
          <label class="form-label">Role Name</label>
          <input 
            v-model="roleName"
            type="text"
            class="form-control"
            placeholder="Enter role name"
          />
        </div>
  
        <div class="mb-3">
          <label class="form-label">Permissions</label>
          <div class="form-check" v-for="permission in permissions" :key="permission">
            <input
              type="checkbox"
              class="form-check-input"
              :id="permission"
              v-model="selectedPermissions"
              :value="permission"
            />
            <label class="form-check-label" :for="permission">{{ permission }}</label>
          </div>
        </div>
      </div>
    </b-modal>
  </template>
  
  <script setup>
  import { defineProps, defineEmits, ref } from 'vue';
  
  // Props
  const props = defineProps({
    show: Boolean
  });
  
  // Emits
  const emit = defineEmits(['update:show', 'save']);
  
  // Data
  const roleName = ref('');
  const selectedPermissions = ref([]);
  const permissions = ref([
    'View Reports',
    'Manage Users',
    'Create Test Cases',
    'Execute Test Cases'
  ]);
  
  // Save function
  const save = () => {
    console.log('Saving Role Settings:', {
      roleName: roleName.value,
      permissions: selectedPermissions.value
    });
    emit('save'); // Trigger save action in parent
    emit('update:show', false); // Close the modal by updating the show prop
  };
  
  // Emit update:show event to handle visibility changes
  const handleShowUpdate = (newValue) => {
    emit('update:show', newValue);
  };
  </script>
  
  <style scoped>
  </style>
  