<template>
  <div class="test-history-container">
    <h2 class="page-title"> Test Execution History</h2>

    <TestHistoryTable :executions="executions" />
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
    };
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
</style>
