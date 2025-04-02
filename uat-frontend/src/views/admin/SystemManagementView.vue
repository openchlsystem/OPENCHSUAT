<template>
  <div class="container">
    <h2>System Management</h2>

    <!-- Create System Button -->
    <button @click="openModal(null)" class="btn btn-primary mb-3">
      + Create System
    </button>

    <!-- System Table Component -->
    <SystemTable 
      :systems="systems"
      :organizations="organizations" 
      @edit="openModal" 
      @delete="deleteSystem" 
    />

    <!-- System Modal Component -->
    <SystemModal 
      v-if="showModal" 
      :system="selectedSystem" 
      :organizations="organizations" 
      @close="closeModal" 
      @save="saveSystem" 
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "@/utils/axios.js";
import SystemTable from "@/components/SystemTable.vue";
import SystemModal from "@/components/SystemModal.vue";

// Reactive state
const systems = ref([]);
const organizations = ref([]); // Holds organization list
const showModal = ref(false);
const selectedSystem = ref(null);

// Fetch Systems
const fetchSystems = async () => {
  try {
    const response = await api.get("/systems/");
    systems.value = response.data;
  } catch (error) {
    console.error("Error fetching systems:", error);
    if (error.response?.status === 401) {
      alert("Session expired. Please log in again.");
      window.location.href = "/login";
    }
  }
};

// Fetch Organizations
const fetchOrganizations = async () => {
  try {
    const response = await api.get("/organizations/");
    organizations.value = response.data;
  } catch (error) {
    console.error("Error fetching organizations:", error);
  }
};

// Open Modal for Create/Edit
const openModal = (system) => {
  selectedSystem.value = system
    ? { ...system }
    : { name: "", description: "", organization_id: null }; // Default values
  showModal.value = true;
};

// Close Modal
const closeModal = () => {
  showModal.value = false;
  selectedSystem.value = null;
};

// Save System (Create/Update)
const saveSystem = async (data) => {
  try {
    if (data.id) {
      await api.put(`/systems/${data.id}/`, data);
    } else {
      await api.post("/systems/", data);
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
      await api.delete(`/systems/${id}/`);
      fetchSystems();
    } catch (error) {
      console.error("Error deleting system:", error);
    }
  }
};

// Fetch data on mount
onMounted(() => {
  fetchSystems();
  fetchOrganizations();
});
</script>

<style scoped>
.container {
  max-width: 90%;
  margin: auto;
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
