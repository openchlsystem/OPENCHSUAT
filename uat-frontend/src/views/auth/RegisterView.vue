<template>
  <div class="auth-container">
    <!-- Welcome Section -->
    <div class="welcome-section">
      <h1>Welcome to UAT</h1>
      <p>Seamlessly transforming ideas into efficiency—your system, your success!</p>
    </div>

    <!-- Form Section -->
    <div class="form-container">
      <h2>Register</h2>
      <form @submit.prevent="registerUser">
        <div class="form-group">
          <label>WhatsApp Number</label>
          <input type="text" v-model="whatsapp_number" placeholder="Enter your WhatsApp number" required />
        </div>

        <div class="form-group">
          <label>Name</label>
          <input type="text" v-model="name" placeholder="Enter your name" required />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input type="password" v-model="password" placeholder="Enter a strong password" required />
        </div>

        <button type="submit">Register</button>
      </form>

      <div class="action-links">
        <router-link to="/login" class="login-link">Already have an account? Login</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth";

export default {
  setup() {
    const whatsapp_number = ref("");
    const name = ref("");
    const password = ref("");
    const router = useRouter();
    const authStore = useAuthStore();

    const registerUser = async () => {
      try {
        await authStore.registerUser(whatsapp_number.value, password.value);
        alert("Registration successful! Redirecting to login...");
        router.push("/login"); // Redirect user to login page
      } catch (error) {
        alert("Registration failed. Please try again.");
        console.error("Registration error:", error);
      }
    };

    return {
      whatsapp_number,
      name,
      password,
      registerUser,
    };
  },
};
</script>

<style scoped>
.auth-container {
  display: flex;
  height: auto;
  width: 100%;
  background: linear-gradient(145deg, #0a0a0a, #1f1f1f);
  color: #ffffff;
  overflow: hidden;
}

.welcome-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 3rem;
  text-align: center;
  background: linear-gradient(135deg, #151515, #222222);
}

.form-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #2c2f48, #1e1f3b);
  padding: 2rem;
  box-shadow: -10px 0 30px rgba(0, 0, 0, 0.4);
  min-height: 100vh;
}

.form-group {
  width: 100%;
  max-width: 400px;
  margin-bottom: 1.2rem;
}

label {
  font-weight: 600;
  display: block;
  margin-bottom: 0.5rem;
}

input {
  width: 100%;
  padding: 0.8rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  outline: none;
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

button {
  width: 100%;
  padding: 0.8rem;
  background: #646cff;
  border: none;
  cursor: pointer;
  transition: background 0.3s ease;
}

button:hover {
  background: #535bf2;
}

.action-links {
  margin-top: 1.5rem;
  text-align: center;
}

.login-link {
  color: #646cff;
  text-decoration: underline;
  cursor: pointer;
}

@media (max-width: 768px) {
  .auth-container {
    flex-direction: column;
    align-items: center;
    width: 100%;
    margin: 0;
  }

  .form-container {
    height: 100vh;
    width: 100%;
    padding: 1.5rem;
  }

  .welcome-section {
    display: none;
  }
}
</style>
