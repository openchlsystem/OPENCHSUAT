import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/store/auth';

// Public Views
import HomeView from '@/views/HomeView.vue';
import LoginView from '@/views/auth/LoginView.vue';
import ForgotPasswordView from '@/views/auth/ForgotPasswordView.vue';

// Admin Views
const AdminLayout = () => import('@/layouts/AdminLayout.vue');
const AdminDashboard = () => import('@/views/admin/AdminDashboard.vue');
const OrganizationManagementView = () => import('@/views/admin/OrganizationManagementView.vue');
const SystemManagementView = () => import('@/views/admin/SystemManagementView.vue');
const FunctionalityManagementView = () => import('@/views/admin/FunctionalityManagementView.vue');
const TestCaseListView = () => import('@/views/admin/TestCaseListView.vue');
const DefectsView = () => import('@/views/admin/DefectsView.vue');
const ReportsView = () => import('@/views/admin/ReportsView.vue');
const SettingsView = () => import('@/views/admin/SettingsView.vue');
const UserManagementView = () => import('@/views/admin/UserManagementView.vue');

// Tester Views
const TesterLayout = () => import('@/layouts/TesterLayout.vue');
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
  { path: '/', name: 'Home', component: HomeView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/forgot-password', name: 'ForgotPassword', component: ForgotPasswordView },

  // Admin Routes
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      { path: 'dashboard', name: 'AdminDashboard', component: AdminDashboard },
      { path: 'organizations', name: 'OrganizationManagementView', component: OrganizationManagementView },
      { path: 'systems', name: 'SystemManagementView', component: SystemManagementView },
      { path: 'functionalities', name: 'FunctionalityManagementView', component: FunctionalityManagementView },
      { path: 'test-cases', name: 'TestCaseListView', component: TestCaseListView },
      { path: 'defects', name: 'DefectsView', component: DefectsView },
      { path: 'reports', name: 'ReportsView', component: ReportsView },
      { path: 'settings', name: 'SettingsView', component: SettingsView },
      { path: 'users', name: 'UserManagementView', component: UserManagementView }
    ],
  },

  // Tester Routes
  {
    path: '/tester',
    component: TesterLayout,
    meta: { requiresAuth: true, role: 'tester' },
    children: [
      { path: 'dashboard', name: 'TesterDashboard', component: TesterDashboard },
      { path: 'assigned-tests', name: 'AssignedTestsView', component: AssignedTests },
      { path: 'test-execution', name: 'TestExecutionView', component: TestExecution },
      { path: 'defect-reporting', name: 'DefectReportView', component: DefectReport },
      { path: 'test-history', name: 'TestHistoryView', component: TestHistory }
    ],
  },

  // Catch-all
  { path: '/:pathMatch(.*)*', redirect: '/' }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const user = getUser();

  if (to.meta.requiresAuth) {
    if (!isAuthenticated()) {
      next('/login');
    } else if (to.meta.role && user?.role !== to.meta.role) {
      next('/');
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
