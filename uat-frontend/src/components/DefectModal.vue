<template>
  <div v-if="show" class="fixed inset-0 bg-gray-800 bg-opacity-50 flex justify-center items-center z-50">
    <div class="bg-white p-6 rounded-lg shadow-lg w-96">
      <h2 class="text-xl font-semibold mb-4">{{ isEdit ? "Edit Defect" : "Create Defect" }}</h2>

      <!-- Title -->
      <label class="block mb-2 text-sm font-medium text-gray-700">Title</label>
      <input v-model="formData.title" type="text" class="w-full p-2 border rounded mb-4" />

      <!-- Description -->
      <label class="block mb-2 text-sm font-medium text-gray-700">Description</label>
      <textarea v-model="formData.description" class="w-full p-2 border rounded mb-4"></textarea>

      <!-- Severity -->
      <label class="block mb-2 text-sm font-medium text-gray-700">Severity</label>
      <select v-model="formData.severity" class="w-full p-2 border rounded mb-4">
        <option v-for="option in severityOptions" :key="option.value" :value="option.value">
          {{ option.label }}
        </option>
      </select>

      <!-- Status -->
      <label class="block mb-2 text-sm font-medium text-gray-700">Status</label>
      <select v-model="formData.status" class="w-full p-2 border rounded mb-4">
        <option v-for="option in statusOptions" :key="option.value" :value="option.value">
          {{ option.label }}
        </option>
      </select>

      <!-- Resolved -->
      <div class="mb-4">
        <input type="checkbox" v-model="formData.resolved" class="mr-2" />
        <label class="text-sm font-medium text-gray-700">Resolved</label>
      </div>

      <!-- Resolution Notes -->
      <label class="block mb-2 text-sm font-medium text-gray-700">Resolution Notes</label>
      <textarea v-model="formData.resolution_notes" class="w-full p-2 border rounded mb-4"></textarea>

      <!-- Attachment -->
      <label class="block mb-2 text-sm font-medium text-gray-700">Attachment</label>
      <input type="file" @change="handleFileUpload" class="w-full p-2 border rounded mb-4" />

      <!-- Actions -->
      <div class="flex justify-end space-x-2">
        <button @click="closeModal" class="px-4 py-2 bg-gray-400 text-white rounded">Cancel</button>
        <button @click="save" :disabled="isSaving" class="px-4 py-2 bg-blue-500 text-white rounded">
          {{ isSaving ? "Saving..." : isEdit ? "Update" : "Save" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref, watch, onMounted } from "vue";

export default {
  props: {
    show: Boolean,
    defect: Object,
    isEdit: Boolean,
  },
  emits: ["close", "save"],
  setup(props, { emit }) {
    const formData = ref({
      title: "",
      description: "",
      severity: "",
      status: "",
      resolved: false,
      resolution_notes: "",
      attachment: null,
    });

    const severityOptions = ref([]);
    const statusOptions = ref([]);
    const isSaving = ref(false);

    // Fetch options from backend
    const fetchOptions = async () => {
      try {
        const response = await axios.get("/defect-options");
        severityOptions.value = response.data.severity_options || [];
        statusOptions.value = response.data.status_options || [];
      } catch (error) {
        console.error("Error fetching options:", error);
      }
    };

    // Populate form if editing
    watch(
      () => props.defect,
      (newDefect) => {
        if (newDefect) {
          formData.value = { ...newDefect, attachment: null };
        }
      },
      { immediate: true }
    );

    // Handle file upload
    const handleFileUpload = (event) => {
      formData.value.attachment = event.target.files[0];
    };

    // Save function
    const save = async () => {
      isSaving.value = true;
      try {
        let payload = new FormData();

        // Append all fields
        payload.append("title", formData.value.title || "");
        payload.append("description", formData.value.description || "");
        payload.append("severity", formData.value.severity || "");
        payload.append("status", formData.value.status || "");
        payload.append("resolved", formData.value.resolved ? "true" : "false");
        payload.append("resolution_notes", formData.value.resolution_notes || "");

        if (formData.value.attachment) {
          payload.append("attachment", formData.value.attachment);
        }

        if (props.isEdit) {
          await axios.put(`/defects/${props.defect.id}/`, payload);
        } else {
          await axios.post("/defects/", payload);
        }

        emit("save");
        closeModal();
      } catch (error) {
        console.error("Error saving defect:", error);
      } finally {
        isSaving.value = false;
      }
    };

    const closeModal = () => {
      emit("close");
    };

    onMounted(fetchOptions);

    return {
      formData,
      severityOptions,
      statusOptions,
      isSaving,
      handleFileUpload,
      save,
      closeModal,
    };
  },
};
</script>



<style scoped>
.form-label {
  font-weight: 500;
}
.text-danger {
  margin-top: 0.25rem;
  font-size: 0.875rem;
}
.form-text {
  font-size: 0.875rem;
  color: #6c757d;
}
</style>