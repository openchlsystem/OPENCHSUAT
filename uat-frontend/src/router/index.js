import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/store/auth';

// Public Views
import HomeView from '@/views/HomeView.vue';
import LoginView from '@/views/auth/LoginView.vue';
import ForgotPasswordView from '@/views/auth/ForgotPasswordView.vue';
import RegisterView from '@/views/auth/RegisterView.vue';

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

// Check if the user is authenticated
const isAuthenticated = () => {
  const authStore = useAuthStore();
  return !!authStore.accessToken; // Check if the access token exists
};

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/forgot-password', name: 'ForgotPassword', component: ForgotPasswordView },
  { path: '/register', name: 'Register', component: RegisterView },

  // Admin Routes
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true },
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
    meta: { requiresAuth: true },
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
  const requiresAuth = to.meta.requiresAuth; // Check if the route requires authentication
  const isAuth = isAuthenticated(); // Check if the user is authenticated

  if (requiresAuth) {
    if (!isAuth) {
      // Redirect to login if not authenticated
      next('/login');
    } else {
      // Redirect all authenticated users to the Admin Dashboard
      if (to.name !== 'AdminDashboard') {
        next({ name: 'AdminDashboard' });
      } else {
        next();
      }
    }
  } else {
    // Redirect authenticated users away from public routes (e.g., login, register)
    if (isAuth && (to.name === 'Login' || to.name === 'Register' || to.name === 'ForgotPassword')) {
      next({ name: 'AdminDashboard' });
    } else {
      next();
    }
  }
});

export default router;