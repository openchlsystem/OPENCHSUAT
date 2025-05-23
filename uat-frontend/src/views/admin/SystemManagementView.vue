<!-- SystemManagement.vue - Client-side Filtering -->
<template>
  <div class="container">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2>
        System Management
        <span v-if="orgName" class="org-filter-label">({{ orgName }})</span>
      </h2>
      <div>
        <button v-if="isOrgFiltered" @click="clearOrgFilter" class="btn btn-secondary me-2">
          Show All Systems
        </button>
        <button @click="openModal(null)" class="btn btn-primary">
          + Create System
        </button>
      </div>
    </div>
    
    <!-- System Table Component -->
    <SystemTable
      :systems="filteredSystems"
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
import { ref, onMounted, computed } from "vue";
import axiosInstance from "@/utils/axios.js";
import SystemTable from "@/components/SystemTable.vue";
import SystemModal from "@/components/SystemModal.vue";

// Reactive state
const systems = ref([]);
const organizations = ref([]);
const showModal = ref(false);
const selectedSystem = ref(null);

// Organization filtering
const orgId = ref(null);
const orgName = ref('');
const isOrgFiltered = ref(false);

// Computed property for client-side filtered systems
const filteredSystems = computed(() => {
  if (!isOrgFiltered.value) {
    return systems.value;
  }
  
  console.log(`Filtering systems for organization ID: ${orgId.value}`);
  console.log('All systems:', systems.value);
  
  // Client-side filtering - look for systems with matching organization
  return systems.value.filter(system => {
    // Compare either directly on organization_id or through the organization field
    const systemOrgId = 
      (system.organization_id !== undefined) ? system.organization_id : 
      (system.organization !== undefined) ? 
        (typeof system.organization === 'object' ? system.organization.id : system.organization) :
      null;
    
    console.log(`System: ${system.name}, Organization ID: ${systemOrgId}`);
    
    // Compare as strings to avoid type mismatches
    return String(systemOrgId) === String(orgId.value);
  });
});

// Fetch all Systems
const fetchSystems = async () => {
  try {
    // Fetch all systems regardless of filter - we'll filter client-side
    const response = await axiosInstance.get("uat/systems/");
    systems.value = response.data;
    console.log(`Fetched ${systems.value.length} systems`);
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
    const response = await axiosInstance.get("uat/organizations/");
    organizations.value = response.data;
    
    // If organization filter is active, get the organization name
    if (isOrgFiltered.value) {
      const org = organizations.value.find(o => {
        return String(o.id) === String(orgId.value);
      });
      
      if (org) {
        orgName.value = org.name;
        console.log(`Found organization: ${org.name}`);
      } else {
        // If org not found in list, fetch it individually
        await fetchOrgName();
      }
    }
  } catch (error) {
    console.error("Error fetching organizations:", error);
  }
};

// Fetch organization name by ID
const fetchOrgName = async () => {
  if (!orgId.value) return;
  
  try {
    const response = await axiosInstance.get(`uat/organizations/${orgId.value}/`);
    if (response.data) {
      orgName.value = response.data.name;
      console.log(`Fetched organization name: ${orgName.value}`);
    }
  } catch (error) {
    console.error("Error fetching organization name:", error);
  }
};

// Check for organization filter in URL
const checkOrgFilter = () => {
  const urlParams = new URLSearchParams(window.location.search);
  const orgIdParam = urlParams.get('org_id');
  
  if (orgIdParam) {
    orgId.value = parseInt(orgIdParam);
    isOrgFiltered.value = true;
    console.log("Organization filter active:", orgId.value);
  }
};

// Clear organization filter
const clearOrgFilter = () => {
  window.location.href = '/admin/systems';
};

// Open Modal for Create/Edit
const openModal = (system) => {
  if (system) {
    selectedSystem.value = { ...system };
  } else {
    // If creating a new system and we have an org filter, pre-select that organization
    selectedSystem.value = { 
      name: "", 
      description: "", 
      organization_id: isOrgFiltered.value ? orgId.value : null 
    };
  }
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
      await axiosInstance.put(`uat/systems/${data.id}/`, data);
    } else {
      await axiosInstance.post("uat/systems/", data);
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
<<<<<<< HEAD
      await axiosInstance.delete(`uat/systems/${id}/`);
=======
      await axiosInstance.deletuate(`/systems/${id}/`);
>>>>>>> nelson
      fetchSystems();
    } catch (error) {
      console.error("Error deleting system:", error);
    }
  }
};

// Fetch data on mount
onMounted(() => {
  // First check if we're filtering by organization
  checkOrgFilter();
  
  // Then fetch systems and organizations
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
.org-filter-label {
  font-size: 0.8em;
  color: #6c757d;
  font-weight: normal;
  margin-left: 10px;
}
</style>