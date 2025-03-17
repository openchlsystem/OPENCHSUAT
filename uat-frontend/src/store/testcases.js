import TestCaseService from '@/services/TestCaseService';

const state = {
  testCases: [],
  systems: [],
  functionalities: [],
  users: []
};

const mutations = {
  SET_TEST_CASES(state, testCases) {
    state.testCases = testCases;
  },
  SET_SYSTEMS(state, systems) {
    state.systems = systems;
  },
  SET_FUNCTIONALITIES(state, functionalities) {
    state.functionalities = functionalities;
  },
  SET_USERS(state, users) {
    state.users = users;
  }
};

const actions = {
  async fetchTestCases({ commit }, filters = {}) {
    const response = await TestCaseService.getTestCases(filters);
    commit('SET_TEST_CASES', response.data);
  },

  async deleteTestCase({ dispatch }, id) {
    await TestCaseService.deleteTestCase(id);
    dispatch('fetchTestCases');
  },

  async fetchSystems({ commit }) {
    const response = await TestCaseService.getSystems();
    commit('SET_SYSTEMS', response.data);
  },

  async fetchFunctionalities({ commit }) {
    const response = await TestCaseService.getFunctionalities();
    commit('SET_FUNCTIONALITIES', response.data);
  },

  async fetchUsers({ commit }) {
    const response = await TestCaseService.getUsers();
    commit('SET_USERS', response.data);
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
