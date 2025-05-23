<!-- src/components/admin/DefectFilter.vue -->
<template>
    <div class="filter-container">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search by defect name..."
        @input="applyFilters"
      />
  
      <select v-model="selectedSeverity" @change="applyFilters">
        <option value="">All Severities</option>
        <option value="Critical">Critical</option>
        <option value="High">High</option>
        <option value="Medium">Medium</option>
        <option value="Low">Low</option>
      </select>
  
      <select v-model="selectedStatus" @change="applyFilters">
        <option value="">All Status</option>
        <option value="Open">Open</option>
        <option value="InProgress">In Progress</option>
        <option value="Resolved">Resolved</option>
        <option value="Closed">Closed</option>
      </select>
  
      <input type="date" v-model="startDate" @change="applyFilters" />
      <input type="date" v-model="endDate" @change="applyFilters" />
  
      <button class="btn-reset" @click="resetFilters">Reset</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        searchQuery: "",
        selectedSeverity: "",
        selectedStatus: "",
        startDate: "",
        endDate: "",
      };
    },
    methods: {
      applyFilters() {
        this.$emit("filter-updated", {
          searchQuery: this.searchQuery,
          selectedSeverity: this.selectedSeverity,
          selectedStatus: this.selectedStatus,
          startDate: this.startDate,
          endDate: this.endDate,
        });
      },
      resetFilters() {
        this.searchQuery = "";
        this.selectedSeverity = "";
        this.selectedStatus = "";
        this.startDate = "";
        this.endDate = "";
        this.applyFilters();
      },
    },
  };
  </script>
  
  <style scoped>
  .filter-container {
    display: flex;
    gap: 10px;
    align-items: center;
    margin-bottom: 15px;
  }
  
  input, select {
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .btn-reset {
    background: #ff6600; /* Theme color - Orange */
    color: white;
    padding: 8px 12px;
    border: none;
    cursor: pointer;
  }
  </style>
  