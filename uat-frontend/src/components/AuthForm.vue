<template>
    <div class="auth-form">
      <h2>{{ title }}</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Email</label>
          <input type="email" v-model="form.email" required />
        </div>
        <div class="form-group" v-if="isRegister || isLogin">
          <label>Password</label>
          <input type="password" v-model="form.password" required />
        </div>
        <div class="form-group" v-if="isRegister">
          <label>Confirm Password</label>
          <input type="password" v-model="form.confirmPassword" required />
        </div>
        <button type="submit" class="btn btn-primary">{{ buttonText }}</button>
        <slot></slot>
      </form>
    </div>
  </template>
  
  <script setup>
  import { reactive, defineProps, defineEmits } from 'vue';
  
  defineProps({
    title: String,
    buttonText: String,
    isRegister: Boolean,
    isLogin: Boolean,
  });
  
  const emit = defineEmits(['submit']);
  
  const form = reactive({
    email: '',
    password: '',
    confirmPassword: '',
  });
  
  const handleSubmit = () => {
    emit('submit', { ...form });
  };
  </script>
  
  <style scoped>
  .auth-form {
    max-width: 400px;
    margin: auto;
    padding: 20px;
    border-radius: 8px;
    background: #fff;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  input {
    width: 100%;
    padding: 10px;
    border-radius: 4px;
    border: 1px solid #ccc;
  }
  
  button {
    width: 100%;
    padding: 10px;
    border-radius: 4px;
    background-color: #ff6600;
    color: #fff;
    border: none;
    cursor: pointer;
    transition: background 0.3s;
  }
  
  button:hover {
    background-color: #cc5500;
  }
  </style>
  