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

    <!-- Functionality Modal (conditionally rendered) -->
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
import axios from "@/utils/axios";
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
        const response = await axios.get("api/functionalities/");
        this.functionalities = response.data;
      } catch (error) {
        console.error("Error fetching functionalities:", error);
      }
    },
    async fetchSystems() {
      try {
        const response = await axios.get("api/systems/");
        this.systems = response.data;
      } catch (error) {
        console.error("Error fetching systems:", error);
      }
    },
    openCreateModal() {
      console.log("Opening Create Functionality Modal ✅"); // Debugging
      this.selectedFunctionality = { id: null, name: "", system: null, description: "" };
      this.showModal = true;
      this.$forceUpdate(); // Ensures Vue re-renders the modal
    },
    editFunctionality(functionality) {
      console.log("Editing Functionality ✅", functionality);
      this.selectedFunctionality = { ...functionality };
      this.showModal = true;
    },
    deleteFunctionality(id) {
      if (confirm("Are you sure you want to delete this functionality?")) {
        axios.delete(`/functionalities/${id}/`)
          .then(() => {
            this.functionalities = this.functionalities.filter(f => f.id !== id);
          })
          .catch(error => console.error("Error deleting functionality:", error));
      }
    },
    saveFunctionality(newFunctionality) {
      if (newFunctionality.id) {
        axios.put(`api/functionalities/${newFunctionality.id}/`, newFunctionality)
          .then(() => this.fetchFunctionalities())
          .catch(error => console.error("Error updating functionality:", error));
      } else {
        axios.post("api/functionalities/", newFunctionality)
          .then(() => this.fetchFunctionalities())
          .catch(error => console.error("Error creating functionality:", error));
      }
      this.closeModal();
    },
    closeModal() {
      console.log("Closing Modal ✅"); // Debugging
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
