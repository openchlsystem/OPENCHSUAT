<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3>Test Steps for "{{ testCase.title }}"</h3>

      <table class="table">
        <thead>
          <tr>
            <th>Step</th>
            <th>Expected Outcome</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="step in testSteps" :key="step.id">
            <td>{{ step.step_description }}</td>
            <td>{{ step.expected_outcome }}</td>
            <td>
              <button @click="editStep(step)" class="btn btn-warning btn-sm">Edit</button>
              <button @click="deleteStep(step.id)" class="btn btn-danger btn-sm">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>

      <button @click="addStep" class="btn btn-primary">+ Add Step</button>
      <button @click="$emit('close')" class="btn btn-secondary">Close</button>
    </div>
  </div>
</template>

<script>
import axios from "@/utils/axios";

export default {
  props: {
    testCase: Object
  },
  data() {
    return {
      testSteps: []
    };
  },
  methods: {
    async fetchTestSteps() {
      try {
        const response = await axios.get(`/testcases/${this.testCase.id}/steps/`);
        this.testSteps = response.data;
      } catch (error) {
        console.error("Error fetching test steps:", error);
      }
    },
    async addStep() {
      const newStep = {
        test_case: this.testCase.id,
        step_description: "New Step",
        expected_outcome: "Expected Outcome"
      };
      await axios.post("/teststeps/", newStep);
      this.fetchTestSteps();
    },
    async editStep(step) {
      const updatedStep = { ...step, step_description: prompt("Edit Step", step.step_description) };
      await axios.put(`/teststeps/${step.id}/`, updatedStep);
      this.fetchTestSteps();
    },
    async deleteStep(stepId) {
      await axios.delete(`/teststeps/${stepId}/`);
      this.fetchTestSteps();
    }
  },
  mounted() {
    this.fetchTestSteps();
  }
};
</script>
