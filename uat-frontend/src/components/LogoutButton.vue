<template>
  <button 
    @click="handleLogout" 
    class="logout-btn"
    :class="[
      { 'small': size === 'small' },
      `theme-${theme}`
    ]"
  >
    <i v-if="showIcon" class="fas fa-sign-out-alt"></i>
    <span v-if="showText">{{ buttonText }}</span>
  </button>
</template>

<script>
import { useAuthStore } from '@/store/auth';

export default {
  name: 'LogoutButton',
  props: {
    buttonText: {
      type: String,
      default: 'Logout'
    },
    showIcon: {
      type: Boolean,
      default: true
    },
    showText: {
      type: Boolean,
      default: true
    },
    size: {
      type: String,
      default: 'normal',
      validator: (value) => ['small', 'normal', 'large'].includes(value)
    },
    theme: {
      type: String,
      default: 'admin', // 'admin' or 'tester'
      validator: (value) => ['admin', 'tester'].includes(value)
    }
  },
  setup() {
    const authStore = useAuthStore();

    const handleLogout = () => {
      authStore.logout();
      // The router navigation is handled in the auth store logout method
    };

    return {
      handleLogout
    };
  }
}
</script>

<style scoped>
.logout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 8px 16px;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s;
  width: 100%;
}

/* Admin theme - orange */
.theme-admin {
  background-color: #ff7f00;
}
.theme-admin:hover {
  background-color: #e67300;
}

/* Tester theme - yellow */
.theme-tester {
  background-color: #f8c146;
}
.theme-tester:hover {
  background-color: #e0ac35;
}

.logout-btn.small {
  padding: 6px 12px;
  font-size: 0.85rem;
  width: auto;
}

i {
  font-size: 14px;
}
</style>