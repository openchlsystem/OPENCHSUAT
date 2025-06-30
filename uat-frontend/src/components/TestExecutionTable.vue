<template>
  <div class="table-responsive">
    <table class="table table-striped table-hover">
      <thead class="thead-dark">
        <tr>
          <th>#</th>
          <th>Test Case</th>
          <th>Functionality</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <!-- Loading State -->
        <tr v-if="loading">
          <td colspan="5" class="text-center">
            <div class="spinner-border text-success" role="status">
              <span class="sr-only">Loading...</span>
            </div>
          </td>
        </tr>

        <!-- Empty State -->
        <tr v-else-if="testExecutions.length === 0">
          <td colspan="5" class="text-center">No test executions found.</td>
        </tr>

        <!-- Data Rows -->
        <tr 
          v-for="(test, index) in testExecutions" 
          :key="test.id"
          :class="{ 'highlighted-row': isHighlighted(test.id) }"
          :ref="isHighlighted(test.id) ? 'highlightedRow' : null"
        >
          <td>{{ index + 1 }}</td>
          <td>{{ getTestCaseTitle(test) }}</td>
          <td>{{ getFunctionalityName(test) }}</td>
          <td>
            <span :class="getStatusClass(test.status)">{{ formatStatus(test.status) }}</span>
          </td>
          <td>
            <button 
              v-if="!isTestExecuted(test)"
              class="btn btn-success btn-sm" 
              @click="$emit('execute', test)"
            >
              Execute
            </button>
            <span v-else class="badge badge-success">Already Executed</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    testExecutions: {
      type: Array,
      default: () => [],
    },
    loading: {
      type: Boolean,
      default: false,
    },
    highlightTestId: {
      type: [Number, String],
      default: null,
    },
  },
  methods: {
    getTestCaseTitle(test) {
      // Handle cases where test case might be a string, JSON string, or an object
      if (!test) return 'Unknown Test';
      
      // If test is a string, try to parse JSON
      if (typeof test === 'string') {
        try {
          const parsed = JSON.parse(test);
          return parsed.name || parsed.title || 'Untitled Test';
        } catch (e) {
          // If not valid JSON, check for name pattern
          const match = test.match(/"name"\s*:\s*"([^"]+)"/);
          if (match && match[1]) return match[1];
          
          // Otherwise return the string itself (if not too long)
          return test.length > 30 ? test.substring(0, 30) + '...' : test;
        }
      }
      
      // If test is an object
      if (typeof test === 'object' && test !== null) {
        // Check for title property
        if (test.title) {
          if (typeof test.title === 'string') return test.title;
          if (typeof test.title === 'object' && test.title.name) return test.title.name;
        }
        
        // Check for name property
        if (test.name) return test.name;
      }
      
      return 'Untitled Test';
    },
    
    getFunctionalityName(test) {
      if (!test) return 'N/A';
      
      // If test is a string, try to parse JSON
      if (typeof test === 'string') {
        try {
          const parsed = JSON.parse(test);
          if (parsed.functionality) {
            if (typeof parsed.functionality === 'string') return parsed.functionality;
            if (typeof parsed.functionality === 'object' && parsed.functionality.name) {
              return parsed.functionality.name;
            }
          }
          return parsed.description || 'N/A';
        } catch (e) {
          // If not valid JSON, check for description pattern
          const match = test.match(/"description"\s*:\s*"([^"]+)"/);
          if (match && match[1]) return match[1];
          return 'N/A';
        }
      }
      
      // If test is an object
      if (typeof test === 'object' && test !== null) {
        // Check for functionality property
        if (test.functionality) {
          if (typeof test.functionality === 'string') return test.functionality;
          if (typeof test.functionality === 'object' && test.functionality.name) {
            return test.functionality.name;
          }
        }
        
        // Check for description property
        if (test.description) return test.description;
        
        // Check for system property
        if (test.system) {
          if (typeof test.system === 'string') return test.system;
          if (typeof test.system === 'object' && test.system.name) {
            return test.system.name;
          }
        }
      }
      
      return 'N/A';
    },
    
    isTestExecuted(test) {
      // Check if the test has been executed by looking at execution history
      if (!test) return false;
      
      // We need to check status more carefully - include all possible "executed" status values
      const status = typeof test.status === 'string' ? test.status.toLowerCase() : '';
      
      // Explicitly check for executed statuses and treat all other statuses as non-executed
      // Include 'completed' to handle cases where status was changed to 'completed'
      return ['executed', 'passed', 'failed', 'completed'].includes(status);
    },
    
    formatStatus(status) {
      if (!status) return "Pending";
      
      // Convert known statuses to proper names
      const statusString = String(status).toLowerCase();
      
      // If the test has been executed in any way, show "Completed"
      if (['executed', 'passed', 'failed', 'completed'].includes(statusString)) {
        return "Completed";
      }
      
      switch (statusString) {
        case "pending":
          return "Pending";
        case "draft":
          return "Pending"; // Convert "draft" to "Pending"
        case "in_progress":
        case "in progress":
          return "In Progress";
        default:
          // Convert to proper case for unknown statuses
          return statusString.charAt(0).toUpperCase() + statusString.slice(1);
      }
    },
    
    getStatusClass(status) {
      if (!status) return "badge badge-secondary";
      
      const statusString = String(status).toLowerCase();
      
      // If the test has been executed in any way, use success style
      if (['executed', 'passed', 'failed', 'completed'].includes(statusString)) {
        return "badge badge-success";
      }
      
      switch (statusString) {
        case "in_progress":
        case "in progress":
          return "badge badge-warning";
        case "draft":
        case "pending":
          return "badge badge-secondary";
        default:
          return "badge badge-secondary";
      }
    },
    
    isHighlighted(testId) {
      return this.highlightTestId && 
             (testId == this.highlightTestId || testId === parseInt(this.highlightTestId));
    },
  },
  
  mounted() {
    // Scroll to highlighted row after component is mounted
    this.$nextTick(() => {
      if (this.highlightTestId && this.$refs.highlightedRow) {
        const element = Array.isArray(this.$refs.highlightedRow) 
          ? this.$refs.highlightedRow[0] 
          : this.$refs.highlightedRow;
        
        if (element) {
          element.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
          });
        }
      }
    });
  },
  
  watch: {
    highlightTestId() {
      // Scroll to highlighted row when highlightTestId changes
      this.$nextTick(() => {
        if (this.highlightTestId && this.$refs.highlightedRow) {
          const element = Array.isArray(this.$refs.highlightedRow) 
            ? this.$refs.highlightedRow[0] 
            : this.$refs.highlightedRow;
          
          if (element) {
            element.scrollIntoView({ 
              behavior: 'smooth', 
              block: 'center' 
            });
          }
        }
      });
    }
  }
};
</script>

<style scoped>
.table {
  width: 100%;
  border-collapse: collapse;
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

.badge-secondary {
  background-color: #6c757d;
  color: white;
}

.btn {
  font-size: 14px;
  padding: 5px 10px;
  border-radius: 4px;
}

.btn-success {
  background-color: #28a745;
  color: white;
}

.btn-success:hover {
  background-color: #218838;
}

.text-center {
  text-align: center;
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

/* Highlighting styles */
.highlighted-row {
  background-color: #fff3cd !important;
  border: 2px solid #ffc107;
  animation: highlight-pulse 2s ease-in-out;
}

@keyframes highlight-pulse {
  0% {
    background-color: #fff3cd;
    box-shadow: 0 0 10px rgba(255, 193, 7, 0.8);
  }
  50% {
    background-color: #ffeaa7;
    box-shadow: 0 0 20px rgba(255, 193, 7, 0.6);
  }
  100% {
    background-color: #fff3cd;
    box-shadow: 0 0 10px rgba(255, 193, 7, 0.8);
  }
}

@keyframes spinner-border {
  to {
    transform: rotate(360deg);
  }
}
</style>