<template>
    <div class="settings-view">
      <div class="container">
        <!-- Header -->
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2 class="fw-bold">Settings</h2>
        </div>
  
        <!-- Settings Sections -->
        <div class="row">
          <!-- User Roles & Permissions -->
          <div class="col-md-6">
            <SettingsCard
              title="User Roles & Permissions"
              description="Manage user roles and permissions."
              icon="bi-person-gear"
              @click="openRoleModal"
            />
          </div>
  
          <!-- Notifications -->
          <div class="col-md-6">
            <SettingsCard
              title="Notifications"
              description="Configure system notifications and alerts."
              icon="bi-bell"
              @click="toggleNotificationSettings"
            />
          </div>
  
          <!-- System Configuration -->
          <div class="col-md-6">
            <SettingsCard
              title="System Configuration"
              description="Update general system settings."
              icon="bi-gear"
              @click="openSystemSettings"
            />
          </div>
  
          <!-- Audit Logs -->
          <div class="col-md-6">
            <SettingsCard
              title="Audit Logs"
              description="View system activity and user logs."
              icon="bi-file-earmark-text"
              @click="viewAuditLogs"
            />
          </div>
        </div>
      </div>
  
      <!-- Role Modal -->
      <RoleModal 
        v-model:show="showRoleModal"
        @save="saveRoleSettings"
      />
  
      <!-- Notifications Settings -->
      <b-modal
        v-model="showNotificationModal"
        title="Notification Settings"
        @ok="saveNotificationSettings"
      >
        <div>
          <div class="form-check">
            <input 
              type="checkbox"
              id="emailNotifications"
              v-model="notificationSettings.email"
              class="form-check-input"
            />
            <label class="form-check-label" for="emailNotifications">Enable Email Notifications</label>
          </div>
  
          <div class="form-check">
            <input 
              type="checkbox"
              id="smsNotifications"
              v-model="notificationSettings.sms"
              class="form-check-input"
            />
            <label class="form-check-label" for="smsNotifications">Enable SMS Notifications</label>
          </div>
        </div>
      </b-modal>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import SettingsCard from '@/components/SettingsCard.vue';
  import RoleModal from '@/components/RoleModal.vue';
  
  const showRoleModal = ref(false);
  const showNotificationModal = ref(false);
  
  const notificationSettings = ref({
    email: true,
    sms: false,
  });
  
  const openRoleModal = () => {
    showRoleModal.value = true;
  };
  
  const toggleNotificationSettings = () => {
    showNotificationModal.value = true;
  };
  
  const openSystemSettings = () => {
    console.log('Open System Settings');
  };
  
  const viewAuditLogs = () => {
    console.log('View Audit Logs');
  };
  
  const saveRoleSettings = () => {
    console.log('Role settings saved');
  };
  
  const saveNotificationSettings = () => {
    console.log('Notification settings saved', notificationSettings.value);
  };
  </script>
  
  <style scoped>
  .settings-view {
    padding: 20px;
  }
  </style>
  