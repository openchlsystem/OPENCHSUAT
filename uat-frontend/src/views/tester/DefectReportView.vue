<template>
  <div class="container mt-4">
    <h2 class="text-center"> Report Defects</h2>

    <button class="btn btn-primary my-3" @click="showForm = true">➕ Report New Defect</button>

    <!-- Defect Form Modal -->
    <DefectForm v-if="showForm" 
      @close="showForm = false"
      @submit="submitDefect"
      :testCases="testCases"
    />

    <!-- Defects Table -->
    <DefectTable :defects="defects" />
  </div>
</template>

<script>
import axios from "@/utils/axios";
import DefectForm from "@/components/DefectForm.vue";
import DefectTable from "@/components/DefectTable.vue";

export default {
  components: { DefectForm, DefectTable },
  data() {
    return {
      showForm: false,
      defects: [],
      testCases: []
    };
  },
  methods: {
    async fetchData() {
      try {
        const [defectRes, testCaseRes] = await Promise.all([
          axios.get("/defects/"),
          axios.get("/testcases/")
        ]);
        this.defects = defectRes.data;
        this.testCases = testCaseRes.data;
      } catch (error) {
        console.error("Error fetching defects or test cases:", error);
      }
    },
    async submitDefect(formData) {
      try {
        const response = await axios.post("/defects/", formData, {
          headers: { "Content-Type": "multipart/form-data" }
        });
        this.defects.push(response.data);
        this.showForm = false;
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
