<template>
  <div class="auth-container">
      <!-- Welcome Section -->
      <div class="welcome-section">
          <h1>Welcome to UAT System</h1>
          <p>Streamline your testing process efficiently.</p>
          <img class="moving-image" src="/public/bc2.png" alt="Welcome Illustration" />
      </div>

      <!-- Form Section -->
      <div class="form-container">
          <h2>{{ isRegister ? "Register" : "Login" }}</h2>
          <form @submit.prevent="isRegister ? registerUser() : verifyOTP()">
              <div class="form-group">
                  <label>WhatsApp Number</label>
                  <input type="text" v-model="whatsapp_number" placeholder="Enter your WhatsApp number" required />
              </div>

              <div class="form-group" v-if="isRegister">
                  <label>Name</label>
                  <input type="text" v-model="name" placeholder="Enter your name" required />
              </div>

              <div class="form-group" v-if="isRegister">
                  <label>Password</label>
                  <input type="password" v-model="password" placeholder="Enter a strong password" required />
              </div>

              <div class="form-group" v-if="otpRequested">
                  <label>OTP</label>
                  <input type="text" v-model="otp" placeholder="Enter OTP" required />
              </div>

              <button type="submit">
                  {{ isRegister ? "Register" : otpRequested ? "Verify OTP" : "Request OTP" }}
              </button>
          </form>

          <button @click="toggleMode" class="toggle-btn">
              {{ isRegister ? "Already have an account? Login" : "New user? Register" }}
          </button>
      </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useToast } from "vue-toastification";
import apiClient from "@/utils/axios";
import { useRouter } from "vue-router";

export default {
  setup() {
      const whatsapp_number = ref("");
      const name = ref("");
      const password = ref("");
      const otp = ref("");
      const isRegister = ref(false);
      const otpRequested = ref(false);
      const router = useRouter();
      const toast = useToast();

      const toggleMode = () => {
          isRegister.value = !isRegister.value;
          otpRequested.value = false;
          whatsapp_number.value = "";
          name.value = "";
          password.value = "";
          otp.value = "";
      };

      const registerUser = async () => {
          console.log("Register function called"); // Debugging

          try {
              const response = await apiClient.post("/auth/register/", {
                  whatsapp_number: whatsapp_number.value,
                  name: name.value,
                  password: password.value,
              });
              toast.success(response.data.message);
              toggleMode();
          } catch (error) {
              toast.error("Registration failed.");
          }
      };

      const requestOTP = async () => {
          try {
              const response = await apiClient.post("/auth/request-otp/", {
                  whatsapp_number: whatsapp_number.value,
              });
              otpRequested.value = true;
              toast.success(response.data.message);
          } catch (error) {
              toast.error("OTP request failed.");
          }
      };

      const verifyOTP = async () => {
          if (!otpRequested.value) {
              return requestOTP();
          }

          try {
              const response = await apiClient.post("/auth/verify-otp/", {
                  whatsapp_number: whatsapp_number.value,
                  otp: otp.value,
              });
              toast.success("OTP Verified! Welcome!");
              localStorage.setItem("access_token", response.data.access);
              router.push("/dashboard");
          } catch (error) {
              toast.error("Invalid OTP.");
          }
      };

      return {
          whatsapp_number,
          name,
          password,
          otp,
          isRegister,
          otpRequested,
          toggleMode,
          registerUser,
          verifyOTP,
      };
  },
};
</script>

<style scoped>
.auth-container {
  display: flex;
  height: 80vh;
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

.moving-image {
  width: 50%;
  animation: float 3s infinite ease-in-out;
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

.toggle-btn {
  background: transparent;
  color: #646cff;
  cursor: pointer;
  margin-top: 1rem;
  text-decoration: underline;
}

@keyframes float {
  0% {
      transform: translateY(0);
  }

  50% {
      transform: translateY(-10px);
  }

  100% {
      transform: translateY(0);
  }
}

@media (max-width: 1024px) {
  .auth-container {
      flex-direction: column;
      align-items: center;
      height: auto;
      width: 100%;
      margin: 0;
  }

  .welcome-section {
      height: 40vh;
  }

  .form-container {
      height: 60vh;
  }
}

@media (max-width: 768px) {
  .auth-container {
      flex-direction: column;
      align-items: center;
      height: auto;
      width: 100%;
      margin: 0;
  }

  .moving-image {
      width: 70%;
  }

  .form-group {
      max-width: 300px;
  }
}

@media (max-width: 480px) {
  .moving-image {
      width: 90%;
  }

  .welcome-section {
      padding: 2rem;
  }
}
</style>
