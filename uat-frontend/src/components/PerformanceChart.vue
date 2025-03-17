<template>
    <div class="card performance-chart-card">
      <div class="card-body">
        <h5 class="card-title">Performance Overview</h5>
        <div class="chart-container">
          <canvas ref="performanceChart"></canvas>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, nextTick } from 'vue';
  import { Chart, registerables } from 'chart.js';
  
  Chart.register(...registerables);
  
  const performanceChart = ref(null);
  let chartInstance = null;
  
  const createChart = async () => {
    if (chartInstance) chartInstance.destroy();
    await nextTick();
  
    chartInstance = new Chart(performanceChart.value, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
        datasets: [
          {
            label: 'Passed',
            data: [65, 59, 80, 81, 56, 55, 40],
            borderColor: '#28a745',
            backgroundColor: 'rgba(40, 167, 69, 0.1)',
            borderWidth: 2,
            pointBackgroundColor: '#28a745',
            pointBorderColor: '#fff',
            pointRadius: 5,
            pointHoverRadius: 7,
            tension: 0.4,
          },
          {
            label: 'Failed',
            data: [35, 30, 45, 50, 40, 35, 20],
            borderColor: '#dc3545',
            backgroundColor: 'rgba(220, 53, 69, 0.1)',
            borderWidth: 2,
            pointBackgroundColor: '#dc3545',
            pointBorderColor: '#fff',
            pointRadius: 5,
            pointHoverRadius: 7,
            tension: 0.4,
          },
          {
            label: 'Blocked',
            data: [10, 15, 5, 8, 12, 10, 7],
            borderColor: '#ffc107',
            backgroundColor: 'rgba(255, 193, 7, 0.1)',
            borderWidth: 2,
            pointBackgroundColor: '#ffc107',
            pointBorderColor: '#fff',
            pointRadius: 5,
            pointHoverRadius: 7,
            tension: 0.4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            ticks: {
              color: '#333',
              font: { size: 14 },
            },
            grid: {
              display: false,
            },
          },
          y: {
            ticks: {
              color: '#333',
              font: { size: 14 },
              stepSize: 20,
              beginAtZero: true,
            },
            grid: {
              color: '#e0e0e0',
            },
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
  
  onMounted(() => {
    createChart();
  });
  </script>
  
  <style scoped>
  .performance-chart-card {
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s ease-in-out;
  }
  
  .performance-chart-card:hover {
    transform: translateY(-4px);
  }
  
  .card-title {
    font-weight: 600;
    color: #333;
    margin-bottom: 20px;
  }
  
  .chart-container {
    height: 300px;
  }
  </style>
  