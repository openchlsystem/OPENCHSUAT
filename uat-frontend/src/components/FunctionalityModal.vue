<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3>{{ functionality?.id ? "Edit Functionality" : "Create Functionality" }}</h3>

      <form @submit.prevent="handleSubmit">
        <!-- Functionality Name -->
        <div class="mb-3">
          <label class="form-label">Functionality Name</label>
          <input type="text" v-model="form.name" class="form-control" required />
        </div>

        <!-- Description -->
        <div class="mb-3">
          <label class="form-label">Description</label>
          <textarea v-model="form.description" class="form-control" rows="3" required></textarea>
        </div>

        <!-- System Selection -->
        <div class="mb-3">
          <label class="form-label">System</label>
          <select v-model="form.system" class="form-control" required>
            <option v-for="sys in systems" :key="sys.id" :value="sys.id">
              {{ sys.name }}
            </option>
          </select>
        </div>

        <!-- Actions -->
        <div class="d-flex justify-content-between">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">Cancel</button>
          <button type="submit" class="btn btn-primary">
            {{ functionality?.id ? "Update" : "Create" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  functionality: Object,
  systems: Array,
});
const emit = defineEmits(["close", "save"]);

const form = ref({
  name: "",
  description: "",
  system: null, // Ensure correct system handling
});

// Watch for functionality changes
watch(
  () => props.functionality,
  (newFunctionality) => {
    if (newFunctionality) {
      form.value = {
        id: newFunctionality.id || null,
        name: newFunctionality.name || "",
        description: newFunctionality.description || "",
        system: newFunctionality.system?.id || null, // ✅ Ensure system is properly set
      };
    } else {
      form.value = { name: "", description: "", system: null };
    }
  },
  { immediate: true }
);

// Handle form submission
const handleSubmit = () => {
  emit("save", { ...form.value });
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
