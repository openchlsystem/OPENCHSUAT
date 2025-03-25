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
import axios from "@/utils/axios";

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
    const response = await axios.get("/users/?role=tester");
    this.testers = response.data;
  },
  methods: {
    assign() {
      this.$emit("assign", { testCaseId: this.testCase.id, userId: this.selectedUser });
    }
  }
};
</script>