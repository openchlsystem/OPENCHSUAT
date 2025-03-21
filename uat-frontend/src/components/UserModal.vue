<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h4 class="modal-title">{{ user ? 'Edit User' : 'Register New User' }}</h4>

      <form @submit.prevent="saveUser">
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
          <input type="password" v-model="formData.password" class="form-control" placeholder="Enter a strong password" />
          <p v-if="user">Leave blank to keep current password.</p>
        </div>

        <div class="form-group">
          <label>Role</label>
          <select v-model="formData.role" class="form-control" required>
            <option v-for="role in roles" :key="role.value" :value="role.value">
              {{ role.label }}
            </option>
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
          <button type="submit" class="btn btn-success">{{ user ? 'Save Changes' : 'Register' }}</button>
          <button type="button" @click="$emit('close')" class="btn btn-secondary">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from "vue";
import axios from "@/utils/axios.js";

export default {
  props: {
    user: Object,
  },
  setup(props, { emit }) {
    const formData = ref({
      whatsapp_number: "",
      first_name: "",
      password: "",
      role: "tester", // Default role
      organization: null,
      is_active: true,
      created_by_admin: true,
    });

    const organizations = ref([]);
    const roles = ref([]);

    // Fetch organizations from the backend
    const fetchOrganizations = async () => {
      try {
        const response = await axios.get("/organizations/");
        organizations.value = response.data;
      } catch (error) {
        console.error("Failed to fetch organizations:", error);
      }
    };

    // Fetch roles from the backend
    const fetchRoles = async () => {
      try {
        const response = await axios.get("/roles/");
        roles.value = response.data;
      } catch (error) {
        console.error("Failed to fetch roles:", error);
      }
    };

    // Fetch data when the modal is mounted
    onMounted(() => {
      fetchOrganizations();
      fetchRoles();
    });

    // Watch for changes in the `user` prop
    watch(
      () => props.user,
      (newValue) => {
        if (newValue) {
          // If editing an existing user, populate the form with their data
          formData.value = { ...newValue };
        } else {
          // If adding a new user, reset the form
          formData.value = {
            whatsapp_number: "",
            first_name: "",
            password: "",
            role: "tester",
            organization: null,
            is_active: true,
            created_by_admin: true,
          };
        }
      },
      { immediate: true }
    );

    // Save or update the user
    const saveUser = async () => {
      try {
        // Ensure the organization ID is an integer
        formData.value.organization = parseInt(formData.value.organization);

        if (props.user) {
          // Update an existing user
          await axios.put(`/users/${props.user.id}/`, formData.value);
          alert("User updated successfully!");
        } else {
          // Create a new user
          await axios.post("/users/", formData.value);
          alert("User registered successfully!");
        }

        // Close the modal and emit the save event
        emit("close");
        emit("save", formData.value);
      } catch (error) {
        alert("Registration failed: " + JSON.stringify(error.response.data));
      }
    };

    return {
      formData,
      saveUser,
      organizations,
      roles,
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