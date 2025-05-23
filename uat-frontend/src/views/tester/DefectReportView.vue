// Updated DefectReportView.vue to Handle Success

<template>
  <div class="container mt-4">
    <h2 class="text-center">Report Defects</h2>
    
    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p>Loading data...</p>
    </div>
    
    <div v-else>
      <div class="d-flex justify-content-between align-items-center mb-4">
        <button class="btn btn-primary" @click="showForm = true">
          <i class="fas fa-plus"></i> Report New Defect
        </button>
        
        <div v-if="defects.length > 0" class="text-muted">
          Total: {{ defects.length }} defect{{ defects.length !== 1 ? 's' : '' }}
        </div>
      </div>
      
      <!-- Defect Form Modal -->
      <DefectForm
        v-if="showForm"
        @close="showForm = false"
        @submit-success="handleDefectSuccess"
        :testCases="testCases"
        :defectOptions="defectOptions"
      />
      
      <!-- Success Message -->
      <div v-if="successMessage" class="alert alert-success alert-dismissible fade show" role="alert">
        {{ successMessage }}
        <button type="button" class="btn-close" @click="successMessage = ''"></button>
      </div>
      
      <!-- Error Message -->
      <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show" role="alert">
        {{ errorMessage }}
        <button type="button" class="btn-close" @click="errorMessage = ''"></button>
      </div>
      
      <!-- Defects Table -->
      <DefectTable :defects="defects" />
    </div>
  </div>
</template>

<script>
import axiosInstance from "@/utils/axios.js";;
import DefectForm from "@/components/DefectForm.vue";
import DefectTable from "@/components/DefectTable.vue";

export default {
  components: { DefectForm, DefectTable },
  
  data() {
    return {
      showForm: false,
      defects: [],
      testCases: [],
      defectOptions: {},
      loading: true,
      successMessage: '',
      errorMessage: ''
    };
  },
  
  methods: {
    async fetchData() {
      this.loading = true;
      
      try {
        // Get all required data in parallel
        const [testCasesResponse, defectsResponse, optionsResponse] = await Promise.all([
          axiosInstance.get("uat/test-cases/"),
          axiosInstance.get("uat/defects/"),
          axiosInstance.get("uat/defect-options/")
        ]);
        
        // Process the responses
        this.testCases = testCasesResponse.data;
        this.defects = defectsResponse.data;
        this.defectOptions = optionsResponse.data;
        
        console.log("Data fetched successfully:");
        console.log(`- ${this.testCases.length} test cases`);
        console.log(`- ${this.defects.length} defects`);
        console.log("- Defect options:", this.defectOptions);
        
      } catch (error) {
        console.error("Error fetching data:", error);
        this.errorMessage = "Failed to load data. Please try again.";
      } finally {
        this.loading = false;
      }
    },
    
    handleDefectSuccess(defectData) {
      // Show success message
      this.successMessage = "Defect reported successfully!";
      
      // Refresh data to include the new defect
      this.fetchData();
    }
  },
  
  mounted() {
    this.fetchData();
  }
};
</script>

<style scoped>
.alert {
  margin-bottom: 1.5rem;
}
</style>