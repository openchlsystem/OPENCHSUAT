<template>
  <div class="container">
    <div class="d-flex justify-content-between mb-3">
      <h3>Test Cases</h3>
     <!-- <button class="btn btn-primary" @click="openModal()">+ New Test Case</button> -->
    </div>

    <!-- ✅ Search Filter -->
    <div class="mb-3">
      <input
        type="text"
        class="form-control"
        v-model="filterText"
        placeholder="Search..."
      />
    </div>

    <!-- ✅ Test Cases Table -->
    <TestCaseTable
      :filteredTestCases="filteredTestCases"
      @edit="editTestCase"
      @delete="deleteTestCase"
      @assign="assignTestCase"
    />

    <!-- ✅ Create/Edit Modal -->
    <TestCaseModal
      :isEdit="isEdit"
      :testCase="selectedTestCase"
      @save="saveTestCase"
      :testers="testers"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import TestCaseModal from '@/components/TestCaseModal.vue';
import TestCaseTable from '@/components/TestCaseTable.vue';

const testCases = ref([]);
const testers = ref([]);
const filterText = ref('');
const isEdit = ref(false);
const selectedTestCase = ref(null);

const filteredTestCases = computed(() => {
  return testCases.value.filter(testCase =>
    testCase.title.toLowerCase().includes(filterText.value.toLowerCase())
  );
});

// ✅ Fetch test cases from backend
const fetchTestCases = async () => {
  try {
    const response = await axios.get('/api/testcases/');
    testCases.value = response.data;
  } catch (error) {
    console.error('Error fetching test cases:', error);
  }
};

// ✅ Fetch testers from backend
const fetchTesters = async () => {
  try {
    const response = await axios.get('/api/users/');
    testers.value = response.data;
  } catch (error) {
    console.error('Error fetching testers:', error);
  }
};

onMounted(() => {
  fetchTestCases();
  fetchTesters();
});

const openModal = () => {
  isEdit.value = false;
  selectedTestCase.value = null;
};

const editTestCase = (testCase) => {
  isEdit.value = true;
  selectedTestCase.value = { ...testCase };
};

const saveTestCase = async (data) => {
  try {
    if (isEdit.value) {
      await axios.put(`/api/testcases/${selectedTestCase.value.id}/`, data);
    } else {
      await axios.post('/api/testcases/', data);
    }
    fetchTestCases(); // Reload after saving
  } catch (error) {
    console.error('Error saving test case:', error);
  }
};

const deleteTestCase = async (id) => {
  try {
    await axios.delete(`/api/testcases/${id}/`);
    fetchTestCases(); // Reload after delete
  } catch (error) {
    console.error('Error deleting test case:', error);
  }
};

// ✅ Assign Test Case to Tester
const assignTestCase = async (testCaseId, testerId) => {
  try {
    await axios.patch(`/api/testcases/${testCaseId}/`, { assigned_to: testerId });
    fetchTestCases();
  } catch (error) {
    console.error('Error assigning test case:', error);
  }
};
</script>
