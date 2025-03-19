<template>
    <b-modal 
      :show="show"  
      @update:show="handleShowUpdate"  
      title="Report Defect" 
      @ok="save"
    >
      <div>
        <div class="mb-3">
          <label class="form-label">Title</label>
          <input 
            v-model="formData.title"
            type="text"
            class="form-control"
            placeholder="Enter defect title"
          />
        </div>
  
        <div class="mb-3">
          <label class="form-label">Description</label>
          <textarea 
            v-model="formData.description"
            class="form-control"
            rows="3"
            placeholder="Enter defect description"
          ></textarea>
        </div>
  
        <div class="mb-3">
          <label class="form-label">Severity</label>
          <select v-model="formData.severity" class="form-control">
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
          </select>
        </div>
  
        <div class="mb-3">
          <label class="form-label">Status</label>
          <select v-model="formData.status" class="form-control">
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
  
  // Watch for changes in defectData
  watch(() => props.defectData, (newValue) => {
    if (newValue) {
      formData.value = { ...newValue };
    } else {
      formData.value = { id: null, title: '', description: '', severity: 'Medium', status: 'Open' };
    }
  }, { deep: true });
  
  // Method to handle updating the show prop
  const handleShowUpdate = (newVal) => {
    emit('update:show', newVal); // Emit updated value of `show`
  };
  
  // Save defect and close modal
  const save = () => {
    emit('save', formData.value);
    emit('update:show', false);
  };
  </script>
  
  <style scoped>
  </style>
  