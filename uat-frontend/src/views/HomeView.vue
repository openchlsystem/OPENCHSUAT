<template>
  <div class="home-view">
    <HeroSection />
  </div>
</template>

<script>
import HeroSection from '@/components/HeroSection.vue'

export default {
  name: 'HomeView',
  components: {
    HeroSection,
  },
}
</script>

<style scoped>
.home-view {
  background-color: #fff;
}
</style>
