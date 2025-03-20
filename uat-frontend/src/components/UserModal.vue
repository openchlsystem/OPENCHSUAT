<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h4 class="modal-title">Register New User</h4>

      <form @submit.prevent="registerUser">
        <div class="form-group">
          <label>WhatsApp Number</label>
          <input type="text" v-model="formData.whatsapp_number" class="form-control" placeholder="Enter WhatsApp number" required />
        </div>

        <div class="form-group">
          <label>Name</label>
          <input type="text" v-model="formData.first_name" class="form-control" placeholder="Enter name" required />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input type="password" v-model="formData.password" class="form-control" placeholder="Enter a strong password" required />
        </div>

        <div class="form-group">
          <label>Role</label>
          <select v-model="formData.role" class="form-control">
            <option value="admin">Admin</option>
            <option value="tester">Tester</option>
          </select>
        </div>

        <div class="form-group">
          <label>Organization</label>
          <select v-model="formData.organization" class="form-control" required>
            <option v-for="org in organizations" :key="org.id" :value="org.id">
              {{ org.name }}
            </option>
          </select>
        </div>

        <div class="form-check">
          <input type="checkbox" v-model="formData.is_active" class="form-check-input" />
          <label class="form-check-label">Active</label>
        </div>

        <div class="modal-actions">
          <button type="submit" class="btn btn-success">Register</button>
          <button type="button" @click="$emit('close')" class="btn btn-secondary">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "@/utils/axios.js";

export default {
  setup(_, { emit }) {
    const formData = ref({
      whatsapp_number: "",
      first_name: "",
      password: "",
      role: "tester",
      organization: "",
      is_active: true,
      created_by_admin: true, // Marks admin-created users
    });

    const organizations = ref([]);

    // Fetch organizations from API
    const fetchOrganizations = async () => {
      try {
        const response = await axios.get("/organizations/");
        organizations.value = response.data;
      } catch (error) {
        console.error("Failed to fetch organizations:", error);
      }
    };

    onMounted(fetchOrganizations);

    const registerUser = async () => {
      try {
        await axios.post("/users/", formData.value);
        alert("User registered successfully!");
        emit("userRegistered"); // Notify parent to refresh user list
        emit("close"); // Close modal
      } catch (error) {
        alert("Registration failed: " + error.response.data.detail);
      }
    };

    return {
      formData,
      registerUser,
      organizations,
    };
  },
};
</script>

<style scoped>
/* Modal Background */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

/* Modal Box */
.modal-content {
  background: #fff;
  padding: 20px;
  width: 400px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  animation: fadeIn 0.3s ease-in-out;
}

/* Modal Title */
.modal-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #2c3e50;
}

/* Form Fields */
.form-control {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  transition: all 0.2s ease-in-out;
}

.form-control:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.3);
}

/* Buttons */
.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
}

.btn-success {
  background: #28a745;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  color: #fff;
  cursor: pointer;
  transition: 0.3s ease;
}

.btn-success:hover {
  background: #218838;
}

.btn-secondary {
  background: #6c757d;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  color: #fff;
  cursor: pointer;
  transition: 0.3s ease;
}

.btn-secondary:hover {
  background: #5a6268;
}

/* Modal Animation */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
