<template>
  <AuthForm 
    title="Login" 
    buttonText="Login" 
    :isLogin="true"
    @submit="handleLogin"
  >
    <div class="form-links">
      <router-link to="/forgot-password" class="link">Forgot Password?</router-link>
      <span> | </span>
      <router-link to="/register" class="link">Create an account</router-link>
    </div>
    <p v-if="error" class="error-message">{{ error }}</p>
  </AuthForm>
</template>

<script setup>
import { ref, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth';
import AuthForm from '@/components/AuthForm.vue';

const router = useRouter();
const authStore = useAuthStore();

const error = ref(null);

const handleLogin = async (form) => {
  try {
    error.value = null; // Reset error state
    await authStore.login(form);

    // Ensure state is updated before navigation
    await nextTick();

    const userRole = authStore.user?.role?.toLowerCase();
    console.log('Logged in user:', authStore.user); // Debugging

    if (userRole === 'admin') {
      router.push('/admin/dashboard');
    } else if (userRole === 'tester') {
      router.push('/tester/dashboard');
    } else {
      router.push('/'); // Fallback to homepage if role is unknown
    }
  } catch (err) {
    error.value = err.response?.data?.message || 'Invalid login credentials';
    console.error('Login error:', err);
  }
};
</script>

<style scoped>
.form-links {
  margin-top: 10px;
  text-align: center;
}

.link {
  color: #ff6600;
  text-decoration: none;
  font-size: 14px;
}

.link:hover {
  text-decoration: underline;
}

.error-message {
  color: red;
  margin-top: 10px;
  text-align: center;
  font-size: 14px;
}
</style>
