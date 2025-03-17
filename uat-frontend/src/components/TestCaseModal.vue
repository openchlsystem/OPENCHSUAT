<template>
  <!-- Modal Trigger -->
  <button 
    class="btn btn-primary mb-3" 
    @click="openModal"
  >
    + New Test Case
  </button>

  <!-- Modal Overlay -->
  <div 
    v-if="showModal" 
    class="modal-overlay" 
    @click.self="closeModal"
  >
    <div class="modal-container">
      <div class="modal-header">
        <h5>{{ isEdit ? 'Edit Test Case' : 'Create Test Case' }}</h5>
        <button 
          type="button" 
          class="close-btn" 
          @click="closeModal"
        >
          ✕
        </button>
      </div>

      <form @submit.prevent="saveTestCase" class="modal-form">
        <!-- ✅ Title -->
        <div class="form-group">
          <label>Title</label>
          <input 
            type="text" 
            v-model="form.title" 
            required 
          />
        </div>

        <!-- ✅ Description -->
        <div class="form-group">
          <label>Description</label>
          <textarea 
            v-model="form.description" 
            rows="3" 
            required
          ></textarea>
        </div>

        <!-- ✅ Expected Outcome -->
        <div class="form-group">
          <label>Expected Outcome</label>
          <input 
            type="text" 
            v-model="form.expected_outcome" 
            required 
          />
        </div>

        <!-- ✅ Status -->
        <div class="form-group">
          <label>Status</label>
          <select v-model="form.status" required>
            <option value="open">Open</option>
            <option value="in_progress">In Progress</option>
            <option value="closed">Closed</option>
          </select>
        </div>

        <!-- ✅ Assign to Tester -->
        <div class="form-group">
          <label>Assign to Tester</label>
          <select v-model="form.assigned_to">
            <option value="">Unassigned</option>
            <option 
              v-for="tester in testers" 
              :key="tester.id" 
              :value="tester.id"
            >
              {{ tester.username }}
            </option>
          </select>
        </div>

        <!-- ✅ Modal Footer -->
        <div class="modal-footer">
          <button 
            type="button" 
            class="btn-secondary" 
            @click="closeModal"
          >
            Cancel
          </button>
          <button 
            type="submit" 
            class="btn-primary"
          >
            {{ isEdit ? 'Update' : 'Create' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, watch } from 'vue';

const props = defineProps({
  isEdit: Boolean,
  testCase: Object,
  testers: Array
});

const emit = defineEmits(['save']);

const showModal = ref(false);

const form = ref({
  title: '',
  description: '',
  expected_outcome: '',
  status: 'open',
  assigned_to: ''
});

// ✅ Reset form when editing a test case
watch(() => props.testCase, (newValue) => {
  if (newValue) {
    form.value = { ...newValue };
  } else {
    resetForm();
  }
});

const openModal = () => {
  showModal.value = true;
};

const closeModal = () => {
  resetForm();
  showModal.value = false;
};

const saveTestCase = () => {
  emit('save', form.value);
  closeModal();
};

const resetForm = () => {
  form.value = {
    title: '',
    description: '',
    expected_outcome: '',
    status: 'open',
    assigned_to: ''
  };
};
</script>

<style scoped>
/* ✅ Overlay to cover the entire screen */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7); /* Darker background for better contrast */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

/* ✅ Modal Container */
.modal-container {
  background-color: #ffffff;
  width: 90%;
  max-width: 500px;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  overflow-y: auto;
  max-height: 90vh;
}

/* ✅ Modal Header */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  border-bottom: 1px solid #e0e0e0;
}

.modal-header h5 {
  font-size: 1.25rem;
  color: #000;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #ff7f0e;
  cursor: pointer;
}

/* ✅ Form Styling */
.modal-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 16px;
}

label {
  display: block;
  font-size: 0.95rem;
  font-weight: 500;
  color: #000;
  margin-bottom: 4px;
}

input,
textarea,
select {
  width: 100%;
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  color: #000;
  transition: border-color 0.2s;
}

input:focus,
textarea:focus,
select:focus {
  border-color: #ff7f0e;
  outline: none;
}

/* ✅ Footer Styling */
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 16px;
}

/* ✅ Primary Button */
.btn-primary {
  background-color: #ff7f0e;
  color: #ffffff;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #e67300;
}

/* ✅ Secondary Button */
.btn-secondary {
  background-color: #000;
  color: #ffffff;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-secondary:hover {
  background-color: #333;
}

/* ✅ Responsive Sizing */
@media (max-width: 480px) {
  .modal-container {
    width: 100%;
    padding: 16px;
  }
}
</style>
