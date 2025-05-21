<template>
  <div class="container mt-4">
    <h2 class="mb-4 text-center text-success">Test Execution</h2>

    <div v-if="loading" class="loading-spinner">
      <div class="spinner-border text-success" role="status">
        <span class="sr-only">Loading...</span>
      </div>
    </div>

    <div v-else>
      <TestExecutionTable 
        :testExecutions="testExecutions"
        :loading="loading"
        @execute="openExecutionModal"
      />
    </div>

    <!-- Execution Modal -->
    <TestExecutionModal
      v-if="showModal"
      :execution="selectedExecution"
      @close="closeModal"
      @save="submitExecution"
    />
  </div>
</template>

<script>
import axiosInstance from "@/utils/axios.js";;
import TestExecutionTable from "@/components/TestExecutionTable.vue";
import TestExecutionModal from "@/components/TestExecutionModal.vue";

export default {
  components: {
    TestExecutionTable,
    TestExecutionModal
  },
  data() {
    return {
      testExecutions: [],
      selectedExecution: null,
      showModal: false,
      loading: false,
      executedTestIds: new Set(),  // Track which tests have been executed
      statusMap: {}  // Map test IDs to their execution status
    };
  },
  mounted() {
    this.fetchTestExecutions();
  },
  methods: {
    // Helper method to parse test cases from various formats
    parseTestCase(testCase) {
      if (typeof testCase === 'string') {
        try {
          // Try to parse as JSON
          const parsed = JSON.parse(testCase);
          return {
            ...parsed,
            status: parsed.status || 'pending'
          };
        } catch (e) {
          // If parsing fails, create a simple object
          return {
            id: typeof testCase === 'number' ? testCase : 0,
            title: testCase,
            status: 'pending'
          };
        }
      }
      
      // If it's already an object
      if (testCase && typeof testCase === 'object') {
        // If the test is in our executed set, mark it as completed
        if (testCase.id && this.executedTestIds.has(testCase.id)) {
          return {
            ...testCase,
            status: this.statusMap[testCase.id] || 'completed'
          };
        }
        
        return {
          ...testCase,
          status: testCase.status || 'pending'
        };
      }
      
      // Default fallback
      return {
        id: 0,
        title: 'Unknown Test',
        status: 'pending'
      };
    },
    
    async fetchTestExecutions() {
      this.loading = true;
      try {
        // First, fetch executed test cases from history to build our executed tests set
        await this.fetchExecutedTests();
        
        // Then fetch test cases
        const response = await axiosInstance.get("uat/test-cases/");
        
        // Process test cases to ensure proper data format
        let testCases = Array.isArray(response.data) 
          ? response.data.map(testCase => this.parseTestCase(testCase))
          : [];
        
        // Update test case statuses based on execution history
        testCases = testCases.map(testCase => {
          if (testCase.id && this.executedTestIds.has(testCase.id)) {
            return {
              ...testCase,
              status: this.statusMap[testCase.id] || 'completed'  // Use status from map if available, otherwise 'completed'
            };
          }
          return {
            ...testCase,
            status: testCase.status || 'pending'
          };
        });
        
        // Log for debugging
        console.log("Final testCases with updated statuses:", testCases);
        
        this.testExecutions = testCases;
      } catch (error) {
        console.error("Error fetching test executions:", error.response?.data || error.message);
      } finally {
        this.loading = false;
      }
    },
    
    // Method to fetch executed tests from both history and executions endpoints
    async fetchExecutedTests() {
      this.executedTestIds.clear(); // Reset the set
      this.statusMap = {}; // Reset the status map
      
      // First try test-history endpoint
      try {
        const historyResponse = await axiosInstance.get("uat/test-history/");
        console.log("Test history response:", historyResponse.data);
        
        if (Array.isArray(historyResponse.data) && historyResponse.data.length > 0) {
          historyResponse.data.forEach(historyItem => {
            this.processExecutedTest(historyItem);
          });
        }
      } catch (historyError) {
        console.log("Could not fetch from test-history endpoint:", historyError.message);
      }
      
      // Then try test-executions endpoint
      try {
        const executionsResponse = await axiosInstance.get("uat/test-executions/");
        console.log("Test executions response:", executionsResponse.data);
        
        if (Array.isArray(executionsResponse.data) && executionsResponse.data.length > 0) {
          executionsResponse.data.forEach(execution => {
            this.processExecutedTest(execution);
          });
        }
      } catch (executionsError) {
        console.log("Could not fetch from test-executions endpoint:", executionsError.message);
      }
      
      // Finally try test-executions/executions/ endpoint
      try {
        const executionsAltResponse = await axiosInstance.get("uat/test-executions/executions/");
        console.log("Test executions/executions response:", executionsAltResponse.data);
        
        if (Array.isArray(executionsAltResponse.data) && executionsAltResponse.data.length > 0) {
          executionsAltResponse.data.forEach(execution => {
            this.processExecutedTest(execution);
          });
        }
      } catch (executionsAltError) {
        console.log("Could not fetch from test-executions/executions endpoint:", executionsAltError.message);
      }
      
      console.log(`Found ${this.executedTestIds.size} executed test IDs:`, [...this.executedTestIds]);
      console.log("Status map:", this.statusMap);
    },
    
    // Helper method to process executed test data
    processExecutedTest(execution) {
      if (!execution) return;
      
      let testCaseId = null;
      let status = execution.status || 'completed';
      
      // Handle different data structures
      if (execution.test_case) {
        if (typeof execution.test_case === 'object' && execution.test_case.id) {
          testCaseId = execution.test_case.id;
        } else if (typeof execution.test_case === 'number') {
          testCaseId = execution.test_case;
        } else if (typeof execution.test_case === 'string' && !isNaN(parseInt(execution.test_case))) {
          testCaseId = parseInt(execution.test_case);
        }
      }
      
      // If we found a valid test case ID, add it to our set and map
      if (testCaseId !== null) {
        this.executedTestIds.add(testCaseId);
        this.statusMap[testCaseId] = status;
      }
    },
    
    openExecutionModal(execution) {
      // Create a deep copy of the execution to avoid modifying the original
      let executionCopy;
      
      try {
        executionCopy = JSON.parse(JSON.stringify(execution));
      } catch (e) {
        // If stringification fails, create a new object
        executionCopy = { ...execution };
      }
      
      // If the execution is a string, parse it
      if (typeof executionCopy === 'string') {
        try {
          this.selectedExecution = JSON.parse(executionCopy);
        } catch (e) {
          this.selectedExecution = { 
            id: 0, 
            title: executionCopy,
            status: 'pending'
          };
        }
      } else {
        this.selectedExecution = executionCopy;
      }
      
      // Ensure we have proper default values
      if (!this.selectedExecution.status) {
        this.selectedExecution.status = 'pending';
      }
      
      if (!this.selectedExecution.steps) {
        this.selectedExecution.steps = [];
      }
      
      this.showModal = true;
    },
    
    closeModal() {
      this.showModal = false;
      this.selectedExecution = null;
      this.fetchTestExecutions(); // Refresh the list completely
    },
    
    async submitExecution({ executionId, steps, status, notes }) {
      try {
        // Ensure we have a valid execution ID
        if (!executionId && this.selectedExecution) {
          executionId = this.selectedExecution.id;
        }
        
        if (!executionId) {
          console.error("No execution ID provided");
          return;
        }
        
        // Prepare payload
        const payload = {
          test_case: executionId,
          steps: steps || [],
          status: status || 'completed', // Default to 'completed'
          notes: notes || '',
          completed_at: new Date().toISOString()
        };
        
        console.log("Submitting execution with payload:", payload);
        
        // Submit the execution
        const response = await axiosInstance.post(`uat/test-executions/`, payload);
        console.log("Execution submitted successfully:", response.data);
        
        // Update local state immediately
        this.executedTestIds.add(executionId);
        this.statusMap[executionId] = status || 'completed';
        
        // Update the test case in the list
        const testCaseIndex = this.testExecutions.findIndex(test => test.id === executionId);
        if (testCaseIndex !== -1) {
          // Create a new object to ensure Vue reactivity
          const updatedTestCases = [...this.testExecutions];
          updatedTestCases[testCaseIndex] = {
            ...updatedTestCases[testCaseIndex],
            status: status || 'completed'
          };
          this.testExecutions = updatedTestCases;
        }
        
        // Show success message if toast functionality is available
        if (this.$toast) {
          this.$toast.success("Test execution submitted successfully");
        } else if (window.alert) {
          window.alert("Test execution submitted successfully");
        }
        
        // Close modal and refresh to ensure we have the latest data
        this.closeModal();
      } catch (error) {
        console.error("Error submitting execution:", error);
        if (this.$toast) {
          this.$toast.error("Failed to submit test execution");
        } else if (window.alert) {
          window.alert("Failed to submit test execution");
        }
      }
    },
  },
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

.text-success {
  color: #28a745 !important;
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
  border: 0.25em solid #28a745;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spinner-border 0.75s linear infinite;
}

@keyframes spinner-border {
  to {
    transform: rotate(360deg);
  }
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
</style>