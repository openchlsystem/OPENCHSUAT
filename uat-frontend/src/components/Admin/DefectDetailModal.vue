<!-- src/components/admin/DefectDetailModal.vue -->
<template>
    <div class="modal-overlay">
      <div class="modal-content">
        <h3>Defect Details</h3>
        <p><strong>Name:</strong> {{ defect.name }}</p>
        <p><strong>Description:</strong> {{ defect.description }}</p>
        <p><strong>Test Case:</strong> {{ defect.test_case }}</p>
        <p><strong>Severity:</strong> <span :class="`severity-${defect.severity}`">{{ defect.severity }}</span></p>
        <p><strong>Status:</strong> <span :class="`status-${defect.status}`">{{ defect.status }}</span></p>
        <p><strong>Date Reported:</strong> {{ new Date(defect.reported_at).toLocaleString() }}</p>
  
        <button @click="$emit('close')" class="btn-close">Close</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      defect: Object
    }
  };
  </script>
  
  <style scoped>
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
  
  .modal-content {
    background: white;
    padding: 20px;
    border-radius: 8px;
    width: 400px;
  }
  
  .btn-close {
    background: #003366; /* Theme color - Blue */
    color: white;
    padding: 10px;
    border: none;
    cursor: pointer;
  }
  </style>
  