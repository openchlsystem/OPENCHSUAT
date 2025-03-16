<template>
  <form @submit.prevent="handleSubmit">
    <div class="mb-3">
      <label for="title" class="form-label">Defect Title</label>
      <input type="text" id="title" v-model="defect.title" class="form-control" required />
    </div>

    <div class="mb-3">
      <label for="description" class="form-label">Description</label>
      <textarea id="description" v-model="defect.description" class="form-control" rows="4" required></textarea>
    </div>

    <div class="mb-3">
      <label for="severity" class="form-label">Severity</label>
      <select id="severity" v-model="defect.severity" class="form-select" required>
        <option value="Low">Low</option>
        <option value="Medium">Medium</option>
        <option value="High">High</option>
      </select>
    </div>

    <div class="mb-3">
      <label for="priority" class="form-label">Priority</label>
      <select id="priority" v-model="defect.priority" class="form-select" required>
        <option value="Low">Low</option>
        <option value="Medium">Medium</option>
        <option value="High">High</option>
      </select>
    </div>

    <div class="mb-3">
      <label for="evidence" class="form-label">Attach Evidence</label>
      <input type="file" id="evidence" class="form-control" @change="handleFileChange" />
    </div>

    <div class="mb-3">
      <button type="submit" class="btn btn-primary">Submit Defect</button>
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
  // Emit the defect data to parent component (DefectsReport.vue)
  emit('submit', defect.value);
  // Optionally, reset the form after submission
  defect.value = { title: '', description: '', severity: 'Low', priority: 'Low', evidence: null };
};
</script>

<style scoped>
/* Optional: Add custom styling */
</style>
