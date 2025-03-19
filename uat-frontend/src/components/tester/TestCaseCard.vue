<template>
    <div class="test-card">
      <h3>{{ testCase.title }}</h3>
      <p>{{ testCase.description }}</p>
      <p><strong>Status:</strong> {{ testCase.status }}</p>
      <button @click="$emit('view-details', testCase.id)">Execute Test</button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'TestCaseCard',
    props: {
      testCase: Object,
    },
  };
  </script>
  
  <style scoped>
  .test-card {
    border: 1px solid #ddd;
    padding: 16px;
    border-radius: 8px;
    background: #fff;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .test-card h3 {
    margin: 0 0 8px;
  }
  
  .test-card button {
    margin-top: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    padding: 8px 12px;
    cursor: pointer;
  }
  
  .test-card button:hover {
    background-color: #0056b3;
  }
  </style>
  