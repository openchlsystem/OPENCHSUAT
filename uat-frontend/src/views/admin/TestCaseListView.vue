// TestCaseListView.vue - Enhanced Organization Sections Only

<template>
  <div class="container mt-4">
    <h2 class="mb-4">Test Case Management</h2>

    <!-- Add Test Case button -->
    <div class="d-flex justify-content-end mb-3">
      <button @click="openCreateModal()" class="btn btn-primary">
        <i class="fas fa-plus me-1"></i> Add Test Case
      </button>
    </div>

    <!-- Organizations with Test Cases -->
    <div class="organization-container">
      <div v-for="org in organizations" :key="org.id" class="organization-section mb-4">
        <!-- Organization Header -->
        <div class="organization-header" @click="toggleOrganization(org.id)">
          <div class="d-flex align-items-center">
            <i :class="isOrgExpanded(org.id) ? 'fas fa-chevron-down' : 'fas fa-chevron-right'" class="me-2"></i>
            <span class="organization-name">{{ org.name }}</span>
            <span class="badge bg-primary ms-2">{{ getTestCasesForOrg(org.id).length }}</span>
          </div>
        </div>

        <!-- Test Cases Table - Using your existing TestCaseTable component -->
        <div v-if="isOrgExpanded(org.id)" class="organization-content mt-2">
          <TestCaseTable 
            :testCases="getTestCasesForOrg(org.id)"
            :functionalities="functionalities"
            @openModal="openCreateModal"
            @edit="editTestCase"
            @delete="deleteTestCase"
            @assign="openAssignModal"
            @viewSteps="openTestSteps"
            @addStep="openAddStepModal"
          />
          
          <!-- Show message if no test cases for this organization -->
          <div v-if="getTestCasesForOrg(org.id).length === 0" class="no-test-cases">
            <p class="text-muted mb-0">No test cases found for this organization.</p>
          </div>
        </div>
      </div>
    </div>

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
import axios from "@/utils/axios";
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
      organizations: [],
      systems: [],
      selectedTestCase: null,
      showModal: false,
      showAssignModal: false,
      showStepsModal: false,
      showAddStepModal: false,
      expandedOrgs: new Set(), // Track which organizations are expanded
    };
  },
  methods: {
    // Toggle organization expanded state
    toggleOrganization(orgId) {
      if (this.expandedOrgs.has(orgId)) {
        this.expandedOrgs.delete(orgId);
      } else {
        this.expandedOrgs.add(orgId);
      }
    },
    
    // Check if organization is expanded
    isOrgExpanded(orgId) {
      return this.expandedOrgs.has(orgId);
    },
    
    // Get test cases for a specific organization
    getTestCasesForOrg(orgId) {
      // Get the systems for this organization
      const systemIds = this.systems
        .filter(system => system.organization === orgId)
        .map(system => system.id);
      
      // Get the functionalities for these systems
      const functionalityIds = this.functionalities
        .filter(func => systemIds.includes(func.system))
        .map(func => func.id);
      
      // Get test cases for these functionalities
      return this.testCases.filter(testCase => 
        functionalityIds.includes(testCase.functionality?.id)
      );
    },
    
    async fetchTestCases() {
      try {
        const response = await axios.get("/test-cases/");
        this.testCases = response.data;
      } catch (error) {
        console.error("Error fetching test cases:", error);
        toast.error("Failed to fetch test cases");
      }
    },
    
    async fetchFunctionalities() {
      try {
        const response = await axios.get("/functionalities/");
        this.functionalities = response.data;
      } catch (error) {
        console.error("Error fetching functionalities:", error);
        toast.error("Failed to fetch functionalities");
      }
    },
    
    async fetchOrganizations() {
      try {
        const response = await axios.get("/organizations/");
        this.organizations = response.data;
        
        // Auto-expand the first organization if there are any
        if (this.organizations.length > 0) {
          this.expandedOrgs.add(this.organizations[0].id);
        }
      } catch (error) {
        console.error("Error fetching organizations:", error);
        toast.error("Failed to fetch organizations");
      }
    },
    
    async fetchSystems() {
      try {
        const response = await axios.get("/systems/");
        this.systems = response.data;
      } catch (error) {
        console.error("Error fetching systems:", error);
        toast.error("Failed to fetch systems");
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
        await axios.post(`/test-cases/${testCaseId}/assign/`, { userId: userId });
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
        try {
          await axios.delete(`/test-cases/${id}/`);
          this.fetchTestCases();
          toast.success("Test case deleted successfully");
        } catch (error) {
          console.error("Error deleting test case:", error);
          toast.error("Failed to delete test case");
        }
      }
    },
    
    async saveTestCase(testCase) {
      try {
        if (testCase.id) {
          await axios.put(`/test-cases/${testCase.id}/`, testCase);
          toast.success("Test case updated successfully");
        } else {
          await axios.post("/test-cases/", testCase);
          toast.success("Test case created successfully");
        }
        this.closeModal();
      } catch (error) {
        console.error("Error saving test case:", error);
        toast.error("Failed to save test case");
      }
    },
    
    handleStepSaved() {
      this.fetchTestCases(); // Re-fetch test cases to update the list
    }
  },
  mounted() {
    this.fetchOrganizations();
    this.fetchSystems();
    this.fetchFunctionalities();
    this.fetchTestCases();
  }
};
</script>

<style scoped>
.organization-container {
  margin-top: 1rem;
}

.organization-section {
  border: 1px solid #dee2e6;
  border-radius: 5px;
  overflow: hidden;
}

.organization-header {
  background-color: #f8f9fa;
  padding: 12px 15px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.organization-header:hover {
  background-color: #e9ecef;
}

.organization-name {
  font-weight: 600;
  font-size: 16px;
  color: #333;
}

.organization-content {
  padding: 0;
  background-color: #fff;
}

.no-test-cases {
  padding: 20px;
  text-align: center;
  background-color: #f8f9fa;
  border-top: 1px solid #dee2e6;
}
</style>