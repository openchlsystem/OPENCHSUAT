<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3>Assign Test Case</h3>
      <form @submit.prevent="assign">
        <label>Select User</label>
        <select v-model="selectedUser" class="form-control">
          <option v-for="user in testers" :key="user.id" :value="user.id">
            {{ user.first_name }} - {{user.organization_name}}
          </option>
        </select>
        <div class="form-buttons">
          <button type="submit" class="btn btn-primary">Assign</button>
          <button type="button" @click="$emit('close')" class="btn btn-secondary">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axiosInstance from "@/utils/axios.js";

export default {
  props: {
    testCase: Object
  },
  data() {
    return {
      testers: [],
      selectedUser: null
    };
  },
  async mounted() {
    const response = await axiosInstance.get("uat/users/?role=tester");
    this.testers = response.data;
  },
  methods: {
    assign() {
      this.$emit("assign", { testCaseId: this.testCase.id, userId: this.selectedUser });
    }
  }
};
</script>
<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000; /* Ensure it appears above everything */
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  width: 400px; /* Adjust width as needed */
  max-width: 90%;
}
</style>
