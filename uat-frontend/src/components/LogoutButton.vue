<template>
    <button @click="handleLogout" class="btn btn-danger">Logout</button>
  </template>
  
  <script>
  import { logout } from '@/utils/auth';
  
  export default {
    methods: {
      handleLogout() {
        logout();
        this.$router.push('/login');
      }
    }
  }
  </script>
  