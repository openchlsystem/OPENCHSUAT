<template>
    <div class="table-responsive">
      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>Title</th>
            <th>Description</th>
            <th>Expected Outcome</th>
            <th>Status</th>
            <th>Assigned To</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="testCase in filteredTestCases" :key="testCase.id">
            <td>{{ testCase.title }}</td>
            <td>{{ testCase.description }}</td>
            <td>{{ testCase.expected_outcome }}</td>
            <td>{{ testCase.status }}</td>
            <td>
              <select
                class="form-control"
                @change="$emit('assign', testCase.id, $event.target.value)"
              >
                <option value="" disabled selected>Select Tester</option>
                <option v-for="tester in testers" :key="tester.id" :value="tester.id">
                  {{ tester.username }}
                </option>
              </select>
            </td>
            <td>
              <button class="btn btn-sm btn-warning me-2" @click="$emit('edit', testCase)">
                Edit
              </button>
              <button class="btn btn-sm btn-danger" @click="$emit('delete', testCase.id)">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  defineProps({
    filteredTestCases: Array,
    testers: Array
  });
  
  defineEmits(['edit', 'delete', 'assign']);
  </script>
  