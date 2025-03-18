<template>
  <div class="container mt-4">
    <h2 class="mb-4">Test Case Management</h2>

    <!-- Test Case Table -->
    <TestCaseTable 
      :testCases="testCases" 
      @openModal="openCreateModal"
      @edit="editTestCase"
      @delete="deleteTestCase"
      @assign="openAssignModal"
      @viewSteps="openTestSteps"
    />

    <!-- Test Case Modal (Add/Edit Test Cases) -->
    <TestCaseModal 
      v-if="showModal"
      :testCase="selectedTestCase"
      :functionalities="functionalities"
      @close="closeModal"
      @save="saveTestCase"
    />

    <!-- Assign Test Case Modal -->
    <TestCaseAssignmentModal 
      v-if="showAssignModal"
      :testCase="selectedTestCase"
      @close="closeAssignModal"
      @assign="assignUser"
    />

    <!-- Test Steps View -->
    <TestStepsView 
      v-if="showStepsModal"
      :testCase="selectedTestCase"
      @close="closeTestSteps"
    />
  </div>
</template>

<script>
import axios from "@/utils/axios";
import TestCaseTable from "@/components/TestCaseTable.vue";
import TestCaseModal from "@/components/TestCaseModal.vue";
import TestCaseAssignmentModal from "@/components/AssignTesterModal.vue";
import TestStepsView from "@/components/TestStepsModal.vue";

export default {
  components: {
    TestCaseTable,
    TestCaseModal,
    TestCaseAssignmentModal,
    TestStepsView,
  },
  data() {
    return {
      testCases: [],
      functionalities: [],
      selectedTestCase: null,
      showModal: false,
      showAssignModal: false,
      showStepsModal: false,
    };
  },
  methods: {
    async fetchTestCases() {
      try {
        const response = await axios.get("/testcases/");
        this.testCases = response.data;
      } catch (error) {
        console.error("Error fetching test cases:", error);
      }
    },
    async fetchFunctionalities() {
      try {
        const response = await axios.get("/functionalities/");
        this.functionalities = response.data;
      } catch (error) {
        console.error("Error fetching functionalities:", error);
      }
    },
    openCreateModal() {
      this.selectedTestCase = null;
      this.showModal = true;
    },
    editTestCase(testCase) {
      this.selectedTestCase = { ...testCase };
      this.showModal = true;
    },
    openAssignModal(testCase) {
      this.selectedTestCase = { ...testCase };
      this.showAssignModal = true;
    },
    openTestSteps(testCase) {
      this.selectedTestCase = { ...testCase };
      this.showStepsModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.fetchTestCases();
    },
    closeAssignModal() {
      this.showAssignModal = false;
      this.fetchTestCases();
    },
    closeTestSteps() {
      this.showStepsModal = false;
    },
    async assignUser({ testCaseId, userId }) {
      try {
        await axios.post(`/testcases/${testCaseId}/assign/`, { user_id: userId });
        this.closeAssignModal();
      } catch (error) {
        console.error("Error assigning user:", error);
      }
    },
    async deleteTestCase(id) {
      if (confirm("Are you sure you want to delete this test case?")) {
        await axios.delete(`/testcases/${id}/`);
        this.fetchTestCases();
      }
    },
    async saveTestCase(testCase) {
      if (testCase.id) {
        await axios.put(`/testcases/${testCase.id}/`, testCase);
      } else {
        await axios.post("/testcases/", testCase);
      }
      this.closeModal();
    }
  },
  mounted() {
    this.fetchTestCases();
    this.fetchFunctionalities();
  }
};
</script>
