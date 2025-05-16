<!-- OrganizationManagement.vue -->
<template>
  <div class="container">
    <h2>Organization Management</h2>
    <!-- Create Organization Button -->
    <button @click="openModal(null)" class="btn btn-primary mb-3">
      + Create Organization
    </button>
    <!-- Organization Table Component -->
    <OrganizationTable
      :organizations="organizations"
      @edit="openModal"
      @delete="deleteOrganization"
    />
    <!-- Organization Modal Component -->
    <OrganizationModal
      v-if="showModal"
      :organization="selectedOrganization"
      @close="closeModal"
      @save="saveOrganization"
    />
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import api from "@/utils/axios.js"; // Import global Axios instance
import OrganizationTable from "@/components/Admin/OrganizationTable.vue";
import OrganizationModal from "@/components/Admin/OrganizationModal.vue";
// Reactive state
const organizations = ref([]);
const showModal = ref(false);
const selectedOrganization = ref(null);
// Fetch Organizations
const fetchOrganizations = async () => {
  try {
    const response = await api.get("/organizations/");
    organizations.value = response.data;
  } catch (error) {
    console.error("Error fetching organizations:", error);
    if (error.response && error.response.status === 401) {
      alert("Session expired. Please log in again.");
      window.location.href = "/login"; // Redirect to login
    }
  }
};
// Open Modal for Create/Edit
const openModal = (organization) => {
  selectedOrganization.value = organization;
  showModal.value = true;
};
// Close Modal
const closeModal = () => {
  showModal.value = false;
  selectedOrganization.value = null;
};
// Save Organization (Create/Update)
const saveOrganization = async (data) => {
  try {
    if (data.id) {
      await api.put(`/organizations/${data.id}/`, data);
    } else {
      await api.post("/organizations/", data);
    }
    fetchOrganizations(); // Refresh list
    closeModal();
  } catch (error) {
    console.error("Error saving organization:", error);
  }
};
// Delete Organization
const deleteOrganization = async (id) => {
  if (confirm("Are you sure you want to delete this organization?")) {
    try {
      await api.delete(`/organizations/${id}/`);
      fetchOrganizations(); // Refresh list
    } catch (error) {
      console.error("Error deleting organization:", error);
    }
  }
};
// Fetch organizations on mount
onMounted(fetchOrganizations);
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