<template>
  <b-modal
    :show="show"
    @hidden="$emit('close')"
    centered
    size="lg"
    class="modern-modal"
    hide-footer
  >
    <template #modal-header>
      <h4 class="modal-title">Test Case Details</h4>
      <button class="close-btn" @click="$emit('close')">&times;</button>
    </template>

    <div v-if="testData" class="modal-body-content">
      <!-- ✅ Test Case Info -->
      <div class="test-info">
        <h4 class="test-title">{{ testData.title }}</h4>
        <p class="test-meta"><strong>Functionality:</strong> {{ testData.functionality }}</p>
        <p class="test-description"><strong>Description:</strong> {{ testData.description }}</p>
        <p class="test-meta"><strong>Expected Result:</strong> {{ testData.expected_result }}</p>
       
        
      </div>

      <!-- ✅ Test Steps -->
      <div class="test-steps-container">
        <h5 class="steps-title">Test Steps</h5>
        <ul v-if="testData.steps && testData.steps.length > 0" class="test-steps">
          <li v-for="step in testData.steps" :key="step.id">
  <div class="step-number">Step {{ step.step_number }}</div>
  <div class="step-content">
    <p><strong>Description:</strong> {{ step.description }}</p>
    <p><strong>Expected Result:</strong> {{ step.expected_result }}</p>
  </div>
</li>

        </ul>
        <div v-else class="no-steps">No test steps found.</div>
      </div>
    </div>

    <!-- ✅ Footer -->
    <div class="modal-footer">
      <button class="btn close-btn" @click="$emit('close')">Close</button>
    </div>
  </b-modal>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";

const props = defineProps({
  show: Boolean,
  testData: Object,
});

const emit = defineEmits(["close"]);
</script>

<style scoped>
/* 🎨 Modern Classic Styling */
.modern-modal {
  background: rgba(255, 255, 255, 0.97);
  border-radius: 10px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
  max-height: 90vh;
  overflow: hidden;
}

/* 📝 Modal Header */
.modal-title {
  font-size: 22px;
  font-weight: bold;
  color: #ff6600; /* Orange */
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: black;
}

/* 📋 Modal Content */
.modal-body-content {
  max-height: 70vh;
  overflow-y: auto;
  padding: 15px;
}

.test-info {
  padding-bottom: 10px;
}

.test-title {
  font-size: 22px;
  font-weight: bold;
  color: #ff6600;
}

.test-meta {
  font-size: 15px;
  color: #222;
  margin-bottom: 6px;
}

.test-description {
  font-size: 16px;
  background: #f8f9fa;
  padding: 12px;
  border-radius: 8px;
  border-left: 4px solid #007bff;
}

/* 📋 Test Steps */
.test-steps-container {
  margin-top: 15px;
  padding: 15px;
  border-radius: 8px;
  background: #f4f4f4;
  border-left: 5px solid #ff6600;
}

.steps-title {
  font-size: 18px;
  font-weight: bold;
  color: #ff6600;
}

.test-steps {
  list-style: none;
  padding-left: 0;
}

.test-steps li {
  background: white;
  padding: 12px;
  margin: 5px 0;
  border-radius: 6px;
  font-size: 15px;
  display: flex;
  align-items: flex-start;
  border-left: 4px solid #007bff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.step-number {
  font-weight: bold;
  color: #007bff;
  margin-right: 10px;
}

.step-content {
  flex: 1;
}

.no-steps {
  text-align: center;
  font-weight: bold;
  color: #777;
  padding: 10px;
}

/* ❌ Footer */
.modal-footer {
  display: flex;
  justify-content: center;
  padding: 10px;
}

.close-btn {
  background-color: #ff6600;
  color: white;
  font-size: 14px;
  padding: 8px 16px;
  border-radius: 5px;
  transition: 0.3s;
  width: 100%;
  text-align: center;
}

.close-btn:hover {
  background-color: #cc5200;
}
</style>
