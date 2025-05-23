<!-- TestCaseManagementView.vue -->
<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2 class="mb-4">
        Test Case Management
        <span v-if="functionalityName" class="functionality-filter-label">({{ functionalityName }})</span>
      </h2>
      <div v-if="isFunctionalityFiltered">
        <button @click="clearFunctionalityFilter" class="btn btn-secondary">
          Show All Test Cases
        </button>
      </div>
    </div>

    <!-- Test Case Table -->
    <TestCaseTable 
      :testCases="filteredTestCases"
      :functionalities="functionalities"
      @openModal="openCreateModal"
      @edit="editTestCase"
      @delete="deleteTestCase"
      @assign="openAssignModal"
      @viewSteps="openTestSteps"
      @addStep="openAddStepModal"
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

    <!-- Add Test Step Modal -->
    <AddTestStepModal
      v-if="showAddStepModal"
      :testCaseId="selectedTestCase?.id"
      :testCaseTitle="selectedTestCase?.title"
      @close="closeAddStepModal"
      @saved="handleStepSaved"
    />
  </div>
</template>

<script>
import axiosInstance from "@/utils/axios.js";
import TestCaseTable from "@/components/TestCaseTable.vue";
import TestCaseModal from "@/components/TestCaseModal.vue";
import TestCaseAssignmentModal from "@/components/AssignTesterModal.vue";
import TestStepsView from "@/components/TestStepsModal.vue";
import AddTestStepModal from "@/components/AddStepModal.vue";
import { useToast } from 'vue-toastification';

const toast = useToast();

export default {
  components: {
    TestCaseTable,
    TestCaseModal,
    TestCaseAssignmentModal,
    TestStepsView,
    AddTestStepModal,
  },
  data() {
    return {
      testCases: [],
      functionalities: [],
      selectedTestCase: null,
      showModal: false,
      showAssignModal: false,
      showStepsModal: false,
      showAddStepModal: false,
      functionalityId: null,
      functionalityName: "",
      isFunctionalityFiltered: false
    };
  },
  computed: {
    // Filter test cases by functionality ID
    filteredTestCases() {
      if (!this.isFunctionalityFiltered) {
        return this.testCasesWithFunctionalityNames;
      }
      
      console.log(`Filtering test cases for functionality ID: ${this.functionalityId}`);
      
      const filtered = this.testCases.filter(testCase => {
        // Handle different possible data structures for functionality
        const testCaseFunctionalityId = 
          testCase.functionality_id !== undefined ? testCase.functionality_id :
          testCase.functionality !== undefined ? 
            (typeof testCase.functionality === 'object' ? testCase.functionality.id : testCase.functionality) :
          null;
        
        console.log(`Test Case: ${testCase.title}, Functionality ID: ${testCaseFunctionalityId}`);
        
        // Compare as strings to avoid type mismatches
        return String(testCaseFunctionalityId) === String(this.functionalityId);
      });
      
      // Add functionality names to filtered test cases
      return filtered.map(testCase => {
        const functionality = this.functionalities.find(func => 
          func.id === testCase.functionality || 
          func.id === testCase.functionality_id || 
          func.id === testCase.functionality?.id
        );
        return {
          ...testCase,
          functionalityName: functionality ? functionality.name : 'N/A'
        };
      });
    },
    
    // Map functionality names to test cases
    testCasesWithFunctionalityNames() {
      return this.testCases.map(testCase => {
        const functionality = this.functionalities.find(func => 
          func.id === testCase.functionality || 
          func.id === testCase.functionality_id || 
          func.id === testCase.functionality?.id
        );
        return {
          ...testCase,
          functionalityName: functionality ? functionality.name : 'N/A'
        };
      });
    }
  },
  methods: {
    // Check URL for functionality_id parameter
    checkFunctionalityFilter() {
      const urlParams = new URLSearchParams(window.location.search);
      const functionalityIdParam = urlParams.get('functionality_id');
      const functionalityNameParam = urlParams.get('functionality_name');
      
      if (functionalityIdParam) {
        this.functionalityId = parseInt(functionalityIdParam);
        this.functionalityName = functionalityNameParam || "";
        this.isFunctionalityFiltered = true;
        console.log("Functionality filter active:", this.functionalityId, this.functionalityName);
      }
    },
    
    // Clear functionality filter
    clearFunctionalityFilter() {
      window.location.href = '/admin/test-cases';
    },
    
    async fetchTestCases() {
      try {
        const response = await axiosInstance.get("uat/test-cases/");
        this.testCases = response.data;
        console.log(`Fetched ${this.testCases.length} test cases`);
      } catch (error) {
        console.error("Error fetching test cases:", error);
      }
    },
    
    async fetchFunctionalities() {
      try {
        const response = await axiosInstance.get("uat/functionalities/");
        this.functionalities = response.data;
        
        // If we have a functionality filter but no name, try to get it
        if (this.isFunctionalityFiltered && !this.functionalityName) {
          const functionality = this.functionalities.find(f => f.id === this.functionalityId);
          if (functionality) {
            this.functionalityName = functionality.name;
          }
        }
      } catch (error) {
        console.error("Error fetching functionalities:", error);
      }
    },
    
    openCreateModal() {
      // If creating a new test case with a functionality filter, pre-select that functionality
      this.selectedTestCase = this.isFunctionalityFiltered 
        ? { functionality: this.functionalityId } 
        : null;
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
    
    openAddStepModal(testCase) {
      this.selectedTestCase = { ...testCase };
      this.showAddStepModal = true;
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
    
    closeAddStepModal() {
      this.showAddStepModal = false;
    },
    
    async assignUser({ testCaseId, userId }) {
      try {
        await axiosInstance.post(`uat/test-cases/${testCaseId}/assign/`, { userId: userId });
        this.closeAssignModal();
        this.fetchTestCases();
        toast.success("User assigned successfully!");
      } catch (error) {
        console.error("Error assigning user:", error);
        if (error.response) {
          toast.error("Error assigning user: " + error.response.data.error);
        } else {
          toast.error("An unexpected error occurred.");
        }
      }
    },
    
    async deleteTestCase(id) {
      if (confirm("Are you sure you want to delete this test case?")) {
        await axiosInstance.delete(`uat/test-cases/${id}/`);
        this.fetchTestCases();
      }
    },
    
    async saveTestCase(testCase) {
      try {
        if (testCase.id) {
          await axiosInstance.put(`uat/test-cases/${testCase.id}/`, testCase);
        } else {
          await axiosInstance.post("uat/test-cases/", testCase);
        }
        this.closeModal();
      } catch (error) {
        console.error("Error saving test case:", error);
        toast.error("Error saving test case");
      }
    },
    
    handleStepSaved() {
      this.fetchTestCases(); // Re-fetch test cases to update the list
    }
  },
  mounted() {
    // First check if we're filtering by functionality
    this.checkFunctionalityFilter();
    
    // Then fetch test cases and functionalities
    this.fetchTestCases();
    this.fetchFunctionalities();
  }
};
</script>

<style scoped>
.functionality-filter-label {
  font-size: 0.8em;
  color: #6c757d;
  font-weight: normal;
  margin-left: 10px;
}
</style>