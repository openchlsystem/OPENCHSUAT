<template>
  <div class="container mt-4">
    <h2 class="mb-4 text-center text-success">Test Execution History</h2>
    
    <div v-if="loading" class="loading-spinner">
      <div class="spinner-border text-success" role="status">
        <span class="sr-only">Loading...</span>
      </div>
    </div>
    
    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>
    
    <div v-else class="test-history-container">
      <TestHistoryTable :executions="executions" />
    </div>
  </div>
</template>

<script>
import TestHistoryTable from "@/components/TestHistoryTable.vue";
import axiosInstance from "@/utils/axios.js";

export default {
  components: { TestHistoryTable },
  data() {
    return {
      executions: [],
      loading: false,
      error: null
    };
  },
  async created() {
    await this.fetchTestHistory();
  },
  methods: {
    async fetchTestHistory() {
      this.loading = true;
      try {
        // Try to fetch from test-history endpoint first
        let response;
        try {
          response = await axiosInstance.get("uat/test-history/");
        } catch (historyError) {
          console.log("History endpoint not available, fetching from test-executions");
          // If that fails, fall back to test-executions endpoint
          response = await axiosInstance.get("uat/test-executions/");
        }
        
        this.executions = response.data;
        
        // If the response is empty, try the executions endpoint
        if (!this.executions || this.executions.length === 0) {
          try {
            const executionsResponse = await axiosInstance.get("uat/test-executions/executions/");
            this.executions = executionsResponse.data;
          } catch (executionsError) {
            console.error("Error fetching from executions endpoint:", executionsError);
          }
        }
      } catch (error) {
        console.error("Error fetching test history:", error);
        this.error = "Failed to load test execution history.";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.container {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #28a745; /* Green text */
  font-weight: bold;
}

.test-history-container {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.loading-spinner {
  display: flex;
  justify-content: center;
  padding: 40px;
}

.spinner-border {
  display: inline-block;
  width: 2rem;
  height: 2rem;
  vertical-align: text-bottom;
  border: 0.25em solid #28a745; /* Green spinner */
  border-right-color: transparent;
  border-radius: 50%;
  animation: spinner-border 0.75s linear infinite;
}

@keyframes spinner-border {
  to {
    transform: rotate(360deg);
  }
}

.error-message {
  color: #dc3545;
  text-align: center;
  padding: 20px;
  background: #f8d7da;
  border-radius: 5px;
  margin-top: 20px;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.mt-4 {
  margin-top: 1.5rem;
}

.mb-4 {
  margin-bottom: 1.5rem;
}

.text-center {
  text-align: center;
}

.text-success {
  color: #28a745 !important;
}
</style>