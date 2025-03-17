import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/store/auth';

import HomeView from '@/views/HomeView.vue';
import LoginView from '@/views/auth/LoginView.vue';
import RegisterView from '@/views/auth/RegisterView.vue';
import ForgotPasswordView from '@/views/auth/ForgotPasswordView.vue';

// Admin Views
import AdminDashboard from '@/views/admin/AdminDashboard.vue';
import DefectsView from '@/views/admin/DefectsView.vue';
import ReportsView from '@/views/admin/ReportsView.vue';
import TestCaseListView from '@/views/admin/TestCaseListView.vue';
const SettingsView = () => import('@/views/admin/SettingsView.vue');
const SystemManagementView = () => import('@/views/admin/SystemManagementView.vue');
const UserManagementView = () => import('@/views/admin/UserManagementView.vue');
const FunctionalityManagementView = () => import('@/views/admin/FunctionalityManagementView.vue');

// Tester Views
const TesterDashboard = () => import('@/views/tester/TesterDashboard.vue');
const AssignedTests = () => import('@/views/tester/AssignedTestsView.vue');
const TestExecution = () => import('@/views/tester/TestExecutionView.vue');
const DefectReport = () => import('@/views/tester/DefectReportView.vue');
const TestHistory = () => import('@/views/tester/TestHistoryView.vue');

// Reports
const TestCaseProgress = () => import('@/views/reports/TestCaseProgressView.vue');
const DefectsDashboard = () => import('@/views/reports/DefectsDashboardView.vue');
const TesterPerformance = () => import('@/views/reports/TesterPerformanceView.vue');
const ExportReports = () => import('@/views/reports/ExportReportsView.vue');

const getUser = () => {
  const authStore = useAuthStore();
  return authStore.user;
};

const isAuthenticated = () => {
  const authStore = useAuthStore();
  return !!authStore.user;
};

const routes = [
  // Public Routes
  { path: '/', name: 'Home', component: HomeView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/register', name: 'Register', component: RegisterView },
  { path: '/forgot-password', name: 'ForgotPassword', component: ForgotPasswordView },

  // Admin Routes
  { path: '/admin/dashboard', name: 'AdminDashboard', component: AdminDashboard, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/defects', name: 'DefectsView', component: DefectsView, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/reports', name: 'ReportsView', component: ReportsView, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/test-cases', name: 'TestCaseListView', component: TestCaseListView, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/settings', name: 'SettingsView', component: SettingsView, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/system-management', name: 'SystemManagementView', component: SystemManagementView, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/users', name: 'UserManagementView', component: UserManagementView, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/functionalities', name: 'FunctionalityManagementView', component: FunctionalityManagementView, meta: { requiresAuth: true, role: 'admin' } },

  // Tester Routes
  { path: '/tester/dashboard', name: 'TesterDashboard', component: TesterDashboard, meta: { requiresAuth: true, role: 'tester' } },
  { path: '/tester/assigned-tests', name: 'AssignedTests', component: AssignedTests, meta: { requiresAuth: true, role: 'tester' } },
  { path: '/tester/test-execution/:testId', name: 'TestExecution', component: TestExecution, props: true, meta: { requiresAuth: true, role: 'tester' } },
  { path: '/tester/defect-report', name: 'DefectReport', component: DefectReport, meta: { requiresAuth: true, role: 'tester' } },
  { path: '/tester/test-history', name: 'TestHistory', component: TestHistory, meta: { requiresAuth: true, role: 'tester' } },

  // Report Routes
  { path: '/reports/test-progress', name: 'TestCaseProgress', component: TestCaseProgress, meta: { requiresAuth: true, role: ['admin', 'viewer'] } },
  { path: '/reports/defects', name: 'DefectsDashboard', component: DefectsDashboard, meta: { requiresAuth: true, role: ['admin', 'viewer'] } },
  { path: '/reports/tester-performance', name: 'TesterPerformance', component: TesterPerformance, meta: { requiresAuth: true, role: ['admin', 'viewer'] } },
  { path: '/reports/export', name: 'ExportReports', component: ExportReports, meta: { requiresAuth: true, role: 'admin' } },

  // Catch-all for unknown routes
  { path: '/:pathMatch(.*)*', redirect: '/' },
];

// Global Route Guard for Authentication and Role Handling
const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const user = getUser();

  if (to.meta.requiresAuth) {
    if (!isAuthenticated()) {
      next('/login'); // Redirect unauthenticated users to login
    } else if (to.meta.role) {
      if (Array.isArray(to.meta.role)) {
        if (!to.meta.role.includes(user?.role)) {
          next('/'); // Redirect users without permission to home page
        } else {
          next(); // Allow access
        }
      } else if (user?.role !== to.meta.role) {
        next('/'); // Redirect if role does not match
      } else {
        next(); // Allow access
      }
    } else {
      next(); // Allow access
    }
  } else {
    next(); // Allow public access
  }
});

export default router;
