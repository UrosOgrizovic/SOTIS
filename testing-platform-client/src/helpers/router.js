import Vue from 'vue';
import Router from 'vue-router';

import Home from '../components/Home'
import Login from '../components/Login'
import Register from '../components/Register'
import Exam from '../components/Exam'
import Question from '../components/Question'
import Choice from '../components/Choice'

Vue.use(Router);

export const router = new Router({
  mode: 'history',
  routes: [
    { path: '/', component: Home },
    { path: '/login', component: Login },
    { path: '/register', component: Register },
    { path: '/exam', component: Exam },
    { path: '/question', component: Question },
    { path: '/choice', component: Choice },

    // otherwise redirect to home
    { path: '*', redirect: '/' }
  ]
});

router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/login', '/register'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem('user');

  if (authRequired && !loggedIn) {
    return next('/login');
  }

  next();
})