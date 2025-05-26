<template>
    <div class="test-details-container">
      <!-- Header -->
      <div class="header">
        <router-link :to="'/tester/assigned-tests'">
          <button class="btn btn-outline-primary">← Back to Tests</button>
        </router-link>
        <h2>{{ testData?.title || "Test Case Details" }}</h2>
      </div>
  
      <!-- Test Details -->
      <div v-if="testData" class="test-content">
        <div class="test-info">
          <p><strong>Functionality:</strong> {{ testData.functionality }}</p>
          <p><strong>Description:</strong> {{ testData.description }}</p>
          <p><strong>Expected Result:</strong> {{ testData.expected_result }}</p>
        </div>
  
        <div class="test-steps">
          <h3>Test Steps</h3>
          <ul>
            <li v-for="step in testData.steps" :key="step.id">
              <strong>Step {{ step.step_number }}:</strong> {{ step.description }}
            </li>
          </ul>
        </div>
      </div>
  
      <!-- Loading -->
      <div v-else class="loading-message">
        <p>Loading test details...</p>
      </div>
  
      <!-- Execute Button -->
      <div class="execute-button">
        <button class="btn btn-success" @click="showTestExecutionModal">
          Execute Test
        </button>
      </div>
  
      <!-- Reused Execution Modal -->
      <TestExecutionModal
        v-if="showModal"
        :execution="selectedExecution"
        @close="closeModal"
        @save="submitExecution"
      />
    </div>
  </template>
  
  <script>
  import axiosInstance from "@/utils/axios.js";
  import TestExecutionModal from "@/components/TestExecutionModal.vue";
  
  export default {
    name: "AssignedTestDetails",
    components: {
      TestExecutionModal,
    },
    data() {
      return {
        testData: null,
        showModal: false,
        selectedExecution: null,
      };
    },
    async created() {
      const testId = this.$route.params.id;
      try {
        const response = await axiosInstance.get(`uat/test-cases/${testId}/`);
        this.testData = response.data;
      } catch (error) {
        console.error("Error fetching test details:", error);
      }
    },
    methods: {
      showTestExecutionModal() {
        this.selectedExecution = { ...this.testData };
        this.showModal = true;
      },
      closeModal() {
        this.showModal = false;
      },
      async submitExecution({ executionId, steps }) {
        try {
          await axiosInstance.post(`uat/test-executions/${executionId}/execute/`, { steps });
          this.closeModal();
        } catch (error) {
          console.error("Error submitting execution:", error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

.test-details-container {
  font-family: 'Inter', sans-serif;
  max-width: 1000px;
  margin: 40px auto;
  padding: 32px;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  border-bottom: 3px solid #007bff;
  padding-bottom: 12px;
}

h2 {
  font-size: 28px;
  color: #1e1e1e;
  font-weight: 600;
}

.test-info p {
  font-size: 16px;
  margin-bottom: 14px;
  color: #333;
  line-height: 1.7;
}

.test-steps {
  margin-top: 32px;
}

.test-steps h3 {
  font-size: 22px;
  font-weight: 600;
  color: #ff6600;
  margin-bottom: 20px;
  border-left: 5px solid #28a745;
  padding-left: 14px;
}

.test-steps ul {
  list-style: none;
  padding-left: 0;
}

.test-steps li {
  position: relative;
  padding: 20px 25px 20px 60px;
  margin-bottom: 18px;
  background: #e9f5ff;
  border-left: 6px solid #007bff;
  border-radius: 10px;
  box-shadow: 0 4px 16px rgba(0, 123, 255, 0.1);
  transition: all 0.25s ease-in-out;
}

.test-steps li:hover {
  background: #d8efff;
  transform: translateY(-2px);
}

.test-steps li::before {
  content: "✓";
  position: absolute;
  top: 18px;
  left: 20px;
  font-size: 20px;
  color: #28a745;
  font-weight: 700;
}

.loading-message {
  text-align: center;
  font-size: 18px;
  color: #555;
  padding: 40px 0;
}

.execute-button {
  margin-top: 40px;
  text-align: center;
}

.execute-button button {
  background-color: #28a745;
  border: none;
  padding: 14px 36px;
  font-size: 16px;
  font-weight: 600;
  color: white;
  border-radius: 8px;
  box-shadow: 0 5px 20px rgba(40, 167, 69, 0.2);
  transition: background 0.3s, transform 0.2s;
}

.execute-button button:hover {
  background-color: #1e7e34;
  transform: scale(1.02);
}

.btn-outline-primary {
  border-color: #007bff;
  color: #007bff;
  padding: 10px 18px;
  font-size: 14px;
  font-weight: 600;
  border-radius: 6px;
  text-transform: uppercase;
  transition: 0.3s ease;
}

.btn-outline-primary:hover {
  background-color: #007bff;
  color: #fff;
}
</style>
