import axios from '@/axios';  // Axios instance

export default {
  state: {
    testHistory: []
  },
  mutations: {
    setTestHistory(state, data) {
      state.testHistory = data;
    }
  },
  actions: {
    async fetchTestHistory({ commit }) {
      try {
        const response = await axios.get('/api/test-history'); // Fetch from backend API
        commit('setTestHistory', response.data);
      } catch (error) {
        console.error('Error fetching test history:', error);
        throw error;
      }
    }
  },
  getters: {
    testHistory: (state) => state.testHistory
  }
};
