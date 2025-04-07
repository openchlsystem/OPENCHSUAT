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
const AssignedTestDetails = () => import('@/views/tester/AssignedTestDetails.vue'); // <-- Added this import

// Custom JWT decode function (no dependency required)
function decodeJwt(token) {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(jsonPayload);
  } catch (error) {
    console.error("Error decoding token:", error);
    return null;
  }
}

const routes = [
  { path: "/", name: "Home", component: HomeView },
  { path: "/login", name: "Login", component: LoginView },
  { path: "/register", name: "Register", component: RegisterView },

  // Admin Routes
  {
    path: "/admin",
    component: AdminLayout,
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      { path: "", name: "AdminDashboardDefault", component: AdminDashboard },
      { path: "dashboard", name: "AdminDashboard", component: AdminDashboard },
      { path: 'organizations', name: 'OrganizationManagementView', component: OrganizationManagementView },
      { path: 'systems', name: 'SystemManagementView', component: SystemManagementView },
      { path: 'functionalities', name: 'FunctionalityManagementView', component: FunctionalityManagementView },
      { path: 'test-cases', name: 'TestCaseListView', component: TestCaseListView },
      { path: 'defects', name: 'DefectsView', component: DefectsView },
      { path: 'reports', name: 'ReportsView', component: ReportsView },
      { path: 'settings', name: 'SettingsView', component: SettingsView },
      { path: 'users', name: 'UserManagementView', component: UserManagementView },
      {
        path: 'functionalities/:functionalityId/test-cases',
        name: 'FunctionalityTestCases',
        component: () => import('@/views/admin/FunctionalityTestCasesView.vue')
      },
    ],
  },
  // Tester Routes
  {
    path: '/tester',
    component: TesterLayout,
    meta: { requiresAuth: true, role: 'tester' },
    children: [
      { path: "", name: "TesterDashboardDefault", component: TesterDashboard },
      { path: 'dashboard', name: 'TesterDashboard', component: TesterDashboard },
      { path: 'assigned-tests', name: 'AssignedTestsView', component: AssignedTests },
      { path: 'assigned-tests/:id', name: 'AssignedTestDetails', component: AssignedTestDetails }, // <-- New Route
      { path: 'test-execution', name: 'TestExecutionView', component: TestExecution },
      { path: 'defect-reporting', name: 'DefectReportView', component: DefectReport },
      { path: 'test-history', name: 'TestHistoryView', component: TestHistory }
    ],
  },
  // Catch-all route
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Global Navigation Guard
router.beforeEach((to, from, next) => {
  console.log(`Navigation to: ${to.path}`);

  // Try to get the auth store
  let authStore;
  try {
    authStore = useAuthStore();
    console.log("Auth store accessed, userRole:", authStore.userRole);
  } catch (error) {
    console.error("Failed to access auth store:", error);
  }

  // Check for token in localStorage
  const token = localStorage.getItem("access_token");
  console.log("Token exists:", !!token);

  // Get user from localStorage as fallback
  let userRole = null;
  if (authStore?.userRole) {
    userRole = authStore.userRole;
  } else {
    try {
      const user = JSON.parse(localStorage.getItem('user'));
      userRole = user?.role || null;
      console.log("User role from localStorage:", userRole);
    } catch (error) {
      console.error("Error parsing user from localStorage");
    }
  }

  // Determine if the user is authenticated
  let isAuthenticated = false;
  if (token) {
    try {
      const decoded = decodeJwt(token);
      if (decoded) {
        const now = Date.now() / 1000;
        if (!decoded.exp || decoded.exp > now) {
          isAuthenticated = true;
          console.log("User is authenticated");
        } else {
          console.log("Token expired");
          localStorage.removeItem("access_token");
          if (authStore && typeof authStore.logout === 'function') {
            authStore.logout();
          }
        }
      }
    } catch (error) {
      console.error("Token validation error:", error);
    }
  }

  // Handle routes requiring authentication
  if (to.meta.requiresAuth) {
    if (!isAuthenticated) {
      console.log("Authentication required, redirecting to login");
      return next('/login');
    }

    // Check role requirements
    if (to.meta.role && to.meta.role !== userRole) {
      console.log(`Role mismatch. Required: ${to.meta.role}, User has: ${userRole}`);

      // Redirect based on user's actual role
      if (userRole === 'admin') {
        console.log("Redirecting to admin dashboard");
        return next('/admin/dashboard');
      } else if (userRole === 'tester') {
        console.log("Redirecting to tester dashboard");
        return next('/tester/dashboard');
      } else {
        console.log("Unknown role, redirecting to home");
        return next('/');
      }
    }

    // All checks passed
    console.log("Authentication and role checks passed");
    return next();
  }
  // Handle login/register when already authenticated
  else if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
    console.log("User already authenticated, redirecting based on role");

    if (userRole === 'admin') {
      console.log("Redirecting to admin dashboard");
      return next('/admin/dashboard');
    } else if (userRole === 'tester') {
      console.log("Redirecting to tester dashboard");
      return next('/tester/dashboard');
    } else {
      console.log("Unknown role, redirecting to home");
      return next('/');
    }
  }

  // Allow navigation for public routes
  console.log("Proceeding with navigation");
  return next();
});

export default router;
