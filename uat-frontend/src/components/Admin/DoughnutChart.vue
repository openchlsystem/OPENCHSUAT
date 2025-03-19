<template>
  <div>
    <DoughnutChart :chart-data="chartData" :chart-options="chartOptions" />
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue';
import { Doughnut } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
});

const chartData = computed(() => ({
  labels: props.data.labels,
  datasets: [
    {
      data: props.data.values,
      backgroundColor: ['#ff7f0e', '#2ca02c', '#1f77b4', '#d62728'],
      hoverBackgroundColor: ['#e67300', '#248f24', '#1c6ea4', '#b22222']
    }
  ]
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top'
    },
    tooltip: {
      enabled: true
    }
  }
};
</script>

<style scoped>
div {
  max-width: 400px;
  margin: auto;
}
</style>
