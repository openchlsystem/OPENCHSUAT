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
  </AuthForm>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth';
import AuthForm from '@/components/AuthForm.vue';

const router = useRouter();
const authStore = useAuthStore();

const handleLogin = async (form) => {
  try {
    const user = await authStore.login(form);
    router.push(user.role === 'admin' ? '/admin/AdminDashboard' : '/tester/TesterDashboard');
  } catch (error) {
    console.error(error);
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
</style>
