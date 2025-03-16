<template>
    <b-modal 
      :show="show"   
      @update:show="handleShowUpdate"  
      title="Assigned Test Details" 
      @hidden="$emit('close')"
    >
      <div>
        <p><strong>Title:</strong> {{ testData?.title }}</p>
        <p><strong>System:</strong> {{ testData?.system }}</p>
        <p><strong>Status:</strong> {{ testData?.status }}</p>
        <p><strong>Description:</strong> {{ testData?.description }}</p>
        <p><strong>Assigned Date:</strong> {{ formatDate(testData?.assigned_date) }}</p>
      </div>
    </b-modal>
  </template>
  
  <script setup>
  import { defineProps, defineEmits } from 'vue';
  
  const props = defineProps({
    show: Boolean,
    testData: Object
  });
  
  const emit = defineEmits(['close']);
  
  // Method to format date
  const formatDate = (date) => {
    return new Date(date).toLocaleDateString();
  };
  
  // Method to update `show` prop value
  const handleShowUpdate = (newVal) => {
    emit('update:show', newVal); // Emit updated value of `show`
  };
  </script>
  
  <style scoped>
  </style>
  