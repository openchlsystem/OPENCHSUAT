import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path' // Import path for aliasing

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src') // Define the '@' alias for 'src'
    }
  }
})

