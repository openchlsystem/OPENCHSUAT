import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/store/auth";

// Public Views
import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/auth/LoginView.vue";
import RegisterView from "@/views/auth/RegisterView.vue";

// Admin Layout and Views
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

const routes = [
  { path: "/", name: "Home", component: HomeView },
  { path: "/login", name: "Login", component: LoginView },
  { path: "/register", name: "Register", component: RegisterView },

  // Admin Routes (Require Authentication)
  {
    path: "/admin",
    component: AdminLayout, // Parent Layout
    meta: { requiresAuth: true }, // Requires authentication
    children: [
      { path: "", name: "AdminDashboardDefault", component: AdminDashboard }, // Default route for /admin
      { path: "dashboard", name: "AdminDashboard", component: AdminDashboard }, // Route for /admin/dashboard
      { path: 'organizations', name: 'OrganizationManagementView', component: OrganizationManagementView },
      { path: 'systems', name: 'SystemManagementView', component: SystemManagementView },
      { path: 'functionalities', name: 'FunctionalityManagementView', component: FunctionalityManagementView },
      { path: 'test-cases', name: 'TestCaseListView', component: TestCaseListView },
      { path: 'defects', name: 'DefectsView', component: DefectsView },
      { path: 'reports', name: 'ReportsView', component: ReportsView },
      { path: 'settings', name: 'SettingsView', component: SettingsView },
      { path: 'users', name: 'UserManagementView', component: UserManagementView },
    ],
  },
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
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Global Navigation Guard to Protect Admin Routes
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const isAuthenticated = !!authStore.accessToken;
  const userRole = authStore.userRole;

  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/login");
  } else if (to.meta.requiresAuth && isAuthenticated) {
    // Redirect based on the user's role if the route role doesn't match
    if (to.meta.role && to.meta.role !== userRole) {
      if (userRole === 'admin') {
        next('/admin/dashboard'); // Redirect admin to admin dashboard
      } else if (userRole === 'tester') {
        next('/tester/dashboard'); // Redirect tester to tester dashboard
      } else {
        next('/'); // Unknown role, send home
      }
    } else {
      next(); // Proceed if the role matches
    }
  } else if (to.path === '/login' && isAuthenticated) {
    // If logged in, prevent access to login page
    if (userRole === 'admin') {
      next('/admin/dashboard');
    } else if (userRole === 'tester') {
      next('/tester/dashboard');
    }
  } else {
    next();
  }
});

export default router;