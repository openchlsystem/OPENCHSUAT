<template>
    <b-modal
      :show="show" 
      title="Report Defect"
      @ok="save"
      @update:show="updateShow" 
    >
      <div>
        <div class="mb-3">
          <label class="form-label">Title</label>
          <input 
            v-model="formData.title"
            type="text"
            class="form-control"
            placeholder="Enter defect title"
            required
          />
        </div>
  
        <div class="mb-3">
          <label class="form-label">Description</label>
          <textarea 
            v-model="formData.description"
            class="form-control"
            rows="3"
            placeholder="Enter defect description"
            required
          ></textarea>
        </div>
  
        <div class="mb-3">
          <label class="form-label">Severity</label>
          <select v-model="formData.severity" class="form-control" required>
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
          </select>
        </div>
  
        <div class="mb-3">
          <label class="form-label">Status</label>
          <select v-model="formData.status" class="form-control" required>
            <option value="Open">Open</option>
            <option value="Closed">Closed</option>
          </select>
        </div>
      </div>
    </b-modal>
  </template>
  
  <script setup>
  import { defineProps, defineEmits, watch, ref } from 'vue';
  
  const props = defineProps({
    show: Boolean,
    defectData: Object,
  });
  
  const emit = defineEmits(['update:show', 'save']);
  
  const formData = ref({
    id: null,
    title: '',
    description: '',
    severity: 'Medium',
    status: 'Open',
  });
  
  // Watch for changes in defectData to populate form if editing an existing defect
  watch(() => props.defectData, (newValue) => {
    if (newValue) {
      formData.value = { ...newValue };
    } else {
      formData.value = { id: null, title: '', description: '', severity: 'Medium', status: 'Open' };
    }
  }, { deep: true, immediate: true });
  
  // Reset form data when modal is closed
  const resetForm = () => {
    formData.value = { id: null, title: '', description: '', severity: 'Medium', status: 'Open' };
  };
  
  // Save the form data and close the modal
  const save = () => {
    if (formData.value.title && formData.value.description) {
      emit('save', formData.value);
      emit('update:show', false);  // Close the modal after saving
    } else {
      alert('Please fill in all required fields');
    }
  };
  
  // Update the show prop when the modal visibility changes
  const updateShow = (value) => {
    emit('update:show', value);
  };
  </script>
  
  <style scoped>
  /* Add additional styling for the modal if needed */
  </style>
  