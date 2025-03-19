<template>
  <div id="app">
    <Navbar />
    <div class="container-fluid">
      <div class="row">
        <Sidebar v-if="isAdmin" />
        <main :class="isAdmin ? 'col-10' : 'col-12'">
          <router-view />
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue';
import Sidebar from './components/Sidebar.vue';

export default {
  name: 'App',
  components: {
    Navbar,
    Sidebar,
  },
  computed: {
    // Check if the current user is an admin
    isAdmin() {
      return localStorage.getItem('role') === 'admin'; // Assuming role is stored in localStorage
    },
  },
};
</script>

<style>
/* You can add global styles here or in a separate CSS file */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f8f9fa;
}
</style>
