<template>
    <div class="test-details-container">
      <!-- Header -->
      <div class="header">
        <router-link to="/tester/assigned-tests">
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
  
        <!-- Test Steps -->
        <div class="test-steps">
          <h3>Test Steps</h3>
          <ul>
            <li v-for="step in testData.steps" :key="step.id">
              <strong>Step {{ step.step_number }}:</strong> {{ step.description }}
            </li>
          </ul>
        </div>
      </div>
  
      <!-- Loading or No Data -->
      <div v-else class="loading-message">
        <p>Loading test details...</p>
      </div>
  
      <!-- Execute Button -->
      <div class="execute-button">
        <router-link :to="'/test-execution/' + testData.id">
          <button class="btn btn-success">Execute Test</button>
        </router-link>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "@/utils/axios.js";
  
  export default {
    name: "AssignedTestDetails",
    data() {
      return {
        testData: null,
      };
    },
    async created() {
      const testId = this.$route.params.id;
      try {
        const response = await axios.get(`/test-cases/${testId}`);
        this.testData = response.data;
      } catch (error) {
        console.error("Error fetching test details:", error);
      }
    },
  };
  </script>
  
  <style scoped>
  .test-details-container {
    max-width: 900px;
    margin: 40px auto;
    padding: 20px;
    background: #fff;
    border-radius: 10px;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
  }
  
  h2 {
    font-size: 24px;
    color: #333;
  }
  
  .test-info p {
    font-size: 16px;
    margin-bottom: 10px;
  }
  
  .test-steps {
    margin-top: 20px;
    padding: 15px;
    background: #f8f9fa;
    border-left: 4px solid #28a745;
  }
  
  .test-steps h3 {
    color: #007bff;
  }
  
  .test-steps ul {
    list-style: none;
    padding-left: 0;
  }
  
  .test-steps li {
    padding: 10px;
    margin-bottom: 10px;
    background: #ffffff;
    border-left: 4px solid #007bff;
    border-radius: 5px;
  }
  
  .loading-message {
    text-align: center;
    font-size: 18px;
    color: #777;
  }
  
  .execute-button {
    margin-top: 30px;
    text-align: center;
  }
  
  .execute-button button {
    background-color: #28a745;
    border: none;
    padding: 12px 25px;
    font-size: 16px;
    color: white;
    border-radius: 5px;
    transition: 0.3s;
  }
  
  .execute-button button:hover {
    background-color: #218838;
  }
  
  .btn-outline-primary {
    border-color: #007bff;
    color: #007bff;
    padding: 6px 12px;
    font-size: 14px;
    border-radius: 5px;
    text-transform: uppercase;
  }
  
  .btn-outline-primary:hover {
    background-color: #007bff;
    color: white;
  }
  </style>
  