<template>
    <AuthForm 
      title="Register" 
      buttonText="Register" 
      :isRegister="true"
      @submit="handleRegister"
    />
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router';
  import { useAuthStore } from '@/store/auth';
  import AuthForm from '@/components/AuthForm.vue';
  
  const router = useRouter();
  const authStore = useAuthStore();
  
  const handleRegister = async (form) => {
    try {
      if (form.password !== form.confirmPassword) {
        alert('Passwords do not match');
        return;
      }
      await authStore.register(form);
      router.push('/login');
    } catch (error) {
      console.error(error);
    }
  };
  </script>
  