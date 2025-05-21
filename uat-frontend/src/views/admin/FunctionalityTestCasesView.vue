<template>
    <div class="container mt-4">
      <h2 class="mb-4">Test Cases for {{ functionalityName }}</h2>
      
      <div class="mb-3">
        <button @click="goBack" class="btn btn-secondary">
          <i class="fas fa-arrow-left"></i> Back to Functionalities
        </button>
      </div>
  
      <!-- Test Cases List -->
      <div class="card">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h4 class="card-title">Test Cases</h4>
            <button @click="openCreateModal" class="btn btn-primary">+ Add Test Case</button>
          </div>
          
          <div v-if="loading" class="text-center py-4">
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
          
          <table v-else-if="testCases.length > 0" class="table table-hover">
            <thead class="table-dark">
              <tr>
                <th width="50"></th>
                <th>Title</th>
                <th>Status</th>
                <th>Created At</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(testCase, index) in testCases" :key="testCase.id" 
                  draggable="true" 
                  @dragstart="startDrag($event, index)"
                  @dragover.prevent
                  @dragenter.prevent
                  @drop="onDrop($event, index)"
                  :class="{ 'drag-over': dragOverIndex === index }">
                <td class="drag-handle text-center">
                  <i class="fas fa-grip-vertical"></i>
                </td>
                <td>{{ testCase.title }}</td>
                <td>
                  <span :class="getStatusClass(testCase.status)">
                    {{ formatStatus(testCase.status) }}
                  </span>
                </td>
                <td>{{ formatDate(testCase.created_at) }}</td>
                <td>
                  <div class="btn-group">
                    <button @click="editTestCase(testCase)" class="btn btn-warning btn-sm">Edit</button>
                    <button @click="viewSteps(testCase)" class="btn btn-info btn-sm">Steps</button>
                    <button @click="addStep(testCase)" class="btn btn-success btn-sm">+ Step</button>
                    <button @click="deleteTestCase(testCase.id)" class="btn btn-danger btn-sm">Delete</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          
          <div v-else class="alert alert-info">
            No test cases found for this functionality. Click "Add Test Case" to create one.
          </div>
        </div>
      </div>
  
      <!-- Test Case Modal (Add/Edit Test Cases) -->
      <TestCaseModal
        v-if="showModal"
        :testCase="selectedTestCase"
        :functionalities="[functionality]"
        @close="closeModal"
        @save="saveTestCase"
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
  import TestCaseModal from "@/components/TestCaseModal.vue";
  import TestStepsView from "@/components/TestStepsModal.vue";
  import AddTestStepModal from "@/components/AddStepModal.vue";
  import { useToast } from 'vue-toastification';
  
  const toast = useToast();
  
  export default {
    components: {
      TestCaseModal,
      TestStepsView,
      AddTestStepModal
    },
    data() {
      return {
        functionalityId: null,
        functionalityName: '',
        functionality: null,
        testCases: [],
        selectedTestCase: null,
        showModal: false,
        showStepsModal: false,
        showAddStepModal: false,
        loading: true,
        draggedItem: null,
        dragOverIndex: null
      };
    },
    methods: {
      async fetchTestCases() {
        this.loading = true;
        try {
          // Use the endpoint with functionality_id filter
          const response = await axiosInstance.get(`uat/test-cases/?functionality_id=${this.functionalityId}`);
          // Sort test cases by sort_order just to be sure
          this.testCases = response.data.sort((a, b) => a.sort_order - b.sort_order);
          console.log("Fetched test cases:", this.testCases);
        } catch (error) {
          console.error("Error fetching test cases:", error);
          toast.error("Failed to load test cases");
        } finally {
          this.loading = false;
        }
      },
  
      async fetchFunctionality() {
        try {
          const response = await axiosInstance.get(`uat/functionalities/${this.functionalityId}/`);
          this.functionality = response.data;
          this.functionalityName = response.data.name;
        } catch (error) {
          console.error("Error fetching functionality details:", error);
          toast.error("Failed to load functionality details");
        }
      },
  
      goBack() {
        this.$router.push('/admin/functionalities');
      },
  
      openCreateModal() {
        this.selectedTestCase = { 
          id: null, 
          title: "", 
          description: "", 
          expected_result: "",
          functionality_id: this.functionalityId 
        };
        this.showModal = true;
      },
  
      editTestCase(testCase) {
        this.selectedTestCase = { ...testCase };
        this.showModal = true;
      },
  
      viewSteps(testCase) {
        this.selectedTestCase = { ...testCase };
        this.showStepsModal = true;
      },
  
      addStep(testCase) {
        this.selectedTestCase = { ...testCase };
        this.showAddStepModal = true;
      },
  
      closeModal() {
        this.showModal = false;
        this.fetchTestCases();
      },
  
      closeTestSteps() {
        this.showStepsModal = false;
      },
  
      closeAddStepModal() {
        this.showAddStepModal = false;
        this.fetchTestCases();
      },
  
      async saveTestCase(testCase) {
        try {
          if (testCase.id) {
            await axiosInstance.put(`uat/test-cases/${testCase.id}/`, testCase);
            toast.success("Test case updated successfully");
          } else {
            await axiosInstance.post("uat/test-cases/", testCase);
            toast.success("Test case created successfully");
          }
          this.closeModal();
        } catch (error) {
          console.error("Error saving test case:", error);
          toast.error("Error saving test case");
        }
      },
  
      async deleteTestCase(id) {
        if (confirm("Are you sure you want to delete this test case?")) {
          try {
            await axiosInstance.delete(`uat/test-cases/${id}/`);
            this.testCases = this.testCases.filter(tc => tc.id !== id);
            toast.success("Test case deleted successfully");
          } catch (error) {
            console.error("Error deleting test case:", error);
            toast.error("Error deleting test case");
          }
        }
      },
  
      handleStepSaved() {
        this.fetchTestCases();
      },
  
      getStatusClass(status) {
        const statusClasses = {
          'draft': 'text-secondary',
          'ready_for_testing': 'text-primary',
          'in_progress': 'text-warning',
          'completed': 'text-success'
        };
        return statusClasses[status] || 'text-secondary';
      },
  
      formatStatus(status) {
        const statusLabels = {
          'draft': 'Draft',
          'ready_for_testing': 'Ready for Testing',
          'in_progress': 'In Progress',
          'completed': 'Completed'
        };
        return statusLabels[status] || status;
      },
  
      formatDate(dateString) {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleDateString();
      },
  
      // Drag and drop handling with native HTML5 drag & drop
      startDrag(event, index) {
        this.draggedItem = index;
        event.dataTransfer.effectAllowed = 'move';
        // Adding some transparency during drag
        event.target.classList.add('dragging');
      },
  
      onDrop(event, dropIndex) {
        event.preventDefault();
        this.dragOverIndex = null;
        
        // Don't do anything if dropping onto the same item
        if (this.draggedItem === dropIndex) {
          return;
        }
  
        // Get the dragged test case
        const testCaseId = this.testCases[this.draggedItem].id;
        
        // Move the item in the UI immediately for better UX
        const item = this.testCases.splice(this.draggedItem, 1)[0];
        this.testCases.splice(dropIndex, 0, item);
        
        // Call the API to update the backend
        this.updateTestCaseOrder(testCaseId, dropIndex);
      },
  
      async updateTestCaseOrder(testCaseId, newPosition) {
        try {
          await axiosInstance.post('uat/test-cases/reorder/', {
            functionality_id: this.functionalityId,
            testcase_id: testCaseId,
            new_position: newPosition
          });
          
          toast.success("Test case order updated");
          // Optionally refresh the test cases to get updated sort_order values
          this.fetchTestCases();
        } catch (error) {
          console.error("Error reordering test cases:", error);
          toast.error("Failed to update test case order");
          // Revert to original order in case of error
          this.fetchTestCases();
        }
      },
  
      // For drag over indication
      onDragOver(index) {
        this.dragOverIndex = index;
      },
  
      onDragLeave() {
        this.dragOverIndex = null;
      }
    },
    created() {
      this.functionalityId = parseInt(this.$route.params.functionalityId);
      this.functionalityName = this.$route.query.functionalityName || 'Functionality';
      
      if (!this.functionalityId) {
        toast.error("Functionality ID is required");
        this.$router.push('/admin/functionalities');
        return;
      }
      
      this.fetchFunctionality();
      this.fetchTestCases();
    }
  };
  </script>
  
  <style scoped>
  .drag-handle {
    cursor: grab;
    color: #aaa;
  }
  .drag-handle:hover {
    color: #666;
  }
  .dragging {
    opacity: 0.5;
  }
  .drag-over {
    background-color: #f0f8ff;
    border: 1px dashed #007bff;
  }
  tr {
    transition: all 0.3s ease;
  }
  </style>