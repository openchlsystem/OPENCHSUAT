<template>
  <div class="container">
    <h2>System Management</h2>

    <SystemTable
      :systems="systems"
      :organizations="organizations"
      @edit="openModal"
      @delete="deleteSystem"
    />

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
import axios from "axios";
import SystemTable from "@/components/SystemTable.vue";
import SystemModal from "@/components/SystemModal.vue";

const systems = ref([]);
const organizations = ref([]);
const showModal = ref(false);
const selectedSystem = ref(null);

// Fetch systems from the backend
const fetchSystems = async () => {
  try {
    const response = await axios.get("/systems/");
    // Create a new array instance to trigger reactivity
    systems.value = [...response.data];
  } catch (error) {
    console.error("Error fetching systems:", error);
  }
};

// Fetch organizations from the backend
const fetchOrganizations = async () => {
  try {
    const response = await axios.get("/organizations/");
    organizations.value = response.data;
  } catch (error) {
    console.error("Error fetching organizations:", error);
  }
};

// Fetch systems and organizations when the component is mounted
onMounted(() => {
  fetchSystems();
  fetchOrganizations();
});

const openModal = (system) => {
  selectedSystem.value = system;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  selectedSystem.value = null;
};

const saveSystem = async (data) => {
  try {
    if (data.id) {
      await axios.put(`/systems/${data.id}/`, data);
    } else {
      await axios.post("/systems/", data);
    }
    fetchSystems();
    closeModal();
  } catch (error) {
    console.error("Error saving system:", error);
  }
};

const deleteSystem = async (id) => {
  if (confirm("Are you sure you want to delete this system?")) {
    try {
      await axios.delete(`/systems/${id}/`);
      fetchSystems();
    } catch (error) {
      console.error("Error deleting system:", error);
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 90%;
  margin: auto;
}
button {
  margin: 10px 0;
  padding: 8px 15px;
  border: none;
  cursor: pointer;
}
</style>