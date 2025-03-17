<template>
  <div class="defects-view">
    <div class="container">
      <!-- Header -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="fw-bold">Defects Management</h2>
        <button class="btn btn-primary" @click="openModal">
          <i class="bi bi-bug"></i> Report Defect
        </button>
      </div>

      <!-- Defects Table -->
      <DefectTable 
        :defects="defects" 
        @edit="editDefect" 
        @delete="deleteDefect"
      />

      <!-- Defect Modal -->
      <DefectModal 
        v-model:show="showModal" 
        :defectData="selectedDefect" 
        @save="saveDefect" 
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import DefectTable from '@/components/DefectTable.vue';
import DefectModal from '@/components/DefectModal.vue';
import axios from 'axios';

const defects = ref([]);
const showModal = ref(false);
const selectedDefect = ref(null);

const fetchDefects = async () => {
  try {
    const response = await axios.get('/api/defects/');
    defects.value = response.data;
  } catch (error) {
    console.error('Error fetching defects:', error);
  }
};

const openModal = () => {
  selectedDefect.value = null;
  showModal.value = true;
};

const editDefect = (defect) => {
  selectedDefect.value = { ...defect };
  showModal.value = true;
};

const deleteDefect = async (id) => {
  if (confirm('Are you sure you want to delete this defect?')) {
    try {
      await axios.delete(`/api/defects/${id}/`);
      defects.value = defects.value.filter((defect) => defect.id !== id);
    } catch (error) {
      console.error('Error deleting defect:', error);
    }
  }
};

const saveDefect = async (defectData) => {
  try {
    if (defectData.id) {
      // Update existing defect
      await axios.put(`/api/defects/${defectData.id}/`, defectData);
      const index = defects.value.findIndex((d) => d.id === defectData.id);
      if (index !== -1) {
        defects.value[index] = defectData;
      }
    } else {
      // Create new defect
      const response = await axios.post('/api/defects/', defectData);
      defects.value.push(response.data);
    }
    showModal.value = false;
  } catch (error) {
    console.error('Error saving defect:', error);
  }
};

onMounted(fetchDefects);
</script>

<style scoped>
.defects-view {
  padding: 20px;
}
</style>
