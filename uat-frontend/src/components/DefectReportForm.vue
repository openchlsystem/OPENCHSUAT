<template>
  <form @submit.prevent="handleSubmit" class="p-4 shadow-sm rounded border bg-light">
    <div class="mb-3">
      <label for="title" class="form-label text-dark">Defect Title</label>
      <input type="text" id="title" v-model="defect.title" class="form-control" required />
    </div>

    <div class="mb-3">
      <label for="description" class="form-label text-dark">Description</label>
      <textarea id="description" v-model="defect.description" class="form-control" rows="4" required></textarea>
    </div>

    <div class="mb-3">
      <label for="severity" class="form-label text-dark">Severity</label>
      <select id="severity" v-model="defect.severity" class="form-select" required>
        <option value="Low">Low</option>
        <option value="Medium">Medium</option>
        <option value="High">High</option>
      </select>
    </div>

    <div class="mb-3">
      <label for="priority" class="form-label text-dark">Priority</label>
      <select id="priority" v-model="defect.priority" class="form-select" required>
        <option value="Low">Low</option>
        <option value="Medium">Medium</option>
        <option value="High">High</option>
      </select>
    </div>

    <div class="mb-3">
      <label for="evidence" class="form-label text-dark">Attach Evidence</label>
      <input type="file" id="evidence" class="form-control" @change="handleFileChange" />
    </div>

    <div class="mb-3 text-center">
      <button type="submit" class="btn btn-primary w-100">Submit Defect</button>
    </div>
  </form>
</template>

<script setup>
import { ref } from 'vue';

const defect = ref({
  title: '',
  description: '',
  severity: 'Low',
  priority: 'Low',
  evidence: null
});

const handleFileChange = (event) => {
  defect.value.evidence = event.target.files[0];
};

const handleSubmit = () => {
  // Emit the defect data to the parent component (DefectReportView.vue)
  emit('submit', defect.value);
  // Reset the form after submission
  defect.value = { title: '', description: '', severity: 'Low', priority: 'Low', evidence: null };
};
</script>

<style scoped>
/* Custom Form Styling */
.form-label {
  font-weight: 600;
  color: #333; /* Dark text for readability */
}

.form-control {
  border-radius: 0.375rem;
  border: 1px solid #ced4da;
  background-color: #f8f9fa;
}

.form-select {
  border-radius: 0.375rem;
  border: 1px solid #ced4da;
  background-color: #f8f9fa;
}

.btn-primary {
  background-color: #007bff; /* Blue button */
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #004085;
}

.bg-light {
  background-color: #f8f9fa !important; /* Light background for the form */
}

.p-4 {
  padding: 2rem !important;
}

.shadow-sm {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075) !important;
}

.w-100 {
  width: 100% !important;
}
</style>
