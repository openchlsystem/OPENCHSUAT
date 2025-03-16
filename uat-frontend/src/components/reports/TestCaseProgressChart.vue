<template>
    <div class="chart-container">
      <canvas id="testCaseProgressChart"></canvas>
    </div>
  </template>
  
  <script setup>
  import { ref, watch, onMounted } from 'vue';
  import { Chart } from 'chart.js';
  
  const props = defineProps({
    progressData: {
      type: Array,
      required: true,
    },
  });
  
  const chart = ref(null);
  
  onMounted(() => {
    chart.value = new Chart(document.getElementById('testCaseProgressChart'), {
      type: 'pie',
      data: {
        labels: ['Pass', 'Fail', 'Blocked'],
        datasets: [
          {
            data: props.progressData.map(item => item.completion),
            backgroundColor: ['#28a745', '#dc3545', '#ffc107'],
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
        },
      },
    });
  });
  
  watch(() => props.progressData, () => {
    chart.value.update();
  });
  </script>
  
  <style scoped>
  .chart-container {
    position: relative;
    height: 400px;
    width: 100%;
  }
  </style>
  