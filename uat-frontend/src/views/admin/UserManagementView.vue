<template>
  <div class="container">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h3>User Management</h3>
      <button @click="openUserModal(null)" class="btn btn-primary">+ Add User</button>
    </div>

    <table class="table table-striped">
      <thead class="table-dark">
        <tr>
          <th>Username</th>
          <th>Email</th>
          <th>Role</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.role }}</td>
          <td>
            <span :class="user.is_active ? 'text-success' : 'text-danger'">
              {{ user.is_active ? "Active" : "Inactive" }}
            </span>
          </td>
          <td>
            <button @click="openUserModal(user)" class="btn btn-warning btn-sm">Edit</button>
            <button @click="deleteUser(user.id)" class="btn btn-danger btn-sm">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- User Modal -->
    <UserModal v-if="isUserModalOpen" :user="selectedUser" :roles="roles" @save="saveUser" @close="closeUserModal" />
  </div>
</template>

<script>
import axios from "@/utils/axios";
import UserModal from "@/components/UserModal.vue";

export default {
  components: { UserModal },
  data() {
    return {
      users: [],
      roles: ["Admin", "Tester"],
      isUserModalOpen: false,
      selectedUser: null
    };
  },
  methods: {
    fetchUsers() {
      axios.get("/users/")
        .then(response => {
          this.users = response.data;
        })
        .catch(error => console.error("Error fetching users:", error));
    },
    openUserModal(user) {
      this.selectedUser = user ? { ...user } : { username: "", email: "", role: "Tester", is_active: true };
      this.isUserModalOpen = true;
    },
    closeUserModal() {
      this.isUserModalOpen = false;
    },
    saveUser(userData) {
      const request = userData.id
        ? axios.put(`/users/${userData.id}/`, userData)
        : axios.post("/users/", userData);

      request
        .then(() => {
          this.fetchUsers();
          alert(userData.id ? "User updated successfully!" : "User created successfully!");
        })
        .catch(error => console.error("Error saving user:", error));

      this.closeUserModal();
    },
    deleteUser(userId) {
      if (confirm("Are you sure you want to delete this user?")) {
        axios.delete(`/users/${userId}/`)
          .then(() => {
            this.fetchUsers();
            alert("User deleted successfully!");
          })
          .catch(error => console.error("Error deleting user:", error));
      }
    }
  },
  mounted() {
    this.fetchUsers();
  }
};
</script>

<style scoped>
.container {
  margin-top: 20px;
}
.table {
  margin-top: 10px;
}
.btn-sm {
  margin-right: 5px;
}
</style>
