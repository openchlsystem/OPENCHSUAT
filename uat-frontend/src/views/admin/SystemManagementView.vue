<template>
    <div class="container">
      <h2>System Management</h2>
  
      <!-- Add System Button -->
      <!--<button @click="openModal(null)">Add New System</button> -->
  
      <!-- System Table Component -->
      <SystemTable :systems="systems" @edit="openModal" @delete="deleteSystem" />
  
      <!-- System Modal Component -->
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
  
  const fetchSystems = async () => {
    try {
      const response = await axios.get("/api/systems/");
      systems.value = response.data;
    } catch (error) {
      console.error("Error fetching systems:", error);
    }
  };
  
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
  button {
    margin: 10px 0;
    padding: 8px 15px;
    border: none;
    cursor: pointer;
  }
  </style>
  