<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <h3 v-if="localTestCase.id">Edit Test Case</h3>
      <h3 v-else>Add New Test Case</h3>

      <form @submit.prevent="save">
        <div class="form-group">
          <label for="title">Test Case Title</label>
          <input
            type="text"
            id="title"
            v-model="localTestCase.title"
            class="form-control"
            required
          />
        </div>

        <div class="form-group">
          <label for="functionality">Functionality</label>
          <select
            id="functionality"
            v-model="localTestCase.functionality"
            class="form-control"
            required
          >
            <option value="" disabled>Select Functionality</option>
            <option
              v-for="func in functionalities"
              :key="func.id"
              :value="func.id"
            >
              {{ func.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <textarea
            id="description"
            v-model="localTestCase.description"
            class="form-control"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="expected_result">Expected Result</label>
          <input
            type="text"
            id="expected_result"
            v-model="localTestCase.expected_result"
            class="form-control"
            required
          />
        </div>

        <div class="form-buttons">
          <button type="submit" class="btn btn-primary">Create</button>
          <button type="button" @click="$emit('close')" class="btn btn-secondary">Cancel</button>
          <button type="button" @click="openAddStepModal" class="btn btn-info">Add Step</button>
        </div>
      </form>

      <!-- Add Test Step Modal -->
      <AddTestStepModal
        v-if="showAddStepModal"
        :testCaseId="localTestCase.id"
        @close="closeAddStepModal"
        @saved="handleStepSaved"
      />
    </div>
  </div>
</template>

<script>
import axios from "@/utils/axios";
import AddTestStepModal from "@/components/AddStepModal.vue";
import { useToast } from 'vue-toastification';

const toast = useToast();

export default {
  components: {
    AddTestStepModal
  },
  props: {
    testCase: Object,
    functionalities: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      localTestCase: {},
      showAddStepModal: false
    };
  },
  watch: {
    testCase: {
      immediate: true,
      handler(newValue) {
        this.localTestCase = newValue
          ? { ...newValue }
          : { title: "", functionality: "", description: "", expected_result: "" };
      }
    }
  },
  methods: {
    save() {
      this.$emit("save", this.localTestCase);
    },
    openAddStepModal() {
      if (!this.localTestCase.id) {
        toast.warning("Please save the test case before adding steps.");
        return;
      }
      this.showAddStepModal = true;
    },
    closeAddStepModal() {
      this.showAddStepModal = false;
    },
    handleStepSaved() {
      this.closeAddStepModal();
      // Optionally, you can emit an event to refresh the parent component
      this.$emit("step-saved");
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
  width: 400px;
}

.form-group {
  margin-bottom: 10px;
}

.form-buttons {
  display: flex;
  justify-content: space-between;
  gap: 10px; /* Add gap between buttons */
}

button {
  flex: 1; /* Make buttons take equal space */
}
</style>