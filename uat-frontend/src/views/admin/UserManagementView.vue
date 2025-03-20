<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h3 class="text-primary">System Management</h3>
      <button @click="openUserModal(null)" class="btn btn-primary">+ Add User</button>
    </div>

    <UserTable :users="users" @edit="openUserModal" @toggle-status="toggleStatus" />

    <UserModal v-if="showUserModal" :user="selectedUser" @close="closeUserModal" @save="saveUser" />
  </div>
</template>

<script>
import axios from "@/utils/axios.js";
import UserTable from "@/components/UserTable.vue";
import UserModal from "@/components/UserModal.vue";
import { useRouter } from "vue-router";

export default {
  components: { UserTable, UserModal },
  data() {
    return {
      users: [],
      selectedUser: null,
      showUserModal: false,
    };
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get("/users/");
        this.users = response.data;
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },
    openUserModal(user) {
      this.selectedUser = user ? { ...user } : null;
      this.showUserModal = true;
    },
    closeUserModal() {
      this.showUserModal = false;
      this.fetchUsers();
    },
    async saveUser(userData) {
      try {
        if (userData.id) {
          await axios.put(`/users/${userData.id}/`, userData);
        } else {
          await axios.post("/users/", { ...userData, created_by_admin: true });
        }
        this.closeUserModal();
      } catch (error) {
        console.error("Error saving user:", error);
      }
    },
    async toggleStatus(user) {
      try {
        await axios.put(`/users/${user.id}/`, { ...user, is_active: !user.is_active });
        this.fetchUsers();
      } catch (error) {
        console.error("Error updating status:", error);
      }
    },
  },
  mounted() {
    this.fetchUsers();
  },
};
</script>
