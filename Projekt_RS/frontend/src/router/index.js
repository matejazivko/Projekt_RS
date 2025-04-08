import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import store from '@/store'
import Signup from '../views/Signup.vue';
import Login from '../views/Login.vue';
import Komentar from '../views/Komentar.vue';
import Kontakt from '../views/Kontakt.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
    meta:{
      needsUser: true
    }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "login" */ '../views/Login.vue')
  },
  {
    path: '/signup',
    name: 'signup',
    component: () => import(/* webpackChunkName: "signup" */ '../views/Signup.vue')
  },
  {
    path: '/komentar',
    name: 'komentar',
    component: () => import ('@/views/Komentar.vue'),
    
  },
  {
    path: '/kontakt',
    name: 'kontakt',
    component: Kontakt,
   
  },
  {
    path: '/slike',
    name:'slike',
    component: () => import ('@/views/Slike.vue')
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach ((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated;
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login' });
  } else {
    next();
  }
});


export default router
