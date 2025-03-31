<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h4 class="modal-title">{{ user ? 'Edit User' : 'Register New User' }}</h4>

      <form @submit.prevent="saveUser">
        <div class="form-group">
          <label>WhatsApp Number</label>
          <input
            type="text"
            v-model="formData.whatsapp_number"
            class="form-control"
            placeholder="Enter WhatsApp number"
            required
          />
        </div>

        <div class="form-group">
          <label>Name</label>
          <input
            type="text"
            v-model="formData.first_name"
            class="form-control"
            placeholder="Enter name"
            required
          />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input
            type="password"
            v-model="formData.password"
            class="form-control"
            placeholder="Enter a strong password"
          />
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
          <label>Organizations</label>
          <div class="search-container">
            <input
              type="text"
              v-model="orgSearchQuery"
              class="search-input"
              placeholder="Search organizations..."
              @input="filterOrganizations"
            />
            <span class="search-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
              </svg>
            </span>
          </div>
          <div class="organization-checkboxes">
            <div v-if="filteredOrganizations.length === 0" class="no-results">
              No organizations found
            </div>
            <div v-for="org in filteredOrganizations" :key="org.id" class="form-check">
              <input
                type="checkbox"
                :id="'org-'+org.id"
                class="form-check-input"
                :value="org.id"
                v-model="formData.organizations"
              >
              <label :for="'org-'+org.id" class="form-check-label">
                {{ org.name }}
              </label>
            </div>
          </div>
          <small class="text-muted">Select one or more organizations</small>
        </div>

        <div class="selected-organizations" v-if="formData.organizations.length > 0">
          <label>Selected Organizations:</label>
          <div class="selected-tags">
            <span v-for="orgId in formData.organizations" :key="orgId" class="tag">
              {{ getOrgName(orgId) }}
              <button type="button" @click="removeOrganization(orgId)" class="tag-remove">
                &times;
              </button>
            </span>
          </div>
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
import { useToast } from 'vue-toastification';

const toast = useToast();

export default {
  props: {
    user: Object,
  },
  setup(props, { emit }) {
    const formData = ref({
      whatsapp_number: "",
      first_name: "",
      password: "",
      role: "tester",
      organizations: [],
      is_active: true,
      created_by_admin: true,
    });

    const organizations = ref([]);
    const roles = ref([]);
    const orgSearchQuery = ref("");
    const filteredOrganizations = ref([]);

    const fetchOrganizations = async () => {
      try {
        const response = await axios.get("/organizations/");
        organizations.value = response.data;
        filteredOrganizations.value = [...response.data];
      } catch (error) {
        console.error("Failed to fetch organizations:", error);
      }
    };

    const fetchRoles = async () => {
      try {
        const response = await axios.get("/roles/");
        roles.value = response.data;
      } catch (error) {
        console.error("Failed to fetch roles:", error);
      }
    };

    const filterOrganizations = () => {
      if (!orgSearchQuery.value) {
        filteredOrganizations.value = [...organizations.value];
        return;
      }
      const query = orgSearchQuery.value.toLowerCase();
      filteredOrganizations.value = organizations.value.filter(org =>
        org.name.toLowerCase().includes(query)
      );
    };

    const getOrgName = (orgId) => {
      const org = organizations.value.find(o => o.id === orgId);
      return org ? org.name : 'Unknown Organization';
    };

    const removeOrganization = (orgId) => {
      formData.value.organizations = formData.value.organizations.filter(id => id !== orgId);
    };

    watch(
      () => props.user,
      (newValue) => {
        if (newValue) {
          const orgIds = newValue.user_organizations
            ? newValue.user_organizations.map(org => org.organization.id)
            : [];

          formData.value = {
            whatsapp_number: newValue.whatsapp_number,
            first_name: newValue.first_name,
            password: "",
            role: newValue.role,
            organizations: orgIds,
            is_active: newValue.is_active,
            created_by_admin: newValue.created_by_admin,
          };
        } else {
          formData.value = {
            whatsapp_number: "",
            first_name: "",
            password: "",
            role: "tester",
            organizations: [],
            is_active: true,
            created_by_admin: true,
          };
        }
      },
      { immediate: true }
    );

   const saveUser = async () => {
  try {
    // Create payload with organizations as an array of numbers
    const payload = {
      whatsapp_number: formData.value.whatsapp_number,
      first_name: formData.value.first_name,
      role: formData.value.role,
      is_active: formData.value.is_active,
      created_by_admin: formData.value.created_by_admin,
      organizations: formData.value.organizations.map(id => Number(id)), // Ensure this is an array of numbers
    };

    // Only include password if provided (for updates)
    if (formData.value.password) {
      payload.password = formData.value.password;
    }

    // Validate at least one organization is selected
    if (payload.organizations.length === 0) {
      toast.warning("Please select at least one organization");
      return;
    }

    console.log("Sending payload:", payload);

    const url = props.user ? `/users/${props.user.id}/` : "/users/";
    const method = props.user ? "put" : "post";

    const response = await axios({
      method,
      url,
      data: payload,
      headers: {
        "Content-Type": "application/json",
      },
    });

    toast.success(`User ${props.user ? 'updated' : 'registered'} successfully!`);
    emit("close");
    emit("refresh");
  } catch (error) {
    console.error("Error saving user:", error);
    let errorMessage = "Operation failed";

    if (error.response?.data) {
      if (error.response.data.organizations) {
        errorMessage = `Organization error: ${error.response.data.organizations.join(", ")}`;
      } else if (error.response.data.detail) {
        errorMessage = error.response.data.detail;
      } else {
        errorMessage = JSON.stringify(error.response.data);
      }
    } else if (error.message) {
      errorMessage = error.message;
    }

    toast.error(errorMessage);
  }
};

    onMounted(() => {
      fetchOrganizations();
      fetchRoles();
    });

    return {
      formData,
      saveUser,
      organizations,
      roles,
      orgSearchQuery,
      filteredOrganizations,
      filterOrganizations,
      getOrgName,
      removeOrganization
    };
  },
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
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #fff;
  padding: 20px;
  width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  animation: fadeIn 0.3s ease-in-out;
}

.modal-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 15px;
}

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

.search-container {
  position: relative;
  margin-bottom: 10px;
}

.search-input {
  width: 100%;
  padding: 10px 35px 10px 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.search-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #6c757d;
}

.organization-checkboxes {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
}

.no-results {
  padding: 10px;
  text-align: center;
  color: #6c757d;
}

.form-check {
  margin-bottom: 8px;
  display: flex;
  align-items: center;
}

.form-check-input {
  margin-right: 8px;
}

.selected-organizations {
  margin: 15px 0;
}

.selected-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-top: 5px;
}

.tag {
  display: inline-flex;
  align-items: center;
  background-color: #e9ecef;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 0.9em;
}

.tag-remove {
  background: none;
  border: none;
  color: #6c757d;
  margin-left: 5px;
  cursor: pointer;
  font-size: 1.1em;
  line-height: 1;
}

.tag-remove:hover {
  color: #dc3545;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
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