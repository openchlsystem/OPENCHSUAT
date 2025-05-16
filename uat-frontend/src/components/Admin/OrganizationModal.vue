<template>
  <div class="modal fade show" tabindex="-1" aria-hidden="true" style="display: block;">
    <div class="modal-dialog">
      <div class="modal-content">
        <form @submit.prevent="handleSubmit">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEdit ? 'Edit Organization' : 'Create Organization' }}</h5>
            <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Name</label>
              <input v-model="form.name" type="text" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Description</label>
              <textarea v-model="form.description" class="form-control" rows="3" required></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary">
              {{ isEdit ? 'Update' : 'Create' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, watch } from 'vue';

const props = defineProps({
  organization: {
    type: Object,
    default: () => ({}),
  },
});

const emit = defineEmits(['save', 'close']);

const form = ref({
  name: '',
  description: '',
});

const isEdit = ref(false);

watch(
  () => props.organization,
  (newVal) => {
    if (newVal && newVal.id) {
      form.value = { ...newVal };
      isEdit.value = true;
    } else {
      form.value = { name: '', description: '' };
      isEdit.value = false;
    }
  },
  { immediate: true }
);

const handleSubmit = () => {
  emit('save', { ...form.value, id: props.organization?.id });
};

const closeModal = () => {
  emit('close'); // This will trigger closing logic in the parent
};
</script>


<style scoped>
.modal-content {
  border-radius: 8px;
}
</style>
