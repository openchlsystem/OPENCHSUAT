<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3 v-if="functionality.id">Edit Functionality</h3>
      <h3 v-else>Add New Functionality</h3>

      <form @submit.prevent="save">
        <div class="form-group">
          <label for="name">Functionality Name</label>
          <input type="text" id="name" v-model="localFunctionality.name" class="form-control" required />
        </div>

        <div class="form-group">
          <label for="system">System</label>
          <select id="system" v-model="localFunctionality.system" class="form-control" required>
            <option v-for="system in systems" :key="system.id" :value="system.id">
              {{ system.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <textarea id="description" v-model="localFunctionality.description" class="form-control"></textarea>
        </div>

        <div class="form-buttons">
          <button type="submit" class="btn btn-primary">Save</button>
          <button type="button" @click="$emit('close')" class="btn btn-secondary">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    functionality: Object,
    systems: Array
  },
  data() {
    return {
      localFunctionality: { ...this.functionality }
    };
  },
  methods: {
    save() {
      this.$emit("save", this.localFunctionality);
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
}

button {
  width: 48%;
}
</style>
