import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),
  actions: {
    async login(form) {
      console.log('Attempting mock login...')

      // Dummy data for testing
      const testUsers = [
        {
          email: 'admin@example.com',
          password: 'Admin@123',
          role: 'admin',
        },
        {
          email: 'tester@example.com',
          password: 'Tester@123',
          role: 'tester',
        },
      ]

      // Find matching user
      const user = testUsers.find(
        (u) => u.email === form.email && u.password === form.password
      )

      if (user) {
        this.user = user
        localStorage.setItem('user', JSON.stringify(user))
        console.log('Mock user logged in:', this.user)
        return user
      } else {
        throw new Error('Invalid email or password')
      }
    },

    logout() {
      localStorage.removeItem('user')
      this.user = null
    },
  },
})
