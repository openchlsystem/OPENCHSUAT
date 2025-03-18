<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3>Execute Test Case: {{ execution.test_case.title }}</h3>

      <form @submit.prevent="submit">
        <div class="form-group" v-for="(step, index) in localSteps" :key="index">
          <label>{{ step.description }}</label>
          <div class="step-actions">
            <button type="button" class="btn btn-success btn-sm" @click="markPass(index)">✅ Pass</button>
            <button type="button" class="btn btn-danger btn-sm" @click="markFail(index)">❌ Fail</button>
          </div>
          <textarea v-model="step.comment" placeholder="Add comments..." class="form-control mt-2"></textarea>
        </div>

        <div class="form-buttons">
          <button type="submit" class="btn btn-primary">Submit</button>
          <button type="button" @click="$emit('close')" class="btn btn-secondary">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    execution: Object
  },
  data() {
    return {
      localSteps: this.execution.test_case.steps.map(step => ({
        ...step,
        status: "",
        comment: ""
      })),
    };
  },
  methods: {
    markPass(index) {
      this.localSteps[index].status = "Passed";
    },
    markFail(index) {
      this.localSteps[index].status = "Failed";
    },
    submit() {
      this.$emit("save", {
        executionId: this.execution.id,
        steps: this.localSteps,
      });
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
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 500px;
}

.form-group {
  margin-bottom: 15px;
}

.step-actions {
  display: flex;
  gap: 10px;
}

.form-buttons {
  display: flex;
  justify-content: space-between;
}
</style>
