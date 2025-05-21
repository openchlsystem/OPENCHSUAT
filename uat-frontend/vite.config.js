import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: 'dist',
    target: 'es2015',
    assetsDir: 'assets'
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    host: '0.0.0.0',  // Add this for dev server
    port: 5173
  },
  preview: {
    host: '0.0.0.0',  // Explicit host binding
    port: 5100,       // Match your Docker port
    strictPort: true,
    allowedHosts: [
      'uat.bitz-itc.com',
      'localhost',
      /\.bitz-itc\.com$/  // Regex for all subdomains
    ]
  }
})