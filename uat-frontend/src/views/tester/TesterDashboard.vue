<template>
  <div>
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
      <RecentActivityTable :activities="recentActivities" />
    </div>
  </div>
</template>

<script>
import DashboardCard from '@/components/Admin/DashboardCard.vue';
import DashboardChart from '@/components/Admin/DashboardChart.vue';
import RecentActivityTable from '@/components/Admin/RecentActivityTable.vue';

export default {
  name: 'TesterDashboardView',
  components: { DashboardCard, DashboardChart, RecentActivityTable },
  data() {
    return {
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
  async created() {
    const response = await this.$axios.get('/api/tester-dashboard/');
    this.stats = response.data.stats;
    this.recentActivities = response.data.recent_activities;
  }
};
</script>

<style scoped>
.dashboard-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.chart-container {
  margin-top: 24px;
  height: 200px;
}
</style>
