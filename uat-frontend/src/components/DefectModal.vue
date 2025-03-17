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
        <label class="form-label">Priority</label>
        <select v-model="formData.priority" class="form-control" required>
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
        </select>
      </div>

      <div class="mb-3">
        <label class="form-label">Evidence</label>
        <input type="file" @change="handleFileChange" class="form-control" />
      </div>
    </div>
  </b-modal>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  show: Boolean,
  defectData: Object,
});

const emit = defineEmits(['update:show', 'save']);

const formData = ref({
  title: '',
  description: '',
  severity: 'Medium',
  priority: 'Medium',
  evidence: null,
});

watch(() => props.defectData, (newValue) => {
  if (newValue) {
    formData.value = { ...newValue };
  } else {
    formData.value = { title: '', description: '', severity: 'Medium', priority: 'Medium', evidence: null };
  }
}, { deep: true, immediate: true });

const handleFileChange = (event) => {
  formData.value.evidence = event.target.files[0];
};

const save = () => {
  if (formData.value.title && formData.value.description) {
    emit('save', formData.value);
    emit('update:show', false); // Close the modal after saving
  } else {
    alert('Please fill in all required fields');
  }
};

const updateShow = (value) => {
  emit('update:show', value);
};
</script>

<style scoped>
/* Add any additional styling for the modal if needed */
</style>
