<template>
  <div class="hero-section d-flex align-items-center justify-content-center text-center">
    <div class="content">
      <h1 class="title">Welcome to the UAT System</h1>
      <p class="subtitle">
        Streamline your testing process with ease and accuracy.
      </p>
      <div class="cta-buttons">
        <router-link to="/login" class="btn btn-primary">Get Started</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HeroSection',
}
</script>

<style scoped>
.hero-section {
  height: 100vh;
  background-color: #fff; /* White background */
}

.content {
  padding: 3rem;
  border-radius: 16px;
  background: rgba(0, 0, 0, 0.05); /* Light gray for contrast */
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  max-width: 700px;
  transition: transform 0.3s ease;
}

.content:hover {
  transform: translateY(-5px); /* Lift effect */
}

.title {
  font-size: 3.5rem;
  font-weight: 700;
  color: #000; /* Black */
  margin-bottom: 1.5rem;
  letter-spacing: 1px;
}

.subtitle {
  font-size: 1.5rem;
  font-weight: 400;
  color: #555;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.cta-buttons {
  display: flex;
  justify-content: center;
}

.btn-primary {
  background-color: #ff7f00; /* Orange */
  color: #fff;
  padding: 0.85rem 2.5rem;
  font-size: 1.2rem;
  font-weight: 500;
  border: none;
  border-radius: 8px;
  transition: background-color 0.3s ease, transform 0.2s;
}

.btn-primary:hover {
  background-color: #e66e00;
  transform: translateY(-3px);
}
</style>
