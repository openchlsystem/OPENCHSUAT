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
import axios from "axios";
import OrganizationTable from "@/components/admin/OrganizationTable.vue";
import OrganizationModal from "@/components/admin/OrganizationModal.vue";

const organizations = ref([]);
const showModal = ref(false);
const selectedOrganization = ref(null);

// Fetch Organizations
const fetchOrganizations = async () => {
  try {
    const response = await axios.get("/organizations");
    organizations.value = response.data;
  } catch (error) {
    console.error("Error fetching organizations:", error);
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
      // Update existing organization
      await axios.put(`/organizations/${data.id}/`, data);
    } else {
      // Create new organization
      await axios.post("/organizations/", data);
    }
    fetchOrganizations(); // Refresh after save
    closeModal();
  } catch (error) {
    console.error("Error saving organization:", error);
  }
};

// Delete Organization
const deleteOrganization = async (id) => {
  if (confirm("Are you sure you want to delete this organization?")) {
    try {
      await axios.delete(`organizations/${id}/`);
      fetchOrganizations(); // Refresh after delete
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
