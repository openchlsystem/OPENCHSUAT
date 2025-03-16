<template>
    <div class="container">
      <div class="d-flex justify-content-between align-items-center my-4">
        <h2 class="fw-bold">Test Case Management</h2>
        <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addTestCaseModal">
          + Add Test Case
        </button>
      </div>
  
      <!-- Filter Section -->
      <div class="row mb-4">
        <div class="col-md-4">
          <input
            type="text"
            class="form-control"
            placeholder="Search test cases"
            v-model="search"
          />
        </div>
        <div class="col-md-4">
          <select class="form-select" v-model="filterSystem">
            <option value="">All Systems</option>
            <option v-for="system in systems" :key="system.id" :value="system.id">
              {{ system.name }}
            </option>
          </select>
        </div>
        <div class="col-md-4">
          <select class="form-select" v-model="filterFunctionality">
            <option value="">All Functionalities</option>
            <option v-for="func in functionalities" :key="func.id" :value="func.id">
              {{ func.name }}
            </option>
          </select>
        </div>
      </div>
  
      <!-- Test Cases List -->
      <table class="table table-striped">
        <thead>
          <tr>
            <th>#</th>
            <th>Title</th>
            <th>System</th>
            <th>Functionality</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(testCase, index) in filteredTestCases" :key="testCase.id">
            <td>{{ index + 1 }}</td>
            <td>{{ testCase.title }}</td>
            <td>{{ getSystemName(testCase.systemId) }}</td>
            <td>{{ getFunctionalityName(testCase.functionalityId) }}</td>
            <td>
              <button class="btn btn-warning me-2" @click="editTestCase(testCase)">Edit</button>
              <button class="btn btn-danger" @click="deleteTestCase(testCase.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <!-- Modal -->
      <TestCaseModal
        id="addTestCaseModal"
        :testCase="selectedTestCase"
        :systems="systems"
        :functionalities="functionalities"
        @add-test-case="addTestCase"
        @update-test-case="updateTestCase"
      />
    </div>
  </template>
  
  <script>
  import TestCaseModal from '@/components/TestCaseModal.vue';
  
  export default {
    components: { TestCaseModal },
    data() {
      return {
        testCases: [],
        systems: [{ id: 1, name: 'Helpline System' }],
        functionalities: [{ id: 1, name: 'Login' }],
        selectedTestCase: null,
        search: '',
        filterSystem: '',
        filterFunctionality: '',
      };
    },
    computed: {
      filteredTestCases() {
        return this.testCases.filter((tc) => {
          return (
            (!this.filterSystem || tc.systemId === this.filterSystem) &&
            (!this.filterFunctionality || tc.functionalityId === this.filterFunctionality) &&
            (!this.search || tc.title.toLowerCase().includes(this.search.toLowerCase()))
          );
        });
      },
    },
  };
  </script>
  