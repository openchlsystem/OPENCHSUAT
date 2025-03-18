<template>
  <div class="container">
    <h2>System Management</h2>

    <!-- Add System Button -->
    <button class="btn btn-primary mb-3" @click="openModal(null)">+ Add System</button>

    <!-- System Table -->
    <SystemTable :systems="systems" @edit="openModal" @delete="deleteSystem" />

    <!-- System Modal -->
    <SystemModal 
      v-if="showModal" 
      :system="selectedSystem" 
      @close="closeModal" 
      @save="saveSystem" 
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import SystemTable from "@/components/SystemTable.vue";
import SystemModal from "@/components/SystemModal.vue";

const systems = ref([]);
const showModal = ref(false);
const selectedSystem = ref(null);

// Fetch Systems
const fetchSystems = async () => {
  try {
    const response = await axios.get("/api/systems/");
    systems.value = response.data;
  } catch (error) {
    console.error("Error fetching systems:", error);
  }
};

// Open Modal for Add/Edit
const openModal = (system = null) => {
  selectedSystem.value = system;
  showModal.value = true;
};

// Close Modal
const closeModal = () => {
  showModal.value = false;
  selectedSystem.value = null;
};

// Save System (Create/Edit)
const saveSystem = async (data) => {
  try {
    if (data.id) {
      await axios.put(`/api/systems/${data.id}/`, data);
    } else {
      await axios.post("/api/systems/", data);
    }
    fetchSystems();
    closeModal();
  } catch (error) {
    console.error("Error saving system:", error);
  }
};

// Delete System
const deleteSystem = async (id) => {
  if (confirm("Are you sure you want to delete this system?")) {
    try {
      await axios.delete(`/api/systems/${id}/`);
      fetchSystems();
    } catch (error) {
      console.error("Error deleting system:", error);
    }
  }
};

onMounted(fetchSystems);
</script>

<style scoped>
.container {
  max-width: 90%;
  margin: auto;
}
</style>
