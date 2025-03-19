<!-- src/components/admin/DefectTable.vue -->
<template>
  <div>
    <table class="defect-table">
      <thead>
        <tr>
          <th @click="sortBy('name')">Defect Name</th>
          <th @click="sortBy('test_case')">Test Case</th>
          <th @click="sortBy('severity')">Severity</th>
          <th @click="sortBy('status')">Status</th>
          <th @click="sortBy('reported_at')">Date Reported</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="defect in sortedDefects" :key="defect.id">
          <td>{{ defect.name }}</td>
          <td>{{ defect.test_case }}</td>
          <td>
            <span :class="`severity-${defect.severity}`">{{ defect.severity }}</span>
          </td>
          <td>
            <span :class="`status-${defect.status}`">{{ defect.status }}</span>
          </td>
          <td>{{ new Date(defect.reported_at).toLocaleDateString() }}</td>
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
    defects: Array
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
        let result = a[this.sortKey] > b[this.sortKey] ? 1 : -1;
        return this.sortAsc ? result : -result;
      });
    }
  },
  methods: {
    sortBy(key) {
      this.sortAsc = this.sortKey === key ? !this.sortAsc : true;
      this.sortKey = key;
    }
  }
};
</script>

<style scoped>
.defect-table {
  width: 100%;
  border-collapse: collapse;
}

.defect-table th {
  background: orange; /* Theme color - Blue */
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
  background: #ff6600; /* Theme color - Orange */
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
