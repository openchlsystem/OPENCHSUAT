<template>
  <div class="container mt-4">
    <h2 class="mb-4">Functionality Management</h2>

    <!-- Functionality Table -->
    <FunctionalityTable 
      :functionalities="functionalities" 
      @openModal="openCreateModal"
      @edit="editFunctionality"
      @delete="deleteFunctionality"
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
import axios from "@/utils/axios.js";
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
    };
  },
  methods: {
    async fetchFunctionalities() {
      try {
        const response = await axios.get("/functionalities/");
        this.functionalities = response.data;
      } catch (error) {
        console.error("Error fetching functionalities:", error);
      }
    },

    async fetchSystems() {
      try {
        const response = await axios.get("/systems/");
        this.systems = response.data;
      } catch (error) {
        console.error("Error fetching systems:", error);
      }
    },

    // ✅ FIXED: Opening modal properly
    openCreateModal() {
      console.log("✅ Opening Create Modal");
      this.selectedFunctionality = { id: null, name: "", description: "", system: null };
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
          await axios.delete(`/functionalities/${id}/`);
          this.functionalities = this.functionalities.filter((f) => f.id !== id);
        } catch (error) {
          console.error("Error deleting functionality:", error);
        }
      }
    },

    async saveFunctionality(newFunctionality) {
      try {
        if (newFunctionality.id) {
          await axios.put(`/functionalities/${newFunctionality.id}/`, newFunctionality);
        } else {
          await axios.post("/functionalities/", newFunctionality);
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
    }
  },
  mounted() {
    this.fetchFunctionalities();
    this.fetchSystems();
  }
};
</script>
