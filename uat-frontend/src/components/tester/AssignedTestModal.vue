<template>
  <b-modal 
    :show="show"   
    @update:show="handleShowUpdate"  
    title="Assigned Test Details" 
    @hidden="$emit('close')"
    class="modal-theme"
  >
    <div>
      <p><strong>Title:</strong> {{ testData?.title }}</p>
      <p><strong>System:</strong> {{ testData?.system }}</p>
      <p><strong>Status:</strong> 
        <span :class="getStatusClass(testData?.status)">
          {{ testData?.status }}
        </span>
      </p>
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

// Method to assign status classes
const getStatusClass = (status) => {
  return status === 'Completed' ? 'text-success' : 'text-warning';
};
</script>

<style scoped>
.modal-theme {
  border-radius: 15px;
  background-color: #f9f9f9;
}

.modal-header {
  background-color: #0066cc; /* Blue */
  color: white;
}

.modal-body p {
  font-size: 16px;
}

.text-success {
  color: #28a745; /* Green */
}

.text-warning {
  color: #ff8c00; /* Orange */
}
</style>
