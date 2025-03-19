<template>
    <div>
      <table class="table table-striped">
        <thead>
          <tr>
            <th>#</th>
            <th>Description</th>
            <th>Status</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(activity, index) in activities" :key="index">
            <td>{{ index + 1 }}</td>
            <td>{{ activity.description }}</td>
            <td>
              <span :class="getStatusClass(activity.status)">
                {{ activity.status }}
              </span>
            </td>
            <td>{{ activity.date }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      activities: Array
    },
    methods: {
      getStatusClass(status) {
        if (status === 'Passed') return 'badge bg-success';
        if (status === 'Failed') return 'badge bg-danger';
        return 'badge bg-warning';
      }
    }
  }
  </script>
  
  <style scoped>
  .table {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  .badge {
    padding: 4px 8px;
    font-size: 12px;
    border-radius: 4px;
  }
  </style>
  