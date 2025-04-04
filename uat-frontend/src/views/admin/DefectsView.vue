<!-- src/views/admin/DefectsView.vue -->
<template>
  <div class="container">
    <h2 class="page-title">Reported Defects</h2>

    <!-- Filters & Search -->
    <DefectFilter @filter-updated="applyFilters" />

    <!-- Defects Table -->
    <DefectTable 
      :defects="filteredDefects" 
      @view-details="openDefectModal" 
    />

    <!-- Defect Details Modal -->
    <DefectDetailModal 
      v-if="selectedDefect" 
      :defect="selectedDefect" 
      @close="selectedDefect = null" 
    />
  </div>
</template>

<script>
import axios from "@/utils/axios.js";
import DefectTable from "@/components/Admin/DefectTable.vue";
import DefectFilter from "@/components/Admin/DefectFilter.vue";
import DefectDetailModal from "@/components/Admin/DefectDetailModal.vue";

export default {
  components: { DefectTable, DefectFilter, DefectDetailModal },
  data() {
    return {
      defects: [],
      filteredDefects: [],
      selectedDefect: null,
    };
  },
  methods: {
    fetchDefects() {
      axios.get("/defects")
        .then(response => {
          this.defects = response.data;
          this.filteredDefects = response.data;
        })
        .catch(error => console.error("Error fetching defects:", error));
    },
    applyFilters(filtered) {
      this.filteredDefects = filtered;
    },
    openDefectModal(defect) {
      this.selectedDefect = defect;
    }
  },
  created() {
    this.fetchDefects();
  }
};
</script>

<style scoped>
.container {
  padding: 20px;
}

.page-title {
  color: #ff6600; /* Theme color - Orange */
  font-size: 24px;
  margin-bottom: 15px;
}
</style>
