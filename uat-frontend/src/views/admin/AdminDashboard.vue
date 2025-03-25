<template>
  <div>
    <div class="dashboard-cards">
      <DashboardCard title="Total Organizations" :value="stats.organizations" icon="fas fa-building" />
      <DashboardCard title="Total Systems" :value="stats.systems" icon="fas fa-desktop" />
      <DashboardCard title="Total Functionalities" :value="stats.functionalities" icon="fas fa-cogs" />
      <DashboardCard title="Total Test Cases" :value="stats.test_cases" icon="fas fa-vial" />
      <DashboardCard title="Active Users" :value="stats.active_users" icon="fas fa-users" />
      <DashboardCard title="Open Defects" :value="stats.open_defects" icon="fas fa-bug" />
    </div>

    <div class="chart-container">
      <DashboardChart
        :labels="['Passed', 'Failed', 'Blocked']"
        :data="[60, 30, 10]"
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
import axios from 'axios';

export default {
  name: 'AdminDashboard',
  components: { DashboardCard, DashboardChart, RecentActivityTable },
  data() {
    return {
      stats: {},
      recentActivities: []
    };
  },
async created() {
  console.log("Dashboard component created"); // Debugging
  try {
    const response = await axios.get('/dashboard/');
    console.log("Fetched stats:", response.data.stats); // Debugging
    this.stats = response.data.stats;
  } catch (error) {
    console.error("Error fetching dashboard data:", error);
  } finally {
    this.loading = false;
  }
},
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
