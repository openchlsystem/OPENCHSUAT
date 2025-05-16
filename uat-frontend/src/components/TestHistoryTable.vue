<template>
  <div>
    <div class="filters">
      <div class="date-filters">
        <label>Filter by Date:</label>
        <input
          type="date"
          v-model="filterStartDate"
          class="filter-input"
          placeholder="Start Date"
        />
        <input
          type="date"
          v-model="filterEndDate"
          class="filter-input"
          placeholder="End Date"
        />
      </div>
    </div>

    <table v-if="filteredExecutions.length > 0" class="table">
      <thead>
        <tr>
          <th @click="sortBy('test_case')">Test Case</th>
          <th @click="sortBy('started_at')">Execution Date</th>
          <th>Comments</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="execution in filteredExecutions" :key="execution.id">
          <td>{{ getTestCaseTitle(execution) }}</td>
          <td>{{ formatDate(execution.started_at || execution.completed_at) }}</td>
          <td>{{ execution.notes || "No comments" }}</td>
          <td>
            <button class="btn btn-success btn-sm" @click="viewSteps(execution)">
              View Details
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else class="no-data-message">No test executions found.</p>

    <!-- Step Details Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h3 class="modal-title text-center text-success">Test Execution Details</h3>
        
        <div class="test-info">
          <h4>{{ getTestCaseTitle(selectedExecution) }}</h4>
          <p><strong>Execution Date:</strong> {{ formatDate(selectedExecution.started_at || selectedExecution.completed_at, true) }}</p>
        </div>
        
        <div class="notes-section" v-if="selectedExecution.notes">
          <h5>Notes</h5>
          <div class="notes-content">{{ selectedExecution.notes }}</div>
        </div>
        
        <div class="steps-section" v-if="hasSteps">
          <h5>Test Steps</h5>
          <div class="step-item" v-for="(step, idx) in stepsList" :key="idx">
            <div class="step-header">
              <span class="step-number">Step {{ step.step_number }}:</span>
              <span class="step-desc">{{ step.description }}</span>
              <span :class="getStepStatusClass(step.status)" class="step-status">
                {{ formatStepStatus(step.status) }}
              </span>
            </div>
            <div class="step-detail" v-if="step.expected_result">
              <em>Expected Result: {{ step.expected_result }}</em>
            </div>
            <div class="step-notes" v-if="step.notes">
              <strong>Notes:</strong> {{ step.notes }}
            </div>
          </div>
        </div>
        
        <div v-else class="alert alert-info">
          No step information available for this execution.
        </div>
        
        <div class="modal-footer">
          <button type="button" class="btn btn-success" @click="closeModal">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/utils/axios";

export default {
  props: {
    executions: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      filterStartDate: "",
      filterEndDate: "",
      sortField: "started_at",
      sortOrder: "desc",
      testCaseCache: {},
      showModal: false,
      selectedExecution: null,
      stepsList: []
    };
  },
  computed: {
    filteredExecutions() {
      let result = [...this.executions];
      
      // Apply date filters
      if (this.filterStartDate || this.filterEndDate) {
        result = result.filter(execution => {
          const executionDate = new Date(execution.started_at || execution.completed_at);
          const startDate = this.filterStartDate ? new Date(this.filterStartDate) : null;
          const endDate = this.filterEndDate ? new Date(this.filterEndDate) : null;
          
          // Add one day to end date to include the selected date
          if (endDate) {
            endDate.setDate(endDate.getDate() + 1);
          }

          return (!startDate || executionDate >= startDate) && 
                 (!endDate || executionDate <= endDate);
        });
      }
      
      // Sort results
      result.sort((a, b) => {
        const dateA = new Date(a[this.sortField] || a.completed_at || a.started_at);
        const dateB = new Date(b[this.sortField] || b.completed_at || b.started_at);
        return this.sortOrder === "asc" ? dateA - dateB : dateB - dateA;
      });
      
      return result;
    },
    hasSteps() {
      return this.stepsList && this.stepsList.length > 0;
    }
  },
  watch: {
    executions: {
      immediate: true,
      handler(newExecutions) {
        if (newExecutions && newExecutions.length > 0) {
          this.prefetchTestCases(newExecutions);
        }
      }
    }
  },
  methods: {
    prefetchTestCases(executions) {
      // Get unique test case IDs
      const testCaseIds = [...new Set(executions.map(execution => {
        // Handle different data structures
        if (execution.test_case && typeof execution.test_case === 'object') {
          return execution.test_case.id;
        }
        return execution.test_case;
      }))];
      
      // Fetch each test case
      testCaseIds.forEach(id => {
        if (id && !this.testCaseCache[id]) {
          this.fetchTestCase(id);
        }
      });
    },
    
    async fetchTestCase(id) {
      if (!id) return;
      
      try {
        // Set a placeholder to avoid multiple fetches
        this.testCaseCache[id] = { title: "Loading..." };
        
        const response = await axios.get(`/test-cases/${id}/`);
        const testCase = response.data;
        
        // Store in cache
        this.testCaseCache[id] = testCase;
      } catch (error) {
        console.error(`Error fetching test case ${id}:`, error);
        this.testCaseCache[id] = { title: "Unknown Test" };
      }
    },
    
    getTestCaseTitle(execution) {
      if (!execution) return "Unknown Test";
      
      let testCaseId;
      let testCaseObj;
      
      // Handle various data structures
      if (execution.test_case) {
        if (typeof execution.test_case === 'object') {
          testCaseObj = execution.test_case;
          testCaseId = execution.test_case.id;
        } else {
          testCaseId = execution.test_case;
        }
      }
      
      // If we have the object directly
      if (testCaseObj) {
        return this.extractTitle(testCaseObj);
      }
      
      // Check cache
      if (testCaseId && this.testCaseCache[testCaseId]) {
        return this.extractTitle(this.testCaseCache[testCaseId]);
      }
      
      // If not in cache, trigger fetch and return placeholder
      if (testCaseId) {
        this.fetchTestCase(testCaseId);
        return "Loading...";
      }
      
      return "Unknown Test";
    },
    
    extractTitle(testCase) {
      if (!testCase) return "Unknown Test";
      
      if (typeof testCase === 'string') {
        return testCase;
      }
      
      if (testCase.title) {
        if (typeof testCase.title === 'string') {
          return testCase.title;
        }
        if (typeof testCase.title === 'object' && testCase.title.name) {
          return testCase.title.name;
        }
      }
      
      if (testCase.name) {
        return testCase.name;
      }
      
      return "Unknown Test";
    },
    
    formatDate(date, includeTime = false) {
      if (!date) return "Unknown";
      
      const dateObj = new Date(date);
      
      if (includeTime) {
        return dateObj.toLocaleString();
      }
      
      return dateObj.toLocaleDateString();
    },
    
    sortBy(field) {
      if (this.sortField === field) {
        // Toggle sort order
        this.sortOrder = this.sortOrder === "asc" ? "desc" : "asc";
      } else {
        this.sortField = field;
        this.sortOrder = "desc";
      }
    },
    
    viewSteps(execution) {
      this.selectedExecution = execution;
      this.extractSteps(execution);
      this.showModal = true;
    },
    
    closeModal() {
      this.showModal = false;
      this.selectedExecution = null;
      this.stepsList = [];
    },
    
    extractSteps(execution) {
      this.stepsList = [];
      
      if (!execution) return;
      
      // Extract steps from different possible data structures
      if (execution.steps) {
        if (Array.isArray(execution.steps)) {
          this.stepsList = execution.steps;
        } else if (typeof execution.steps === 'object') {
          // Handle steps as an object
          this.stepsList = Object.values(execution.steps);
        }
      } else if (execution.execution_steps) {
        if (Array.isArray(execution.execution_steps)) {
          this.stepsList = execution.execution_steps;
        } else if (typeof execution.execution_steps === 'object') {
          this.stepsList = Object.values(execution.execution_steps);
        }
      }
      
      // If no steps were found, try alternative approaches
      if (this.stepsList.length === 0 && execution.test_case) {
        // If we have a test case object with steps
        if (typeof execution.test_case === 'object' && execution.test_case.steps) {
          if (Array.isArray(execution.test_case.steps)) {
            this.stepsList = execution.test_case.steps;
          } else if (typeof execution.test_case.steps === 'object') {
            this.stepsList = Object.values(execution.test_case.steps);
          }
        }
        // If we have a test case ID, we could fetch the steps from the API
        else if (typeof execution.test_case === 'number' || typeof execution.test_case === 'string') {
          this.fetchTestCaseSteps(execution.test_case);
        }
      }
      
      // Sort steps by step_number
      this.stepsList.sort((a, b) => {
        return (a.step_number || 0) - (b.step_number || 0);
      });
    },
    
    async fetchTestCaseSteps(testCaseId) {
      if (!testCaseId) return;
      
      try {
        const response = await axios.get(`/test-cases/${testCaseId}/steps/`);
        if (response.data && response.data.length > 0) {
          this.stepsList = response.data;
        }
      } catch (error) {
        console.error(`Error fetching steps for test case ${testCaseId}:`, error);
      }
    },
    
    formatStepStatus(status) {
      if (!status) return "Unknown";
      
      const statusMap = {
        "passed": "Passed",
        "failed": "Failed",
        "skipped": "Skipped",
        "in_progress": "In Progress"
      };
      
      return statusMap[status.toLowerCase()] || status;
    },
    
    getStepStatusClass(status) {
      if (!status) return "badge badge-secondary";
      
      const statusString = status.toLowerCase();
      
      switch (statusString) {
        case "passed":
          return "badge badge-success";
        case "failed":
          return "badge badge-danger";
        case "skipped":
          return "badge badge-warning";
        case "in_progress":
          return "badge badge-info";
        default:
          return "badge badge-secondary";
      }
    }
  }
};
</script>

<style scoped>
/* Filters */
.filters {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.date-filters {
  display: flex;
  align-items: center;
  gap: 10px;
}

.date-filters label {
  font-weight: bold;
  margin-right: 5px;
}

.filter-input {
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ddd;
  background-color: white;
}

/* Table */
.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

th {
  background: #28a745; /* Changed from blue to green */
  color: white;
  padding: 12px;
  text-align: left;
  cursor: pointer;
}

th:hover {
  background: #218838; /* Darker green for hover */
}

td {
  padding: 12px;
  border-bottom: 1px solid #eee;
}

tr:hover {
  background-color: #f5f5f5;
}

/* No Data Message */
.no-data-message {
  text-align: center;
  color: #666;
  font-size: 16px;
  margin-top: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 5px;
  border: 1px solid #eee;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #fff;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.2);
  width: 700px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-title {
  color: #28a745; /* Changed from blue to green */
  margin-bottom: 20px;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
}

.test-info {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 20px;
}

.test-info h4 {
  margin-top: 0;
  color: #333;
  margin-bottom: 10px;
}

.notes-section, .steps-section {
  border: 1px solid #eee;
  border-radius: 6px;
  padding: 15px;
  margin-bottom: 20px;
}

.notes-section h5, .steps-section h5 {
  color: #555;
  margin-top: 0;
  margin-bottom: 10px;
  border-bottom: 1px solid #eee;
  padding-bottom: 5px;
}

.notes-content {
  white-space: pre-line;
  color: #555;
}

.step-item {
  border: 1px solid #eee;
  border-radius: 4px;
  padding: 10px;
  margin-bottom: 10px;
}

.step-header {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.step-number {
  font-weight: bold;
  margin-right: 5px;
}

.step-desc {
  flex: 1;
  margin-right: 10px;
}

.step-detail {
  color: #666;
  font-style: italic;
  margin: 5px 0;
}

.step-notes {
  margin-top: 5px;
  padding-top: 5px;
  border-top: 1px dashed #eee;
  font-size: 0.9em;
  color: #666;
}

.badge {
  padding: 5px 10px;
  font-size: 14px;
  border-radius: 4px;
}

.badge-success {
  background-color: #28a745;
  color: white;
}

.badge-danger {
  background-color: #dc3545;
  color: white;
}

.badge-warning {
  background-color: #ffc107;
  color: black;
}

.badge-info {
  background-color: #17a2b8;
  color: white;
}

.badge-secondary {
  background-color: #6c757d;
  color: white;
}

.alert-info {
  background-color: #d1f7dd; /* Light green background */
  color: #0c5460;
  border: 1px solid #badbcc; /* Light green border */
  padding: 12px;
  border-radius: 4px;
}

.btn {
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  border: none;
  transition: background-color 0.2s;
}

.btn-success {
  background-color: #28a745; /* Green */
  color: white;
}

.btn-success:hover {
  background-color: #218838; /* Darker green */
}

.btn-sm {
  padding: 5px 10px;
  font-size: 12px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.text-success {
  color: #28a745 !important;
}
</style>