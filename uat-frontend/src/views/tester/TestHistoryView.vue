<template>
  <div class="test-history-container">
    <h2 class="page-title"> Test Execution History</h2>

    <div class="filters">
      <input v-model="searchQuery" type="text" class="form-control" placeholder="🔍 Search by Test Case" />
      
      <select v-model="filterStatus" class="form-control">
        <option value="">Filter by Status</option>
        <option value="Passed">✅ Passed</option>
        <option value="Failed">❌ Failed</option>
      </select>

      <select v-model="sortOrder" class="form-control">
        <option value="desc">Sort by Date (Newest First)</option>
        <option value="asc">Sort by Date (Oldest First)</option>
      </select>
    </div>

    <TestHistoryTable :executions="filteredExecutions" :sortOrder="sortOrder" />
  </div>
</template>

<script>
import TestHistoryTable from "@/components/TestHistoryTable.vue";
import axios from "@/utils/axios";

export default {
  components: { TestHistoryTable },
  data() {
    return {
      executions: [],
      searchQuery: "",
      filterStatus: "",
      sortOrder: "desc",
    };
  },
  computed: {
    filteredExecutions() {
      let filtered = this.executions;

      // Search by test case name
      if (this.searchQuery) {
        filtered = filtered.filter(execution =>
          execution.test_case.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }

      // Filter by status
      if (this.filterStatus) {
        filtered = filtered.filter(execution => execution.status === this.filterStatus);
      }

      return filtered;
    }
  },
  async created() {
    await this.fetchTestHistory();
  },
  methods: {
    async fetchTestHistory() {
      try {
        const response = await axios.get("/test-executions");
        this.executions = response.data;
      } catch (error) {
        console.error("Error fetching test history:", error);
      }
    }
  }
};
</script>

<style scoped>
.test-history-container {
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.page-title {
  text-align: center;
  color: #ff6600;
  margin-bottom: 20px;
}

.filters {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.filters .form-control {
  flex: 1;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.filters select {
  background: white;
}

/* Responsive */
@media (max-width: 768px) {
  .filters {
    flex-direction: column;
  }
}
</style>
