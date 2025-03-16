import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '@/views/auth/LoginView.vue';
import RegisterView from '@/views/auth/RegisterView.vue';
import ForgotPasswordView from '@/views/auth/ForgotPasswordView.vue';
import AdminDashboard from '@/views/admin/AdminDashboard.vue';
import DefectsView from '@/views/admin/DefectsView.vue';
import ReportsView from '@/views/admin/ReportsView.vue';
//import ViewerDashboard from '@/views/viewer/ViewerDashboard.vue';
import HomeView from '@/views/HomeView.vue';
import TestCaseListView from '@/views/admin/TestCaseListView.vue';
const routes = [
    { path: '/', redirect: '/login' }, // Redirect root to register
    { path: '/login', component: LoginView },
    { path: '/register', component: RegisterView },
    { path: '/forgot-password', component: ForgotPasswordView },
    { path: '/admin/test-cases', component: TestCaseListView },
  {
    path: '/',
    name: 'Home',
    component: HomeView,  // Home view showing the login button
 },

  // Admin Routes
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    beforeEnter: (to, from, next) => {
      const user = getUser();
      if (isAuthenticated() && user && user.role === 'admin') {
        next();
      } else {
        next('/');
      }
    },
  },
  {
    path: '/admin/defects',
    name: 'DefectsView',
    component: DefectsView,
    beforeEnter: (to, from, next) => {
      const user = getUser();
      if (isAuthenticated() && user && user.role === 'admin') {
        next();
      } else {
        next('/');
      }
    },
  },
  {
    path: '/admin/reports',
    name: 'ReportsView',
    component: ReportsView,
    beforeEnter: (to, from, next) => {
      const user = getUser();
      if (isAuthenticated() && user && user.role === 'admin') {
        next();
      } else {
        next('/');
      }
    },
  },
  {
    path: '/admin/settings',
    name: 'SettingsView',
    component: () => import('@/views/admin/SettingsView.vue'),
    beforeEnter: (to, from, next) => {
      const user = getUser();
      if (isAuthenticated() && user && user.role === 'admin') {
        next();
      } else {
        next('/');
      }
    },
  },
  {
    path: '/admin/system-management',
    name: 'SystemManagementView',
    component: () => import('@/views/admin/SystemManagementView.vue'),
    beforeEnter: (to, from, next) => {
      const user = getUser();
      if (isAuthenticated() && user && user.role === 'admin') {
        next();
      } else {
        next('/');
      }
    },
  },

  {
    path: '/admin/test-steps',
    name: 'TestStepsView',
    component: () => import('@/views/admin/TestSteps.vue'),
    beforeEnter: (to, from, next) => {
      const user = getUser();
      if (isAuthenticated() && user && user.role === 'admin') {
        next();
      } else {
        next('/');
      }
    },
  },
  {
    path: '/admin/users',
    name: 'UserManagementView',
    component: () => import('@/views/admin/UserManagementView.vue'),
    beforeEnter: (to, from, next) => {
      const user = getUser();
      if (isAuthenticated() && user && user.role === 'admin') {
        next();
      } else {
        next('/');
      }
    },
  },
  //{
   // path: '/viewer/dashboard',
    //name: 'ViewerDashboard',
    //component: ViewerDashboard,  // New viewer view
    //meta: { layout: 'ViewerLayout' },
  //},
  // Tester Routes
  {
    path: '/tester/dashboard',
    name: 'TesterDashboardView',
    component: () => import('@/views/tester/TesterDashboard.vue'),
    beforeEnter: (to, from, next) => {
      const user = getUser();
      if (isAuthenticated() && user && user.role === 'tester') {
        next();
      } else {
        next('/');
      }
    },
  },
  {
    path: '/tester/assigned-tests',
    name: 'AssignedTestsView',
    component: () => import('@/views/tester/AssignedTestsView.vue'),
    beforeEnter: (to, from, next) => {
      const user = getUser();
      if (isAuthenticated() && user && user.role === 'tester') {
        next();
      } else {
        next('/');
      }
    },
  },
  {
    path: '/tester/test-execution/:testId',
    name: 'TestExecutionView',
    component: () => import('@/views/tester/TestExecutionView.vue'),
    props: true,
    beforeEnter: (to, from, next) => {
      const user = getUser();
      if (isAuthenticated() && user && user.role === 'tester') {
        next();
      } else {
        next('/');
      }
    },
  },
  {
    path: '/tester/defect-report',
    name: 'DefectReportView',
    component: () => import('@/views/tester/DefectReportView.vue'),
    beforeEnter: (to, from, next) => {
      const user = getUser();
      if (isAuthenticated() && user && user.role === 'tester') {
        next();
      } else {
        next('/');
      }
    },
  },
  {
    path: '/tester/test-history',
    name: 'TestHistoryView',
    component: () => import('@/views/tester/TestHistoryView.vue'),
    beforeEnter: (to, from, next) => {
      const user = getUser();
      if (isAuthenticated() && user && user.role === 'tester') {
        next();
      } else {
        next('/');
      }
    },
  },

  // Reports Routes
  {
    path: '/reports/test-progress',
    name: 'TestCaseProgressView',
    component: () => import('@/views/reports/TestCaseProgressView.vue'),
    beforeEnter: (to, from, next) => {
      const user = getUser();
      if (isAuthenticated() && user) {
        next();
      } else {
        next('/');
      }
    },
  },
  {
    path: '/reports/defects',
    name: 'DefectsDashboardView',
    component: () => import('@/views/reports/DefectsDashboardView.vue'),
    beforeEnter: (to, from, next) => {
      const user = getUser();
      if (isAuthenticated() && user) {
        next();
      } else {
        next('/');
      }
    },
  },
  {
    path: '/reports/tester-performance',
    name: 'TesterPerformanceView',
    component: () => import('@/views/reports/TesterPerformanceView.vue'),
    beforeEnter: (to, from, next) => {
      const user = getUser();
      if (isAuthenticated() && user) {
        next();
      } else {
        next('/');
      }
    },
  },

  // Admin Functionalities
  {
    path: '/admin/functionalities',
    name: 'FunctionalityManagementView',
    component: () => import('@/views/admin/FunctionalityManagementView.vue'),
    beforeEnter: (to, from, next) => {
      const user = getUser();
      if (isAuthenticated() && user && user.role === 'admin') {
        next();
      } else {
        next('/');
      }
    },
  },
  {
    path: '/admin/export',
    name: 'ExportReports',
    component: () => import('@/views/reports/ExportReportsView.vue'),
    beforeEnter: (to, from, next) => {
      const user = getUser();
      if (isAuthenticated() && user) {
        next();
      } else {
        next('/');
      }
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
