<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3 class="modal-title">{{ stepToEdit ? 'Edit Step' : 'Add Step' }}</h3>

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

        <div class="form-group">
          <label for="attachment">Attachment</label>
          <input
            type="file"
            id="attachment"
            @change="handleFileUpload"
            class="form-control"
          />
        </div>

        <div class="form-group">
          <button type="submit" class="btn btn-primary">
            {{ stepToEdit ? 'Update' : 'Save' }}
          </button>
          <button type="button" @click="closeModal" class="btn btn-secondary">
            Cancel
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axiosInstance from "@/utils/axios.js";

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
        expected_result: "",
        attachment: null
      },
      file: null
    };
  },
  watch: {
    stepToEdit: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.step = { ...newVal };
        } else {
          this.resetForm();
        }
      }
    }
  },
  methods: {
    resetForm() {
      this.step = {
        step_number: 1,
        description: "",
        expected_result: "",
        attachment: null
      };
      this.file = null;
    },
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
    async saveStep() {
      try {
        const formData = new FormData();
        formData.append("step_number", this.step.step_number);
        formData.append("description", this.step.description);
        formData.append("expected_result", this.step.expected_result);
        formData.append("test_case", this.testCaseId);
        if (this.file) {
          formData.append("attachment", this.file);
        }

        if (this.stepToEdit) {
          // Update existing step
          await axiosInstance.put(`uat/test-steps/${this.stepToEdit.id}/uat`, formData, {
            headers: {
              "Content-Type": "multipart/form-data"
            }
          });
        } else {
          // Create new step
          await axiosInstance.post("uat/test-steps/", formData, {
            headers: {
              "Content-Type": "multipart/form-data"
            }
          });
        }

        this.$emit("saved"); // Emit the saved event
        this.closeModal();
      } catch (error) {
        console.error("Error saving test step:", error);
        this.$emit("error", error);
      }
    },
    closeModal() {
      this.$emit("close");
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

label {
  display: block;
  margin-bottom: 5px;
}

input,
textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  margin-right: 10px;
}
</style>