<template>
  <div>
    <table class="defect-table">
      <thead>
        <tr>
          <th @click="sortBy('title')">Defect Name</th>
          <th @click="sortBy('execution.test_case_title')">Test Case</th>
          <th @click="sortBy('severity')">Severity</th>
          <th @click="sortBy('status')">Status</th>
          <th @click="sortBy('created_at')">Date Reported</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="defect in sortedDefects" :key="defect.id">
          <!-- ✅ Use correct key for defect name -->
          <td>{{ defect.title ?? 'N/A' }}</td>
          <!-- ✅ Show test case title instead of ID -->
          <td>{{ defect.execution?.test_case_title ?? 'N/A' }}</td>
          <td>
            <span :class="`severity-${defect.severity}`">{{ defect.severity ?? 'N/A' }}</span>
          </td>
          <td>
            <span :class="`status-${defect.status}`">{{ defect.status ?? 'N/A' }}</span>
          </td>
          <td>{{ defect.created_at ? new Date(defect.created_at).toLocaleDateString() : 'N/A' }}</td>
          <td>
            <button class="btn-view" @click="$emit('view-details', defect)">View</button>
          </td>
        </tr>
        <tr v-if="!sortedDefects.length">
          <td colspan="6" class="no-data">No defects reported.</td>
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
  data() {
    return {
      sortKey: "",
      sortAsc: true
    };
  },
  computed: {
    sortedDefects() {
      return [...this.defects].sort((a, b) => {
        if (!this.sortKey) return 0;

        // ✅ Handle nested keys like execution.test_case_title
        const valueA = this.getNestedValue(a, this.sortKey) || "";
        const valueB = this.getNestedValue(b, this.sortKey) || "";

        let result = valueA > valueB ? 1 : -1;
        return this.sortAsc ? result : -result;
      });
    }
  },
  methods: {
    sortBy(key) {
      this.sortAsc = this.sortKey === key ? !this.sortAsc : true;
      this.sortKey = key;
    },
    getNestedValue(obj, path) {
      return path.split('.').reduce((value, key) => value?.[key], obj);
    }
  },
  mounted() {
    console.log("Defects data:", this.defects); // ✅ Debugging data
  }
};
</script>

<style scoped>
.defect-table {
  width: 100%;
  border-collapse: collapse;
}

.defect-table th {
  background: orange;
  color: white;
  cursor: pointer;
  padding: 10px;
}

.defect-table td {
  padding: 10px;
  text-align: center;
}

.status-Open {
  color: red;
  font-weight: bold;
}

.status-InProgress {
  color: orange;
}

.status-Resolved {
  color: green;
}

.status-Closed {
  color: black;
}

.severity-Critical {
  color: red;
}

.severity-High {
  color: darkorange;
}

.severity-Medium {
  color: yellowgreen;
}

.severity-Low {
  color: gray;
}

.btn-view {
  background: #ff6600;
  color: white;
  padding: 5px 10px;
  border: none;
  cursor: pointer;
}

.no-data {
  text-align: center;
  font-style: italic;
  color: gray;
}
</style>
