<template>
    <div>
      <canvas ref="chartCanvas"></canvas>
    </div>
  </template>
  
  <script>
  import { Chart } from 'chart.js/auto';
  
  export default {
    props: {
      labels: Array,
      data: Array,
      backgroundColor: Array,
      chartType: {
        type: String,
        default: 'bar'
      }
    },
    mounted() {
      new Chart(this.$refs.chartCanvas, {
        type: this.chartType,
        data: {
          labels: this.labels,
          datasets: [{
            data: this.data,
            backgroundColor: this.backgroundColor
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      });
    }
  }
  </script>
  
  <style scoped>
  canvas {
    max-width: 100%;
    height: 200px;
  }
  </style>
  