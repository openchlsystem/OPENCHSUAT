<template>
  <div class="container mt-4">
    <h2 class="text-center">Report Defects</h2>

    <button class="btn btn-primary my-3" @click="showForm = true">➕ Report New Defect</button>

    <!-- Defect Form Modal -->
    <DefectForm
      v-if="showForm"
      @close="showForm = false"
      @submit="submitDefect"
      :testCases="testCases"
      :defectOptions="defectOptions"
    />

    <!-- Defects Table -->
    <DefectTable :defects="defects" />
  </div>
</template>

<script>
import axios from "@/utils/axios.js";
import DefectForm from "@/components/DefectForm.vue";
import DefectTable from "@/components/DefectTable.vue";

export default {
  components: { DefectForm, DefectTable },
  data() {
    return {
      showForm: false,
      defects: [],
      testCases: [],
      defectOptions: []
    };
  },
  methods: {
    async fetchData() {
      try {
        // Fetch test cases assigned to the logged-in user
        const testCaseRes = await axios.get("/test-cases/");
        
        // Fetch all reported defects
        const defectRes = await axios.get("/defects/");
        const defectOptionsRes = await axios.get("/defect-options/");

        this.testCases = testCaseRes.data; // Only assigned test cases
        this.defectOptions = defectOptionsRes.data; // Only assigned test cases
        this.defects = defectRes.data; // All defects
        
      } catch (error) {
        console.error("Error fetching defects or test cases:", error);
      }
    },
    async submitDefect(formData) {
      try {
        await axios.post("/defects/", formData, {
          headers: { "Content-Type": "multipart/form-data" }
        });

        this.showForm = false;
        this.fetchData(); // Refresh defect list after submission
      } catch (error) {
        console.error("Error submitting defect:", error);
      }
    }
  },
  mounted() {
    this.fetchData();
  }
};
</script>
