<template>
  <div>
    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Loading dashboard data...</p>
    </div>
    
    <div v-else-if="error" class="alert alert-danger">
      <strong>Error:</strong> {{ error }}
    </div>
    
    <div v-else>
      <div class="dashboard-cards">
        <DashboardCard title="Assigned Test Cases" :value="stats.assigned_tests" icon="fas fa-tasks" />
        <DashboardCard title="Executed Tests" :value="stats.executed_tests" icon="fas fa-check-circle" />
        <DashboardCard title="Pending Tests" :value="stats.pending_tests" icon="fas fa-clock" />
        <DashboardCard title="Passed Tests" :value="stats.passed_tests" icon="fas fa-thumbs-up" />
        <DashboardCard title="Failed Tests" :value="stats.failed_tests" icon="fas fa-times-circle" />
        <DashboardCard title="Reported Defects" :value="stats.reported_defects" icon="fas fa-bug" />
      </div>
      
      <div class="chart-container">
        <DashboardChart
          :labels="['Passed', 'Failed', 'Blocked']"
          :data="[stats.passed_tests, stats.failed_tests, stats.blocked_tests]"
          :backgroundColor="['#28a745', '#dc3545', '#ffc107']"
        />
      </div>
      
      <div>
        <h3>Recent Activity</h3>
        <div v-if="recentActivities.length === 0" class="text-center text-muted my-4">
          <p>No recent activities found.</p>
        </div>
        <RecentActivityTable v-else :activities="recentActivities" />
      </div>
    </div>
  </div>
</template>

<script>
import DashboardCard from '@/components/Admin/DashboardCard.vue';
import DashboardChart from '@/components/Admin/DashboardChart.vue';
import RecentActivityTable from '@/components/Admin/RecentActivityTable.vue';
import axios from '@/utils/axios.js';

export default {
  name: 'TesterDashboardView',
  components: { DashboardCard, DashboardChart, RecentActivityTable },
  
  data() {
    return {
      loading: true,
      error: null,
      stats: {
        assigned_tests: 0,
        executed_tests: 0,
        pending_tests: 0,
        passed_tests: 0,
        failed_tests: 0,
        blocked_tests: 0,
        reported_defects: 0
      },
      recentActivities: []
    };
  },
  
  created() {
    this.fetchDashboardData();
  },
  
  methods: {
    async fetchDashboardData() {
      this.loading = true;
      this.error = null;
      
      try {
        console.log('Fetching tester dashboard data...');
        const response = await axios.get('/tester-dashboard/');
        console.log('Dashboard data received:', response.data);
        
        // Update stats
        if (response.data && response.data.stats) {
          this.stats = {
            ...this.stats,
            ...response.data.stats
          };
        }
        
        // Update recent activities
        if (response.data && response.data.recent_activities) {
          this.recentActivities = response.data.recent_activities;
        }
        
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        
        // Extract error message from response if available
        if (error.response && error.response.data) {
          if (error.response.data.error) {
            this.error = error.response.data.error;
          } else if (error.response.data.message) {
            this.error = error.response.data.message;
          } else {
            this.error = `Error: ${error.response.status} - Failed to fetch dashboard data`;
          }
        } else {
          this.error = error.message || 'Failed to fetch dashboard data. Please try again later.';
        }
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.dashboard-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.chart-container {
  margin-top: 24px;
  margin-bottom: 32px;
  height: 200px;
}

h3 {
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #eaeaea;
}
</style>