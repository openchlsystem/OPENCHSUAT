<template>
    <div>
      <div v-if="defects.length === 0" class="no-defects">
        <p>No defects reported yet. ✅</p>
      </div>
  
      <table v-else class="table custom-table shadow-sm">
        <thead>
          <tr>
            <th>Defect Name</th>
            <th>Test Case</th>
            <th>Severity</th>
            <th>Status</th>
            <th>Evidence</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="defect in defects" :key="defect.id">
            <td>{{ defect.name }}</td>
            <td>{{ defect.test_case?.title || "N/A" }}</td>
            <td>
              <span :class="severityClass(defect.severity)">
                {{ defect.severity }}
              </span>
            </td>
            <td>
              <span class="badge bg-warning">{{ defect.status || "Pending" }}</span>
            </td>
            <td>
              <a v-if="defect.evidence" :href="defect.evidence" target="_blank" class="btn btn-link">
                📎 View
              </a>
              <span v-else>No Evidence</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    props: { defects: Array },
    methods: {
      severityClass(severity) {
        return {
          "badge bg-danger": severity === "Critical",
          "badge bg-warning": severity === "High",
          "badge bg-primary": severity === "Medium",
          "badge bg-success": severity === "Low",
        };
      },
    },
  };
  </script>
  