<template>
    <AuthForm 
      title="Forgot Password" 
      buttonText="Reset Password" 
      @submit="handleForgotPassword"
    />
  </template>
  
  <script setup>
  import { useAuthStore } from '@/store/auth';
  import AuthForm from '@/components/AuthForm.vue';
  
  const authStore = useAuthStore();
  
  const handleForgotPassword = async (form) => {
    try {
      await authStore.forgotPassword(form.email);
      alert('Check your email for reset instructions');
    } catch (error) {
      console.error(error);
    }
  };
  </script>
  