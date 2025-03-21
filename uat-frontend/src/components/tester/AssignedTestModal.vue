<template>
  <b-modal
    :show="show"
    @update:show="handleShowUpdate"
    title="📋 Test Case Details"
    @hidden="$emit('close')"
    centered
    class="modern-modal"
  >
    <div v-if="testData">
      <div class="test-info">
        <h4 class="test-title">{{ testData.title }}</h4>
        <p class="test-meta"><strong>🖥️ System:</strong> {{ testData.system }}</p>
        <p class="test-meta">
          <strong>📊 Priority:</strong>
          <span class="badge" :class="getPriorityClass(testData.priority)">
            {{ testData.priority }}
          </span>
        </p>
        <p class="test-meta">
          <strong>✅ Status:</strong>
          <span class="badge" :class="getStatusClass(testData.status)">
            {{ testData.status }}
          </span>
        </p>
        <p class="test-description">
          <strong>📄 Description:</strong> {{ testData.description }}
        </p>
        <p class="test-meta"><strong>📅 Assigned Date:</strong> {{ formatDate(testData.assigned_date) }}</p>
      </div>

      <!-- ✅ View Test Steps Button -->
      <div class="test-steps-section">
        <button class="btn btn-primary" @click="fetchTestSteps(testData.id)" :disabled="isLoading">
          <span v-if="isLoading">Fetching Test Steps...</span>
          <span v-else>🔍 View Test Steps</span>
        </button>
      </div>

      <!-- ✅ Test Steps Section -->
      <transition name="fade">
        <div v-if="showSteps" class="test-steps-container">
          <h5 class="steps-title">Test Steps</h5>
          
          <div v-if="isLoading" class="loading-spinner">
            <i class="fas fa-spinner fa-spin"></i> Loading...
          </div>

          <ul v-else-if="testSteps.length > 0" class="test-steps">
            <li v-for="step in testSteps" :key="step.id">
              <i class="fas fa-check-circle"></i> {{ step.description }}
            </li>
          </ul>

          <div v-else class="no-steps">No test steps found.</div>
        </div>
      </transition>

      <!-- ✅ Error Message -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <!-- ✅ Close Button -->
      <div class="modal-footer">
        <button class="btn close-btn" @click="$emit('close')">
          <i class="fas fa-times"></i> Close
        </button>
      </div>
    </div>
  </b-modal>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue';
import axios from "@/utils/axios.js";

// Props & Emits
const props = defineProps({
  show: Boolean,
  testData: Object
});
const emit = defineEmits(['close']);

// State Variables
const testSteps = ref([]);
const showSteps = ref(false);
const isLoading = ref(false);
const errorMessage = ref("");

// ✅ Fetch Test Steps Correctly
const fetchTestSteps = async (testCaseId) => {
  if (testSteps.value.length > 0) {
    showSteps.value = !showSteps.value; // Toggle visibility
    return;
  }

  isLoading.value = true;
  errorMessage.value = "";

  try {
    const response = await axios.get(`/test-cases/${testCaseId}/steps/`); // ✅ Fixed API Endpoint
    testSteps.value = response.data;
    showSteps.value = true;
  } catch (error) {
    console.error("❌ Error fetching test steps:", error);
    errorMessage.value = "Failed to load test steps. Please try again.";
  }

  isLoading.value = false;
};

// ✅ Handle Modal Close
const handleShowUpdate = (newVal) => {
  emit("update:show", newVal);
};

// ✅ Format Date
const formatDate = (date) => new Date(date).toLocaleDateString();

// ✅ Priority & Status Classes
const getPriorityClass = (priority) => ({
  "badge-high": priority === "High",
  "badge-medium": priority === "Medium",
  "badge-low": priority === "Low",
});

const getStatusClass = (status) => ({
  "badge-passed": status === "Passed",
  "badge-pending": status === "Pending",
  "badge-failed": status === "Failed",
});
</script>

<style scoped>
/* 🎨 Modern Glassmorphism Modal */
.modern-modal {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
}

/* 📝 Test Info */
.test-info {
  padding: 10px;
}

.test-title {
  font-size: 22px;
  font-weight: 700;
  color: #003366;
  margin-bottom: 8px;
}

.test-meta {
  font-size: 15px;
  color: #444;
  margin-bottom: 6px;
}

.test-description {
  font-size: 16px;
  color: #555;
  background: #f8f9fa;
  padding: 10px;
  border-radius: 8px;
  margin-top: 10px;
}

/* 🔖 Badges */
.badge {
  padding: 6px 12px;
  font-size: 13px;
  font-weight: 600;
  border-radius: 15px;
}

.badge-high { background-color: #dc3545; color: white; }
.badge-medium { background-color: #ffc107; color: black; }
.badge-low { background-color: #28a745; color: white; }
.badge-passed { background-color: #28a745; color: white; }
.badge-pending { background-color: #ffc107; color: black; }
.badge-failed { background-color: #dc3545; color: white; }

/* 📋 Test Steps Section */
.test-steps-section {
  text-align: center;
  margin-top: 15px;
}

.btn-primary {
  background: #007bff;
  color: white;
  padding: 8px 15px;
  font-weight: bold;
  border-radius: 5px;
}

.test-steps-container {
  margin-top: 15px;
  padding: 15px;
  border-radius: 8px;
  background: #f0f4ff;
  border-left: 5px solid #007bff;
}

.steps-title {
  font-size: 18px;
  font-weight: bold;
  color: #0056b3;
  text-align: center;
}

.test-steps {
  list-style: none;
  padding-left: 0;
}

.test-steps li {
  background: white;
  padding: 10px;
  margin: 5px 0;
  border-radius: 6px;
  font-size: 15px;
  display: flex;
  align-items: center;
}

.test-steps i {
  margin-right: 10px;
  color: #007bff;
}

/* ❌ Close Button */
.close-btn {
  background-color: #ff4d4d;
  border: none;
  padding: 10px 15px;
  color: white;
  font-size: 14px;
  border-radius: 5px;
  transition: 0.3s;
}

.close-btn:hover {
  background-color: #cc0000;
}

/* 🔄 Loading Spinner */
.loading-spinner {
  text-align: center;
  font-size: 16px;
  color: #007bff;
}

.error-message {
  color: red;
  font-weight: bold;
  text-align: center;
  margin-top: 10px;
}
</style>
