<template>
    <div class="reports-view">
      <div class="container">
        <!-- Header -->
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2 class="fw-bold">Reports</h2>
          <div>
            <select v-model="filterPeriod" class="form-select" @change="filterReports">
              <option value="7">Last 7 Days</option>
              <option value="30">Last 30 Days</option>
              <option value="90">Last 90 Days</option>
            </select>
          </div>
        </div>
  
        <!-- Overview Cards -->
        <div class="row mb-4">
          <div class="col-md-4">
            <ReportCard title="Total Tests" :value="reportData.totalTests" color="primary" />
          </div>
          <div class="col-md-4">
            <ReportCard title="Passed Tests" :value="reportData.passedTests" color="success" />
          </div>
          <div class="col-md-4">
            <ReportCard title="Failed Tests" :value="reportData.failedTests" color="danger" />
          </div>
        </div>
  
        <!-- Charts Section -->
        <div class="row">
          <div class="col-md-6">
            <div class="card mb-4">
              <div class="card-body">
                <h5 class="card-title">Test Status Overview</h5>
                <div class="chart-container">
                  <canvas ref="statusChart"></canvas>
                </div>
              </div>
            </div>
          </div>
  
          <div class="col-md-6">
            <div class="card mb-4">
              <div class="card-body">
                <h5 class="card-title">Defect Severity Overview</h5>
                <div class="chart-container">
                  <canvas ref="severityChart"></canvas>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Detailed Report Table -->
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Detailed Report</h5>
            <table class="table table-bordered table-hover">
              <thead class="table-dark">
                <tr>
                  <th>ID</th>
                  <th>Test Case</th>
                  <th>Status</th>
                  <th>Severity</th>
                  <th>Executed By</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="report in filteredReports" :key="report.id">
                  <td>{{ report.id }}</td>
                  <td>{{ report.testCase }}</td>
                  <td>
                    <span :class="getStatusClass(report.status)">
                      {{ report.status }}
                    </span>
                  </td>
                  <td>
                    <span :class="getSeverityClass(report.severity)">
                      {{ report.severity }}
                    </span>
                  </td>
                  <td>{{ report.executedBy }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch, nextTick } from 'vue';
  import { Chart, registerables } from 'chart.js';
  import ReportCard from '@/components/ReportCard.vue';
  
  Chart.register(...registerables);
  
  const filterPeriod = ref('7');
  
  const reportData = ref({
    totalTests: 120,
    passedTests: 90,
    failedTests: 30,
  });
  
  const reports = ref([
    { id: 1, testCase: 'Login Test', status: 'Passed', severity: 'Low', executedBy: 'Tester A' },
    { id: 2, testCase: 'API Test', status: 'Failed', severity: 'High', executedBy: 'Tester B' },
    { id: 3, testCase: 'Signup Test', status: 'Blocked', severity: 'Medium', executedBy: 'Tester C' },
    { id: 4, testCase: 'Logout Test', status: 'Passed', severity: 'Low', executedBy: 'Tester A' },
  ]);
  
  const filteredReports = ref(reports.value);
  
  const statusChart = ref(null);
  const severityChart = ref(null);
  
  let statusChartInstance = null;
  let severityChartInstance = null;
  
  // Create Status Chart
  const createStatusChart = async () => {
    if (statusChartInstance) statusChartInstance.destroy();
    await nextTick();
  
    statusChartInstance = new Chart(statusChart.value, {
      type: 'doughnut',
      data: {
        labels: ['Passed', 'Failed', 'Blocked'],
        datasets: [
          {
            data: [reportData.value.passedTests, reportData.value.failedTests, 10],
            backgroundColor: ['#28a745', '#dc3545', '#ffc107'],
            hoverOffset: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              color: '#333',
              font: { size: 14 },
            },
          },
        },
      },
    });
  };
  
  // Create Severity Chart
  const createSeverityChart = async () => {
    if (severityChartInstance) severityChartInstance.destroy();
    await nextTick();
  
    severityChartInstance = new Chart(severityChart.value, {
      type: 'bar',
      data: {
        labels: ['Low', 'Medium', 'High'],
        datasets: [
          {
            label: 'Defects by Severity',
            data: [40, 35, 25],
            backgroundColor: ['#17a2b8', '#ffc107', '#dc3545'],
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            ticks: { color: '#333' },
          },
          y: {
            ticks: { color: '#333', stepSize: 10, beginAtZero: true },
          },
        },
        plugins: {
          legend: {
            position: 'top',
            labels: {
              color: '#333',
              font: { size: 14 },
            },
          },
        },
      },
    });
  };
  
  // Status and Severity Classes
  const getStatusClass = (status) => {
    switch (status) {
      case 'Passed': return 'badge bg-success';
      case 'Failed': return 'badge bg-danger';
      case 'Blocked': return 'badge bg-warning text-dark';
      default: return 'badge bg-secondary';
    }
  };
  
  const getSeverityClass = (severity) => {
    switch (severity) {
      case 'Low': return 'badge bg-info';
      case 'Medium': return 'badge bg-warning text-dark';
      case 'High': return 'badge bg-danger';
      default: return 'badge bg-secondary';
    }
  };
  
  // Filter Reports
  const filterReports = () => {
    console.log(`Filtering reports for last ${filterPeriod.value} days...`);
    // Example: Adjust logic when fetching from backend
    filteredReports.value = reports.value;
  };
  
  onMounted(() => {
    createStatusChart();
    createSeverityChart();
  });
  
  watch(filterPeriod, () => {
    createStatusChart();
    createSeverityChart();
  });
  </script>
  
  <style scoped>
  .reports-view {
    padding: 20px;
  }
  
  .table th,
  .table td {
    text-align: center;
    vertical-align: middle;
  }
  
  .chart-container {
    width: 80%;
    height: 200px;
  }
  
  .card-title {
    font-weight: 600;
    color: #333;
  }
  
  .table-dark th {
    background-color: #343a40;
    color: #fff;
  }
  </style>
  