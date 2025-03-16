<template>
    <b-card class="filter-panel">
      <b-row>
        <b-col md="3">
          <b-form-select v-model="selectedSystem" :options="systemOptions" placeholder="Select System" />
        </b-col>
        <b-col md="3">
          <b-form-select v-model="selectedFunctionality" :options="functionalityOptions" placeholder="Select Functionality" />
        </b-col>
        <b-col md="2">
          <b-form-select v-model="selectedStatus" :options="statusOptions" placeholder="Select Status" />
        </b-col>
        <b-col md="2">
          <b-form-select v-model="selectedUser" :options="userOptions" placeholder="Select User" />
        </b-col>
        <b-col md="2">
          <b-button variant="primary" @click="applyFilter">Filter</b-button>
        </b-col>
      </b-row>
    </b-card>
  </template>
  
  <script>
  export default {
    name: 'FilterPanel',
  
    props: {
      systems: Array,
      functionalities: Array,
      statuses: Array,
      users: Array
    },
  
    data() {
      return {
        selectedSystem: null,
        selectedFunctionality: null,
        selectedStatus: null,
        selectedUser: null
      };
    },
  
    computed: {
      systemOptions() {
        return [{ value: null, text: 'All Systems' }, ...this.systems.map(s => ({ value: s.id, text: s.name }))];
      },
      functionalityOptions() {
        return [{ value: null, text: 'All Functionalities' }, ...this.functionalities.map(f => ({ value: f.id, text: f.name }))];
      },
      statusOptions() {
        return [
          { value: null, text: 'All Statuses' },
          { value: 'Pending', text: 'Pending' },
          { value: 'In Progress', text: 'In Progress' },
          { value: 'Completed', text: 'Completed' }
        ];
      },
      userOptions() {
        return [{ value: null, text: 'All Users' }, ...this.users.map(u => ({ value: u.id, text: u.name }))];
      }
    },
  
    methods: {
      applyFilter() {
        this.$emit('filter', {
          system: this.selectedSystem,
          functionality: this.selectedFunctionality,
          status: this.selectedStatus,
          user: this.selectedUser
        });
      }
    }
  };
  </script>
  
  <style scoped>
  .filter-panel {
    margin-bottom: 20px;
  }
  </style>
  