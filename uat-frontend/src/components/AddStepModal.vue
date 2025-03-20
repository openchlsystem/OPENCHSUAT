<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <h3 v-if="isEditing">Edit Test Step</h3>
      <h3 v-else>Add New Test Step</h3>

      <form @submit.prevent="saveStep">
        <div class="form-group">
          <label for="stepNumber">Step Number</label>
          <input
            type="number"
            id="stepNumber"
            v-model="step.step_number"
            class="form-control"
            required
          />
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <textarea
            id="description"
            v-model="step.description"
            class="form-control"
            required
          ></textarea>
        </div>

        <div class="form-group">
          <label for="expectedResult">Expected Result</label>
          <textarea
            id="expectedResult"
            v-model="step.expected_result"
            class="form-control"
            required
          ></textarea>
        </div>

        <div class="form-buttons">
          <button type="submit" class="btn btn-primary">{{ isEditing ? 'Update' : 'Add' }}</button>
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
    testCaseId: {
      type: Number,
      required: true
    },
    stepToEdit: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      step: {
        step_number: 1,
        description: "",
        expected_result: ""
      },
      isEditing: false
    };
  },
  watch: {
    stepToEdit: {
      immediate: true,
      handler(newValue) {
        if (newValue) {
          this.step = { ...newValue };
          this.isEditing = true;
        } else {
          this.step = {
            step_number: 1,
            description: "",
            expected_result: ""
          };
          this.isEditing = false;
        }
      }
    }
  },
  methods: {
    async saveStep() {
      try {
        const payload = {
          test_case: this.testCaseId,
          step_number: this.step.step_number,
          description: this.step.description,
          expected_result: this.step.expected_result
        };

        if (this.isEditing) {
          await axios.put(`http://127.0.0.1:8000/api/test-steps/${this.step.id}/`, payload);
        } else {
          await axios.post("http://127.0.0.1:8000/api/test-steps/", payload);
        }

        this.$emit("saved");
        this.$emit("close");
      } catch (error) {
        console.error("Error saving test step:", error);
        this.$emit("error", error); // Emit error event for handling in parent
      }
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
  margin-bottom: 10px;
}

.form-buttons {
  display: flex;
  justify-content: space-between;
}

button {
  width: 48%;
}
</style>