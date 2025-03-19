// src/store/adminDashboard.js
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useAdminDashboardStore = defineStore('adminDashboard', () => {
  const loading = ref(false);
  const error = ref(null);
  
  // Mock data for dashboard metrics
  const metrics = ref({
    totalTestCases: 120,
    passedTests: 95,
    failedTests: 20,
    blockedTests: 5,
    totalTesters: 15,
    defectsReported: 8,
  });

  // Mock data for recent activity
  const recentActivity = ref([
    { id: 1, message: 'Test Case #12 marked as Passed', time: '5 mins ago' },
    { id: 2, message: 'Defect #45 reported by John Doe', time: '20 mins ago' },
    { id: 3, message: 'Test Case #34 marked as Blocked', time: '1 hour ago' },
  ]);

  // Mock data for performance chart
  const performanceData = ref({
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    data: [90, 80, 95, 85, 87, 92],
  });

  // Simulate fetching from API
  const fetchDashboardData = async () => {
    loading.value = true;
    error.value = null;
    try {
      // Mock delay to simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1000));
      // Assume data is already populated from mock
    } catch (err) {
      error.value = 'Failed to load dashboard data';
    } finally {
      loading.value = false;
    }
  };

  return {
    loading,
    error,
    metrics,
    recentActivity,
    performanceData,
    fetchDashboardData,
  };
});
