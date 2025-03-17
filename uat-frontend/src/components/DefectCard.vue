<template>
    <div class="card defect-card">
      <div class="card-body">
        <h5 class="card-title">{{ defect.title }}</h5>
        <p class="card-text">{{ defect.description }}</p>
        <div class="d-flex justify-content-between align-items-center">
          <span :class="statusClass">{{ defect.status }}</span>
          <span :class="priorityClass">{{ defect.priority }}</span>
        </div>
        <div class="mt-2 small text-muted">Reported by: {{ defect.createdBy }}</div>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({
    defect: Object,
  });
  
  const statusClass = (defect) => {
    switch (defect.status) {
      case 'Open':
        return 'badge bg-danger';
      case 'Closed':
        return 'badge bg-success';
      case 'In Progress':
        return 'badge bg-warning text-dark';
      default:
        return 'badge bg-secondary';
    }
  };
  
  const priorityClass = (defect) => {
    switch (defect.priority) {
      case 'Low':
        return 'badge bg-info';
      case 'Medium':
        return 'badge bg-warning text-dark';
      case 'High':
        return 'badge bg-danger';
      default:
        return 'badge bg-secondary';
    }
  };
  </script>
  
  <style scoped>
  .defect-card {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    transition: transform 0.2s ease-in-out;
  }
  .defect-card:hover {
    transform: translateY(-5px);
  }
  .card-title {
    font-size: 18px;
    font-weight: bold;
  }
  .badge {
    font-size: 14px;
    padding: 6px 12px;
    border-radius: 12px;
  }
  </style>
  