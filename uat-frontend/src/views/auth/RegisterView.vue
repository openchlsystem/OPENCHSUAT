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
  
  const handleRegister = async (formData) => {
  if (formData.password !== formData.confirmPassword) {
    alert("Passwords do not match.");
    return;
  }
  try {
    const registeredUser = await authStore.registerUser(formData.whatsapp_number, formData.password); // Corrected function name
    console.log("Registered user", registeredUser);
    alert("Registration successful!");
    // Handle successful registration (e.g., redirect, show success message)
  } catch (error) {
    console.error('Registration error:', error.message);
    // Handle registration error (e.g., show error message to user)
    alert(error.message);
  }
};
  </script>
  