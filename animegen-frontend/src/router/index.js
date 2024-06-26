import { createRouter, createWebHistory } from 'vue-router';
import Auth from '../components/Auth.vue'
import MainApp from '../views/MainApp.vue';

const routes = [
  { path: '/:catchAll(.*)', redirect: '/app', meta: { requiresAuth: true } },
  {path:  '/auth', component : Auth},
  { path: '/app', component: MainApp, meta: { requiresAuth: true } },

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('accessToken');
  if (to.matched.some(record => record.meta.requiresAuth) && !isLoggedIn) {
    next('/auth');
  } else {
    next();
  }
});

export default router;
