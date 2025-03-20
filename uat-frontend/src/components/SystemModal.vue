<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3>{{ system?.id ? "Edit System" : "Create System" }}</h3>

      <form @submit.prevent="handleSubmit">
        <!-- System Name -->
        <div class="mb-3">
          <label class="form-label">System Name</label>
          <input type="text" v-model="form.name" class="form-control" required />
        </div>

        <!-- System Description -->
        <div class="mb-3">
          <label class="form-label">Description</label>
          <textarea v-model="form.description" class="form-control" rows="3" required></textarea>
        </div>

        <!-- Organization Selection -->
        <div class="mb-3">
          <label class="form-label">Organization</label>
          <select v-model="form.organization" class="form-control" required>
            <option v-for="org in organizations" :key="org.id" :value="org.id">
              {{ org.name }}
            </option>
          </select>
        </div>

        <!-- Actions -->
        <div class="d-flex justify-content-between">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">Cancel</button>
          <button type="submit" class="btn btn-primary">{{ system?.id ? "Update" : "Create" }}</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  system: Object,
  organizations: Array, // Keep organizations unchanged
});
const emit = defineEmits(["close", "save"]);

const form = ref({
  name: "",
  description: "",
  organization: null, // Keep organization handling unchanged
});

// Watch for system changes and update form
watch(
  () => props.system,
  (newSystem) => {
    if (newSystem) {
      form.value = { ...newSystem };
    } else {
      form.value = { name: "", description: "", organization: null };
    }
  },
  { immediate: true }
);

const handleSubmit = () => {
  emit("save", form.value);
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
  border-radius: 5px;
  width: 400px;
}

.btn-primary {
  background-color: #ff7f0e;
  border-color: #ff7f0e;
}

.btn-primary:hover {
  background-color: #e67300;
  border-color: #e67300;
}
</style>
