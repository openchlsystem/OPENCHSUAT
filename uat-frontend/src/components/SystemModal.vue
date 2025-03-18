<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3 class="modal-title">{{ form.id ? "Edit System" : "Add New System" }}</h3>
      <form @submit.prevent="submitForm">
        
        <!-- System Name -->
        <div class="mb-3">
          <label class="form-label">System Name</label>
          <input v-model="form.name" class="form-control" required />
        </div>

        <!-- Organization -->
        <div class="mb-3">
          <label class="form-label">Organization</label>
          <select v-model="form.organization" class="form-control" required>
            <option v-for="org in organizations" :key="org.id" :value="org.id">
              {{ org.name }}
            </option>
          </select>
        </div>

        <!-- Description -->
        <div class="mb-3">
          <label class="form-label">Description</label>
          <textarea v-model="form.description" class="form-control" rows="3" required></textarea>
        </div>

        <!-- Buttons -->
        <div class="d-flex justify-content-between">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">Cancel</button>
          <button type="submit" class="btn btn-primary">{{ form.id ? "Update" : "Create" }}</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps(["system"]);
const emit = defineEmits(["close", "save"]);

const form = ref({ id: null, name: "", organization: "", description: "" });

// Watch for system prop changes (for edit mode)
watch(
  () => props.system,
  (newSystem) => {
    form.value = newSystem
      ? { ...newSystem }
      : { id: null, name: "", organization: "", description: "" };
  },
  { immediate: true }
);

const submitForm = () => {
  emit("save", form.value);
};
</script>

<style scoped>
/* Overlay */
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

/* Modal Content */
.modal-content {
  background: #fff;
  padding: 25px;
  width: 400px;
  border-radius: 10px;
}

/* Form */
.form-control {
  border-radius: 5px;
  padding: 8px;
}
</style>
