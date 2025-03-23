<template>
  <div>
    <div class="filters">
      <select v-model="filterStatus" class="filter-select">
        <option value="">All Statuses</option>
        <option v-for="status in statusChoices" :key="status.value" :value="status.value">
          {{ status.label }}
        </option>
      </select>

      <div class="date-filters">
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
          <th @click="sortBy('status')">Status</th>
          <th>Comments</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="execution in filteredExecutions" :key="execution.id">
          <td>{{ getTestCaseTitle(execution.test_case) }}</td>
          <td>{{ formatDate(execution.started_at) }}</td>
          <td :class="statusClass(execution.status)">
            {{ getStatusLabel(execution.status) }}
          </td>
          <td>{{ execution.notes || "No comments" }}</td>
        </tr>
      </tbody>
    </table>

    <p v-else class="no-data-message">🚫 No test executions found.</p>
  </div>
</template>

<script>
import axios from "@/utils/axios";

export default {
  props: {
    executions: Array,
    sortOrder: String,
  },
  data() {
    return {
      filterStatus: "",
      filterStartDate: "",
      filterEndDate: "",
      statusChoices: [
        { value: "in_progress", label: "In Progress" },
        { value: "passed", label: "Passed" },
        { value: "failed", label: "Failed" },
      ],
      testCaseTitles: {},
    };
  },
  computed: {
    filteredExecutions() {
      return this.executions
        .filter((execution) => {
          const matchesStatus =
            !this.filterStatus || execution.status === this.filterStatus;

          const executionDate = new Date(execution.started_at);
          const startDate = this.filterStartDate ? new Date(this.filterStartDate) : null;
          const endDate = this.filterEndDate ? new Date(this.filterEndDate) : null;

          const matchesDate =
            (!startDate || executionDate >= startDate) &&
            (!endDate || executionDate <= endDate);

          return matchesStatus && matchesDate;
        })
        .sort((a, b) => {
          const dateA = new Date(a.started_at);
          const dateB = new Date(b.started_at);
          return this.sortOrder === "asc" ? dateA - dateB : dateB - dateA;
        });
    },
  },
  watch: {
    executions: {
      immediate: true,
      async handler(newExecutions) {
        if (newExecutions && newExecutions.length > 0) {
          const testCaseIds = [...new Set(newExecutions.map((execution) => execution.test_case))];

          console.log("Test Case IDs:", testCaseIds);

          await Promise.all(
            testCaseIds.map((testCaseId) => this.fetchTestCaseTitle(testCaseId))
          );

          console.log("Updated testCaseTitles:", this.testCaseTitles);
        } else {
          this.testCaseTitles = {};
        }
      },
    },
  },
  methods: {
    async fetchTestCaseTitle(testCaseId) {
      try {
        const response = await axios.get(`/test-cases/${testCaseId}/`);
        console.log("Fetched Test Case:", response.data);

        this.$set(this.testCaseTitles, testCaseId, response.data.title || "Unknown");

        console.log("Updated testCaseTitles:", this.testCaseTitles);
      } catch (error) {
        console.error("Error fetching test case title:", error);
        this.$set(this.testCaseTitles, testCaseId, "Unknown");
      }
    },
    getTestCaseTitle(testCaseId) {
      if (this.testCaseTitles[testCaseId]) {
        return this.testCaseTitles[testCaseId];
      } else {
        if (this.testCaseTitles.hasOwnProperty(testCaseId)) {
          return this.testCaseTitles[testCaseId];
        } else {
          return "Loading...";
        }
      }
    },
    getStatusLabel(statusValue) {
      const status = this.statusChoices.find((s) => s.value === statusValue);
      return status ? status.label : statusValue;
    },
    formatDate(date) {
      return new Date(date).toLocaleString();
    },
    statusClass(status) {
      return status === "passed" ? "status-pass" : "status-fail";
    },
    sortBy(column) {
      this.executions.sort((a, b) => {
        if (a[column] < b[column]) return this.sortOrder === "asc" ? -1 : 1;
        if (a[column] > b[column]) return this.sortOrder === "asc" ? 1 : -1;
        return 0;
      });
    },
  },
};
</script>

<style scoped>
/* Filters */
.filters {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.filter-select {
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ddd;
  background-color: white;
  cursor: pointer;
}

.date-filters {
  display: flex;
  gap: 10px;
}

.filter-input {
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ddd;
  background-color: white;
  cursor: pointer;
}

/* Table */
.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}
th {
  background: #007bff;
  color: white;
  padding: 10px;
  cursor: pointer;
}
td {
  padding: 8px;
  border-bottom: 1px solid #ddd;
}
th:hover {
  background: #0056b3;
}

/* Status Classes */
.status-pass {
  color: green;
  font-weight: bold;
}
.status-fail {
  color: red;
  font-weight: bold;
}

/* No Data Message */
.no-data-message {
  text-align: center;
  color: #666;
  font-size: 16px;
  margin-top: 20px;
}
</style>