import { createRouter, createWebHistory } from "vue-router";
import HomeView from "./views/HomeView.vue";
import SystemsView from "./views/SystemsView.vue";
import TestCasesView from "./views/TestCasesView.vue";
import DefectsView from "./views/DefectsView.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/systems", component: SystemsView },
  { path: "/testcases", component: TestCasesView },
  { path: "/defects", component: DefectsView }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
