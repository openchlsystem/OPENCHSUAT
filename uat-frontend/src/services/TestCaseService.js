import axios from 'axios';

const API_URL = '/api/testcases';

export default {
  getTestCases(filters) {
    return axios.get(API_URL, { params: filters });
  },

  deleteTestCase(id) {
    return axios.delete(`${API_URL}/${id}`);
  },

  getSystems() {
    return axios.get('/api/systems');
  },

  getFunctionalities() {
    return axios.get('/api/functionalities');
  },

  getUsers() {
    return axios.get('/api/users');
  }
};
