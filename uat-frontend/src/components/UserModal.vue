<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3>{{ user.id ? "Edit User" : "Add New User" }}</h3>

      <form @submit.prevent="save">
        <div class="form-group">
          <label>Username</label>
          <input type="text" v-model="localUser.username" class="form-control" required />
        </div>

        <div class="form-group">
          <label>Email</label>
          <input type="email" v-model="localUser.email" class="form-control" required />
        </div>

        <div class="form-group">
          <label>Role</label>
          <select v-model="localUser.role" class="form-control">
            <option v-for="role in roles" :key="role">{{ role }}</option>
          </select>
        </div>

        <div class="form-group">
          <label>Status</label>
          <select v-model="localUser.is_active" class="form-control">
            <option :value="true">Active</option>
            <option :value="false">Inactive</option>
          </select>
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
    user: Object,
    roles: Array
  },
  data() {
    return {
      localUser: { ...this.user }
    };
  },
  methods: {
    save() {
      this.$emit("save", this.localUser);
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
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
}

.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.form-buttons {
  display: flex;
  justify-content: space-between;
}

.btn {
  padding: 8px 16px;
  font-size: 14px;
}
</style>
