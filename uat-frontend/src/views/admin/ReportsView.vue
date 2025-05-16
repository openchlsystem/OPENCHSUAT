// ReportsView.vue - Complete Updated File
<template>
  <div class="container mt-4">
    <h2 class="text-center text-primary mb-4">Executed Test Reports</h2>
    <ReportTable
      :executions="executions"
      @view="openModal"
    />
    <ReportModal
      v-if="showModal"
      :execution="selectedExecution"
      @close="closeModal"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/utils/axios'
import ReportTable from '@/components/ReportTable.vue'
import ReportModal from '@/components/ReportModal.vue'

const executions = ref([])
const selectedExecution = ref(null)
const showModal = ref(false)

onMounted(async () => {
  try {
    // Fetch test executions - now with proper test case data from backend
    const res = await axios.get('/test-executions/')
    executions.value = res.data
    
    // Log for debugging
    console.log('Loaded test executions:', executions.value)
  } catch (error) {
    console.error('Error loading reports:', error)
  }
})

const openModal = (execution) => {
  selectedExecution.value = execution
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  selectedExecution.value = null
}
</script>