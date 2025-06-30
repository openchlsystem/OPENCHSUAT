<template>
  <div>
    <div v-if="defects.length === 0" class="no-defects">
      <p>No defects reported yet. ✅</p>
    </div>

    <table v-else class="table custom-table shadow-sm">
      <thead>
        <tr>
          <th>Defect Title</th>
          <th>Test Case</th>
          <th>Severity</th>
          <th>Status</th>
          <th>Evidence</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="defect in defects" :key="defect.id">
          <td>{{ defect.title }}</td>
          <td>{{ defect.test_case_title || "N/A" }}</td>
          <td>
            <span :class="severityClass(defect.severity)">
              {{ defect.severity }}
            </span>
          </td>
          <td>
            <span class="badge bg-warning">{{ defect.status || "Pending" }}</span>
          </td>
          <td>
            <a v-if="defect.attachment" :href="defect.attachment" target="_blank" class="btn btn-link">
              View
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
  props: {
    defects: {
      type: Array,
      required: true
    }
  },
  methods: {
    severityClass(severity) {
      return {
        "badge bg-danger": severity === "Critical",
        "badge bg-warning": severity === "High",
        "badge bg-primary": severity === "Medium",
        "badge bg-success": severity === "Low",
      };
    }
  }
};
</script>

<style scoped>
.table {
  margin-top: 1rem;
}

.no-defects {
  text-align: center;
  font-style: italic;
  color: #6c757d;
}

.badge {
  padding: 0.4em 0.6em;
  font-size: 0.85rem;
  border-radius: 0.25rem;
}

.btn-link {
  color: #0d6efd;
  text-decoration: none;
}
</style>
