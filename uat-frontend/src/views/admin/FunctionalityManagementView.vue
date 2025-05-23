<!-- FunctionalityManagementView.vue - Updated to use axiosInstance -->
<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2 class="mb-4">
        Functionality Management
        <span v-if="systemName" class="system-filter-label">({{ systemName }})</span>
      </h2>
      <div v-if="isSystemFiltered">
        <button @click="clearSystemFilter" class="btn btn-secondary">
          Show All Functionalities
        </button>
      </div>
    </div>

    <!-- Functionality Table -->
    <FunctionalityTable
      :functionalities="filteredFunctionalities"
      :systems="systems"
      @openModal="openCreateModal"
      @edit="editFunctionality"
      @delete="deleteFunctionality"
      @viewTestCases="navigateToTestCases"
    />
    
    <!-- Functionality Modal -->
    <FunctionalityModal
      v-if="showModal"
      :functionality="selectedFunctionality"
      :systems="systems"
      @close="closeModal"
      @save="saveFunctionality"
    />
  </div>
</template>

<script>
import axiosInstance from "@/utils/axios.js";
import FunctionalityTable from "@/components/FunctionalityTable.vue";
import FunctionalityModal from "@/components/FunctionalityModal.vue";

export default {
  components: {
    FunctionalityTable,
    FunctionalityModal,
  },
  
  data() {
    return {
      functionalities: [],
      systems: [],
      showModal: false,
      selectedFunctionality: null,
      systemId: null,
      systemName: "",
      isSystemFiltered: false
    };
  },
  
  computed: {
    // Filter functionalities by system ID
    filteredFunctionalities() {
      if (!this.isSystemFiltered) {
        return this.functionalities;
      }
      
      console.log(`Filtering functionalities for system ID: ${this.systemId}`);
      
      return this.functionalities.filter(functionality => {
        // Handle both possible data structures (system_id or system)
        const functionalitySystemId = 
          functionality.system_id !== undefined ? functionality.system_id :
          functionality.system !== undefined ? 
            (typeof functionality.system === 'object' ? functionality.system.id : functionality.system) :
          null;
        
        console.log(`Functionality: ${functionality.name}, System ID: ${functionalitySystemId}`);
        
        // Compare as strings to avoid type mismatches
        return String(functionalitySystemId) === String(this.systemId);
      });
    }
  },
  
  methods: {
    // Check URL for system_id parameter
    checkSystemFilter() {
      const urlParams = new URLSearchParams(window.location.search);
      const systemIdParam = urlParams.get('system_id');
      const systemNameParam = urlParams.get('system_name');
      
      if (systemIdParam) {
        this.systemId = parseInt(systemIdParam);
        this.systemName = systemNameParam || "";
        this.isSystemFiltered = true;
        console.log("System filter active:", this.systemId, this.systemName);
      }
    },
    
    // Clear system filter
    clearSystemFilter() {
      window.location.href = '/admin/functionalities';
    },
    
    async fetchFunctionalities() {
      try {
        const response = await axiosInstance.get("uat/functionalities/");
        this.functionalities = response.data;
        console.log(`Fetched ${this.functionalities.length} functionalities`);
      } catch (error) {
        console.error("Error fetching functionalities:", error);
      }
    },
    
    async fetchSystems() {
      try {
        const response = await axiosInstance.get("uat/systems/");
        this.systems = response.data;
        
        // If we have a system filter but no name, try to get it
        if (this.isSystemFiltered && !this.systemName) {
          const system = this.systems.find(s => s.id === this.systemId);
          if (system) {
            this.systemName = system.name;
          }
        }
      } catch (error) {
        console.error("Error fetching systems:", error);
      }
    },
    
    openCreateModal() {
      console.log("✅ Opening Create Modal");
      // If creating a new functionality with a system filter, pre-select that system
      this.selectedFunctionality = { 
        id: null, 
        name: "", 
        description: "", 
        system: this.isSystemFiltered ? this.systemId : null 
      };
      this.showModal = true;
      this.$nextTick(() => this.$forceUpdate()); // Ensures reactivity update
    },
    
    editFunctionality(functionality) {
      console.log("✅ Editing Functionality", functionality);
      this.selectedFunctionality = { ...functionality };
      this.showModal = true;
    },
    
    async deleteFunctionality(id) {
      if (confirm("Are you sure you want to delete this functionality?")) {
        try {
          await axiosInstance.delete(`uat/functionalities/${id}/`);
          this.functionalities = this.functionalities.filter((f) => f.id !== id);
        } catch (error) {
          console.error("Error deleting functionality:", error);
        }
      }
    },
    
    async saveFunctionality(newFunctionality) {
      try {
        if (newFunctionality.id) {
          await axiosInstance.put(`uat/functionalities/${newFunctionality.id}/`, newFunctionality);
        } else {
          await axiosInstance.post("uat/functionalities/", newFunctionality);
        }
        this.fetchFunctionalities();
        this.closeModal();
      } catch (error) {
        console.error("Error saving functionality:", error);
      }
    },
    
    closeModal() {
      console.log("✅ Closing Modal");
      this.selectedFunctionality = null;
      this.showModal = false;
    },
    
    navigateToTestCases(functionality) {
      // Navigate to test cases view with functionality id as parameter
      this.$router.push({
        name: 'FunctionalityTestCases',
        params: {
          functionalityId: functionality.id
        },
        query: {
          functionalityName: functionality.name
        }
      });
    }
  },
  
  mounted() {
    // First check if we're filtering by system
    this.checkSystemFilter();
    
    // Then fetch functionalities and systems
    this.fetchFunctionalities();
    this.fetchSystems();
  }
};
</script>

<style scoped>
.system-filter-label {
  font-size: 0.8em;
  color: #6c757d;
  font-weight: normal;
  margin-left: 10px;
}
</style>