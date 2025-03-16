<template>
    <div class="card p-3">
      <h5 class="fw-bold">Tester Performance</h5>
  
      <div v-if="testers.length === 0" class="text-center text-muted">
        No tester performance data available.
      </div>
  
      <table v-else class="table table-striped">
        <thead>
          <tr>
            <th>#</th>
            <th>Name</th>
            <th>Tests Executed</th>
            <th>Success Rate (%)</th>
            <th>Defects Reported</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(tester, index) in testers" :key="tester.id">
            <td>{{ index + 1 }}</td>
            <td>{{ tester.name }}</td>
            <td>{{ tester.tests_executed }}</td>
            <td>
              <span class="badge bg-success">{{ tester.success_rate }}%</span>
            </td>
            <td>
              <span class="badge bg-danger">{{ tester.defects_reported }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  import { defineProps } from 'vue';
  
  defineProps({
    testers: Array
  });
  </script>
  